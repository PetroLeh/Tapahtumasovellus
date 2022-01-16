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
    event_id INTEGER REFERENCES events ON DELETE CASCADE,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    additional_info TEXT
);

CREATE TABLE attendances (
    event_id INTEGER REFERENCES events ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    creator INTEGER REFERENCES users ON DELETE SET NULL,
    name TEXT NOT NULL,
    is_public BOOLEAN
);

CREATE TABLE members (
    group_id INTEGER REFERENCES groups ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    group_admin BOOLEAN
);

CREATE TABLE friends (
    user1 INTEGER REFERENCES users ON DELETE CASCADE,
    user2 INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE friend_invitations (
    user1 INTEGER REFERENCES users ON DELETE CASCADE,
    user2 INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE invitations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    invited_by INTEGER REFERENCES users ON DELETE CASCADE,
    event_id INTEGER REFERENCES events ON DELETE CASCADE
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    user_from INTEGER REFERENCES users ON DELETE SET NULL,
    user_to INTEGER REFERENCES users ON DELETE SET NULL,
    read BOOLEAN DEFAULT false,
    message TEXT
);

CREATE TABLE login_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    login_time TIMESTAMP,
    logout_time TIMESTAMP
);