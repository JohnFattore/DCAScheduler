CREATE TABLE users
(
    id INTEGER,
    username TEXT,
    password_hash INTEGER,
    PRIMARY KEY(id)
);

CREATE TABLE stocks
(
    id INTEGER,
    symbol TEXT,
    shares INTEGER,
    user_id INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);