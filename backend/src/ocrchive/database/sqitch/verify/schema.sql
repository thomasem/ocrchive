-- Verify ocrchive:schema on pg

BEGIN;

DO $$
DECLARE
	result INTEGER;
BEGIN
	-- Assert schema exists
	SELECT COUNT(*) INTO result
	FROM information_schema.schemata
	WHERE schema_name = 'ocrchive';

	ASSERT result = 1, 'Schema ocrchive missing';

	-- Assert update_updated_at_column function exists
	SELECT COUNT(*) INTO result 
	FROM information_schema.routines
	WHERE routine_schema = 'ocrchive' AND
	routine_type = 'FUNCTION' AND
	routine_name = 'update_updated_at_column';

	ASSERT result = 1, 'Function update_updated_at_column missing';

	-- Assert document_statuses enum exists
	SELECT COUNT(*) INTO result
	FROM pg_type
	WHERE typcategory = 'E' AND
	typname = 'document_status';

	ASSERT result = 1, 'Type document_status missing';

	-- Assert documents table exists with expected columns
	PERFORM id, uri, created_at, updated_at, status FROM ocrchive.documents WHERE FALSE;

	-- Assert update_documents_updated_at trigger exists for documents table
	SELECT COUNT(*) INTO result
	FROM information_schema.triggers
	WHERE event_object_schema = 'ocrchive' AND
	event_object_table = 'documents' AND
	trigger_name = 'update_documents_updated_at';

	ASSERT result = 1, 'Trigger update_documents_updated_at missing';
END $$;

ROLLBACK;
