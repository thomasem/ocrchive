-- Revert ocrchive:schema from pg

BEGIN;

DROP SCHEMA ocrchive CASCADE;

COMMIT;
