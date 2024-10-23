CREATE EXTENSION IF NOT EXISTS vector;

-- Create the magazine_information table
CREATE TABLE IF NOT EXISTS magazine_information (
    id SERIAL PRIMARY KEY,                         -- Unique identifier for each magazine
    title VARCHAR(255) NOT NULL,                   -- Magazine title
    author VARCHAR(255),                           -- Author of the magazine
    publication_date DATE,                         -- Date of publication
    category VARCHAR(100)                          -- Category or genre of the magazine
);

-- Create the magazine_content table
CREATE TABLE magazine_content (
    id SERIAL PRIMARY KEY,                         -- Unique identifier for each content entry
    magazine_id INT NOT NULL,                      -- Foreign key referencing magazine_information
    content TEXT NOT NULL,                         -- Actual content of the magazine
    vector_representation VECTOR,                  -- Vector representation for semantic search
    FOREIGN KEY (magazine_id)                      -- Foreign key constraint linking to magazine_information
        REFERENCES magazine_information(id)
        ON DELETE CASCADE                          -- Delete associated content when the magazine is deleted
);

-- Indexes (for performance improvement)
-- Index on magazine_information.title for faster searches by title
CREATE INDEX idx_magazine_information_title ON magazine_information(title);

-- Index on magazine_information.author for faster searches by author
CREATE INDEX idx_magazine_information_author ON magazine_information(author);

-- Index on magazine_content.magazine_id for faster lookups on content linked to a magazine
CREATE INDEX idx_magazine_content_magazine_id ON magazine_content(magazine_id);