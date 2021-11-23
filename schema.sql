CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    description TEXT,
    info TEXT
);

CREATE TABLE recurring_events (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    additional_info TEXT
);

CREATE TABLE attendances (
    event_id INTEGER REFERENCES events,
    user_id INTEGER REFERENCES users
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    creator INTEGER REFERENCES users,
    name TEXT NOT NULL
);

CREATE TABLE members (
    group_id INTEGER REFERENCES groups,
    user_id INTEGER REFERENCES users,
    group_admin BOOLEAN
);

CREATE TABLE friends (
    user1 INTEGER REFERENCES users,
    user2 INTEGER REFERENCES users
);
