CREATE TABLE IF NOT EXISTS articles (
    id          SERIAL PRIMARY KEY,
    arXiv_id    TEXT    NOT NULL UNIQUE,
    title       TEXT    NOT NULL,
    url         TEXT    NOT NULL,
    abstract    TEXT,
    embedding   REAL[]
);