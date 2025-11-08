# Database
ALWAYS use the live postgres database for testing and production (`PGDB`); never SQLite or any other database system.

## Credentials
- DB connection credentials: `.env`
- Users' credentials: `.env`

## Structure
- Schema documentation: `database_schema.md`
- SQLAlchemy model files: models/models_*.py (eg, `models/models_user.py`)
- Schema Inspector utility: `utils/schema_inspector.py`

## Source of Truth Hierarchy
The formal Source of Truth (SoT) hierarchy for database schema information:
1) PGDB (live PostgreSQL)
2) models_*.py (SQLAlchemy) (eg, `models/models_user.py`)
3) database_schema.md (generated)

When there is any doubt about a column, see PGDB. If a column is needed or a column name needs to change, always ask user for permission to make the add/change.

## Schema Update Workflow
When making schema changes, follow this workflow in order:
1) Modify PGDB - Make changes to the live database (credentials in `.env`)
2) Update models_*.py - Update the appropriate SQLAlchemy model files to reflect database changes (eg, `models/models_user.py`)
3) Regenerate documentation - Run: `python utils/schema_inspector.py generate-docs` to update `database_schema.md`
4) Log changes - Record the date and change in `pgdb_changes.md`

## Schema Inspector Utility
The `utils/schema_inspector.py` tool provides commands for schema management:
- `introspect` - Inspect live database schema and display structure
- `compare-db-models` - Compare live database against SQLAlchemy models to identify discrepancies
- `generate-docs` - Generate/update `database_schema.md` from current database state
- `validate` - Verify schema documentation is up-to-date with the database

Usage examples:
- Introspect schema: `python utils/schema_inspector.py introspect`
- Compare: `python utils/schema_inspector.py compare-db-models`
- Generate docs: `python utils/schema_inspector.py generate-docs`
- Validate docs: `python utils/schema_inspector.py validate`
