#!/usr/bin/env python3
''' A module for using the Redis NoSQL data storage. '''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def track_calls(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        if isinstance(self._cache, redis.Redis):
            self._cache.incr(func.__qualname__)
        return func(self, *args, **kwargs)
    return wrapper


def track_history(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        input_key = '{}:inputs'.format(func.__qualname__)
        output_key = '{}:outputs'.format(func.__qualname__)
        if isinstance(self._cache, redis.Redis):
            self._cache.rpush(input_key, str(args))
        output = func(self, *args, **kwargs)
        if isinstance(self._cache, redis.Redis):
            self._cache.rpush(output_key, output)
        return output
    return wrapper


def show_history(fn: Callable) -> None:
    if fn is None or not hasattr(fn, '__self__'):
        return
    cache_store = getattr(fn.__self__, '_cache', None)
    if not isinstance(cache_store, redis.Redis):
        return
    function_name = fn.__qualname__
    input_key = '{}:inputs'.format(function_name)
    output_key = '{}:outputs'.format(function_name)
    function_call_count = 0
    if cache_store.exists(function_name) != 0:
        function_call_count = int(cache_store.get(function_name))
    print('{} was called {} times:'.format(function_name, function_call_count))
    function_inputs = cache_store.lrange(input_key, 0, -1)
    function_outputs = cache_store.lrange(output_key, 0, -1)
    for function_input, function_output in zip(function_inputs,
                                               function_outputs):
        print('{}(*{}) -> {}'.format(
            function_name,
            function_input.decode("utf-8"),
            function_output,

            ))


class DataCache:
    def __init__(self) -> None:
        self._cache = redis.Redis()
        self._cache.flushdb(True)

    @track_history
    @track_calls
    def store_data(self, data: Union[str, bytes, int, float]) -> str:
        data_key = str(uuid.uuid4())
        self._cache.set(data_key, data)
        return data_key

    def retrieve_data(self, key: str, conversion_fn: Callable = None) -> Union[
            str, bytes, int, float]:
        data = self._cache.get(key)
        return conversion_fn(data) if conversion_fn is not None else data

    def retrieve_string(self, key: str) -> str:
        return self.retrieve_data(key, lambda x: x.decode('utf-8'))

    def retrieve_integer(self, key: str) -> int:
        return self.retrieve_data(key, lambda x: int(x))
