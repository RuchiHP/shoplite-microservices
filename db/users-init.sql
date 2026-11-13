-- Runs automatically the first time the users-db container starts.
-- Compare with user-service/create_table.py and make the columns match.
CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    username          VARCHAR(100) NOT NULL,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT         NOT NULL,
    created_at    TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);
