#!/usr/bin/env python3
''' A module with tools for request caching and tracking. '''
import redis
import requests
from functools import wraps
from typing import Callable


cache = redis.Redis()


def cache_data(func: Callable) -> Callable:
    '''Decorator function to cache the output of fetched data.
    '''
    @wraps(func)
    def wrapper(url) -> str:
        '''Wrapper function for caching the output.
        '''
        cache.incr(f'count:{url}')
        result = cache.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = func(url)
        cache.set(f'count:{url}', 0)
        cache.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@cache_data
def fetch_url_content(url: str) -> str:
    '''
    Fetches and returns the content of a URL after
    caching the response and tracking the request.
    '''
    return requests.get(url).text
