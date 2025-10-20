# MediaShare Application Analysis

Flask-based media platform with role-based access, hierarchical reseller model, and credit system.

## Critical instructions

Highest priority - follow to the letter:
 `@\.roo\rules\01-general.md`

## Application Reference

### Core Files
- Entry: `app.py` - `create_app()`, `load_user()`
- Config: `config.py` - environment-based configuration
- Database: 
    - `@\.roo\rules\02-database.md`
    - `@\.roo\docs\database_schema.md`
    - `@\utils\database.py`
    - `@\models\models_*.py`
    - `db = SQLAlchemy()`
- Models: `models/models_*.py` - domain-specific data models

### Architecture Layers
- Core: `utils/*_core.py` - stateless business logic
- Presentation: `routes/utils_*_*.py` - Flask-aware utilities
- Routes: `routes/*.py` - blueprint definitions
- Templates: `templates/` - Jinja2 UI components

### Key Patterns
- Separation of concerns: core logic separate from Flask context
- Utility delegation: routes delegate to specialized utility functions
- Standardized responses: `utils/route_helpers.py` for consistent handling
- Audit logging: `UserAction.log_action()` throughout

## Application Structure

### Framework Stack
- Flask with Blueprints, SQLAlchemy ORM, Flask-Login, Flask-WTF CSRF, Flask-Mail
- PostgreSQL database (never SQLite)
- Jinja2 templating with responsive UI

### Blueprints
- Auth: `routes/auth.py` - login, register, password reset
- Admin: `routes/admin.py` - platform management
- User: `routes/user.py` - end-user functionality
- Reseller: `routes/reseller.py` - partner management
- Media: `routes/media.py` - public media access

### Core Modules (Business Logic)
- `utils/imdb_core.py` - IMDb API operations
- `utils/api_core.py` - unified API provider interface
- `utils/dashboard_core.py` - platform metrics
- `utils/media_core.py` - media processing and validation
- `utils/users_core.py` - user management
- `utils/genres_core.py` - genre operations
- `utils/payments_core.py` - payment processing

## Database Models

### User System (`models/models_user.py`)
- `UserType` - role definitions (admin, reseller, basic)
- `User` - hierarchical user model with parent/child relationships
- `UserSession` - session tracking with expiry
- `UserDevice` - device fingerprinting
- `UserAction` - comprehensive audit trail
- `Notification` - user notifications

### Domain Models
- Media: `models/models_media.py` - content management
- Payments: `models/models_payment.py` - financial transactions
- Support: `models/models_support.py` - ticket system
- Reseller: `models/models_reseller.py` - partner data
- Interactions: `models/models_interaction.py` - user engagement
- Referrals: `models/models_referral.py` - referral tracking

## Authentication & Security

### Authentication Flow (`routes/auth.py`)
- Login: email/password with lockout protection (5 attempts, 15 min)
- Registration: server-side validation, secure hashing
- Password reset: token-based with email verification
- CSRF protection: global via CSRFProtect
- Session management: Flask-Login with secure user loader

### Authorization
- Admin guard: `utils/auth_admin.py` - `admin_required()` decorator
- Role-based access: `current_user.user_type.code` checks
- Hierarchical permissions: parent/child user relationships

### Security Features
- Password hashing: Werkzeug (never plaintext)
- Account lockout: progressive delays
- Audit logging: all critical actions logged
- CSRF tokens: per-form validation

## Admin System

### Admin Routes (`routes/admin.py`)
- Dashboard: `/admin/` - platform metrics
- Users: `/admin/users` - CRUD operations
- Media: `/admin/media` - content management
- Upload: `/admin/media/upload` - file processing
- Genres: `/admin/genres` - taxonomy management
- Settings: `/admin/settings` - configuration

### Admin Utilities (Separation Pattern)
- `routes/utils_admin_dashboard.py` - metrics and analytics
- `routes/utils_admin_users.py` - user management operations
- `routes/utils_admin_media.py` - media operations
- `routes/utils_admin_api.py` - external API integration
- `routes/utils_admin_genres.py` - genre system
- `routes/utils_admin_payments.py` - financial data
- `routes/utils_admin_support.py` - ticket management
- `routes/utils_admin_resellers.py` - partner management

### Route Helpers (`utils/route_helpers.py`)
- `handle_util_result()` - standard response processing
- `handle_simple_util_result()` - read-only operations
- `handle_delete_result()` - deletion with flash messages

## Media System

### Upload Processing (`utils/media_core.py`)
- File validation: extension, size, MIME type
- Storage: organized by user and media type
- Metadata extraction: SHA-256, EXIF data
- Thumbnail generation: images only (300x300 JPEG)
- Multi-file support: batch processing

### Storage Structure
- Base: `static/uploads/media/`
- Organization: `media_type_code/user_id/`
- Thumbnails: `static/uploads/thumbnails/`
- Cleanup: automated file removal

### Media Routes
- Management: `/admin/media` - browse/search
- Upload: `/admin/media/upload` - file processing
- Edit: `/admin/media_edit/<id>` - metadata editing
- Owner selection: `/admin/media/select-owner` - dynamic assignment

## External APIs

### API Provider System (`utils/api_core.py`)
- `BaseApiProvider` - abstract interface
- `ImdbApiProvider` - active implementation
- `TmdbApiProvider` - preserved, disabled
- `TvdbApiProvider` - preserved, disabled

### IMDb Integration (`utils/imdb_core.py`)
- `imdb_search_core()` - title search with pagination
- `imdb_details_fetch_core()` - metadata retrieval
- `imdb_rating_core()` - rating via scraping
- `imdb_import_core()` - data preparation

### Admin API Routes
- Pull: `/admin/media/<id>/pull-imdb` - fetch metadata
- Search: `/admin/media/search-imdb` - title search
- Import: `/admin/media/import-imdb` - bulk import
- Rating: `/admin/media/<id>/rating-imdb` - rating retrieval

## User System

### User Routes (`routes/user.py`)
- Dashboard: `/user/` - personal metrics
- Profile: `/user/profile` - account management
- Media: `/user/media` - content access

### User Utilities
- `routes/utils_user_dashboard.py` - user metrics
- `routes/utils_user_profile.py` - profile operations
- `routes/utils_user_media.py` - media access
- `routes/utils_user_imdb.py` - search functionality

### Hierarchical Model
- Parent/child relationships: reseller → customers
- Credit system: balance tracking
- Permission inheritance: management capabilities

## Templates & Static Assets

### Template Structure
- Layout: `templates/layout.html` - base template
- Auth: `templates/auth/` - login, register, reset
- Admin: `templates/admin/` - management interfaces
- User: `templates/user/` - end-user pages
- Errors: `templates/errors/` - 404, 500 pages

### Static Assets
- CSS: `static/css/main.css` - responsive styling
- JavaScript: `static/js/` - interactive components
- Images: `static/images/` - logos, placeholders
- Uploads: `static/uploads/` - user content

## Configuration (`config.py`)

### Environment Classes
- `Config` - base configuration
- `DevelopmentConfig` - dev settings
- `ProductionConfig` - production settings
- `TestingConfig` - test environment (CSRF disabled)

### Database Configuration
- PostgreSQL: primary database
- URI construction: environment variables
- Engine options: connection pooling, pre-ping
- Migration support: SQLAlchemy integration

## Testing Infrastructure

### Test Structure (`tests/`)
- `conftest.py` - pytest fixtures
- `test_auth.py` - authentication flows
- `test_models.py` - database models
- `test_user.py` - user operations
- `test_e2e_auth.py` - end-to-end testing

### Testing Approach
- pytest framework with Flask test client
- Database fixtures for isolation
- Mock external APIs for reliability

## Development Tools

### Database Scripts
- `admin_setup.py` - create admin users
- `populate_*.py` - test data generation
- `check_*.py` - database verification
- `update_*.py` - data migration

### Analysis Tools
- `analyze_redundant_functions.py` - code quality
- `generate_schema_documentation.py` - DB docs
- `get_db_schema.py` - schema extraction

### Debug Scripts (`scripts-debug/`)
- `debug_admin_credentials.py` - verify admin user credentials and authentication
- `debug_admin_login.py` - trace admin login process step-by-step
- `debug_catch22_directors.py` - test director extraction for specific IMDb titles
- `debug_genre_save.py` - debug genre association save process
- `debug_imdb_tt0816692.py` - test IMDb API calls for specific titles
- `debug_import_issue.py` - diagnose Flask import failures and startup hangs
- `debug_login_trace.py` - comprehensive login procedure tracing
- `debug_test_data.py` - verify database user types and test data

## Key Functions Reference

### Application Factory
- `create_app()` - Flask app configuration
- `load_user()` - Flask-Login user loader
- `init_db()` - database initialization

### Authentication
- `login()` - user authentication
- `register()` - account creation
- `admin_required()` - authorization decorator

### Core Business Logic
- `imdb_search_core()` - external API search
- `media_upload_core()` - file processing
- `user_create_core()` - user management
- `dashboard_metrics_core()` - analytics

### Utility Functions
- `handle_util_result()` - response standardization
- `log_action()` - audit trail
- `validate_file()` - upload validation

## Documentation Structure

### Project Docs (`.roo/docs/`)
- `agents.md` - this file
- `database_schema.md` - DB structure
- `api-imdb-docs.md` - API documentation
- `core_modules/` - detailed module docs

### Rules & Guidelines (`.roo/rules*/`)
- `01-general.md` - core standards and workflow
- `02-database.md` - database operations
- `rules-debug/01-debug.md` - systematic debugging process
- `rules-code/01-code.md` - complex coding guidelines
- `rules-*/*.md` - mode-specific rules

### Planning & Logs
- `plan_*.md` - project planning
- `*_log.md` - execution logs
- `old_versions/` - backups
- `plans_completed/` - archived plans

## Common Patterns

### Error Handling
- Try/catch blocks with logging
- User-friendly error messages
- Graceful degradation for external APIs

### Data Validation
- Server-side validation for all inputs
- CSRF protection on state-changing operations
- SQL injection prevention via ORM

### Performance Considerations
- Database connection pooling
- Lazy loading for relationships
- Pagination for large datasets
- Thumbnail generation for images

## Operational Notes

### Development
- Environment variables for configuration
- Debug mode for development
- Comprehensive logging for troubleshooting

### Production Considerations
- Database migrations instead of `create_all()`
- HTTPS enforcement
- Email service integration
- File storage optimization