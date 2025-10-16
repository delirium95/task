ALTER TABLE contacts
ADD COLUMN search_vector tsvector;

UPDATE contacts
SET search_vector =
    setweight(to_tsvector('english', coalesce(first_name, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(last_name, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(email, '')), 'B') ||
    setweight(to_tsvector('english', coalesce(description, '')), 'C');

CREATE INDEX idx_contacts_search_vector
ON contacts
USING GIN (search_vector);