# Database
ALWAYS use the live postgres database for testing and production (`PGDB`); never SQLite or any other database system.

## Credentials
- Connection credentials: `\.env`
- Users' credentials: `\.env` (hash is stored in the pw_hashed column)

## Structure
- Schema documentation: `.roo/docs/database_schema.md`
- SQLAlchemy model files: models/models_*.py (eg, `models/models_user.py`)
- Schema Inspector utility: `utils_db/schema_inspector.py`

## Source of Truth Hierarchy
The formal Source of Truth (SoT) hierarchy for database schema information:
1) PGDB (live PostgreSQL)
2) models_*.py (SQLAlchemy) (eg, `models/models_user.py`)
3) `.roo/docs/database_schema.md` (generated)

When there is any doubt about a column, see PGDB. If a column is needed or a column name needs to change, always ask user for permission to make the add/change.

## Schema Update Workflow
When making schema or data changes, follow this workflow in order:
1) Modify PGDB - Make changes to the live database (See "## Credentials" section above)
    When creating a script to check or change the database":
    a) Do NOT paste the script into the terminal.
    b) Check the `utils_db/` folder to see if a suitable or near-suitable script already exists. If so, use (or modify, if necessary) it.
    c) If no suitable script exists, write one as a .py file in the `utils_db/` folder and run it.
2) Update models_*.py - Update the appropriate SQLAlchemy model files to reflect database changes (eg, `models/models_user.py`
3) Regenerate documentation - Run: `python utils_db/schema_inspector.py generate-docs` to update `.roo/docs/database_schema.md`
4) Log changes - Record the date and change in `.roo/docs/pgdb_changes.md`

## Schema Inspector Utility
The `utils_db/schema_inspector.py` tool provides commands for schema management:
- `introspect` - Inspect live database schema and display structure
- `compare-db-models` - Compare live database against SQLAlchemy models to identify discrepancies
- `generate-docs` - Generate/update `.roo/docs/database_schema.md` from current database state
- `validate` - Verify schema documentation is up-to-date with the database

Usage examples:
- Introspect schema: `python utils_db/schema_inspector.py introspect`
- Compare: `python utils_db/schema_inspector.py compare-db-models`
- Generate docs: `python utils_db/schema_inspector.py generate-docs`
- Validate docs: `python utils_db/schema_inspector.py validate`
