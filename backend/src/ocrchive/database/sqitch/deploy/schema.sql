-- Deploy ocrchive:schema to pg

BEGIN;

CREATE SCHEMA ocrchive;

-- Function for automatically updating timestamp for updated_at column
CREATE OR REPLACE FUNCTION ocrchive.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = now(); 
   RETURN NEW;
END;
$$ language 'plpgsql';

-- Enum type for document statuses, will be extended later
CREATE TYPE ocrchive.document_status AS ENUM (
	'uploading',
	'uploaded',
	'failed'
);

-- Initial documents table holding just what we need to start accumulating source metadata
CREATE TABLE ocrchive.documents (
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	uri TEXT UNIQUE,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
	updated_at TIMESTAMP NOT NULL DEFAULT now(),
	status ocrchive.document_status
);

-- Accompanying trigger to call the aforementioned function when we update rows in documents table
CREATE TRIGGER update_documents_updated_at BEFORE UPDATE
ON documents FOR EACH ROW EXECUTE PROCEDURE ocrchive.update_updated_at_column();

COMMIT;
