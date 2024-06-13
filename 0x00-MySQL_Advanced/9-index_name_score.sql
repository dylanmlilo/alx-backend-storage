-- Assuming the table names is already imported and exists
-- Create an index on the first letter of name and the score column
CREATE INDEX idx_name_first_score ON names (name(1), score)
