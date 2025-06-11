DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

DROP TABLE IF EXISTS photos CASCADE;

CREATE TABLE IF NOT EXISTS photos (
    id BIGINT PRIMARY KEY,
    width INTEGER,
    height INTEGER,
    url VARCHAR(255),
    photographer VARCHAR(255),
    photographer_url VARCHAR(255),
    photographer_id BIGINT,
    avg_color VARCHAR(7),
    src_original TEXT,
    src_large2x TEXT,
    src_large TEXT,
    src_medium TEXT,
    src_small TEXT,
    src_portrait TEXT,
    src_landscape TEXT,
    src_tiny TEXT,
    alt TEXT
);

