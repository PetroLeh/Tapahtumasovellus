CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    is_admin BOOLEAN
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    description TEXT,
    info TEXT
)
