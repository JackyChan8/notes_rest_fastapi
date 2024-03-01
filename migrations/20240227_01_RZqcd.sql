-- 
-- depends: 
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username VARCHAR(255) NOT NULL UNIQUE,
	password VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    is_published BOOL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    author_id INT,

    FOREIGN KEY (author_id) REFERENCES users(id)
);