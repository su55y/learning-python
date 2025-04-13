PRAGMA user_version=2;

ALTER TABLE test_table
ADD COLUMN description TEXT NOT NULL DEFAULT 'No description.';
