# Documentation Writer
Focus on creating documentation that is clear, concise, and follows a consistent style. 

## Resources
**CRITICAL**
Use these resources to thoroughly understand the application (expected behavior and existing patterns) before planning: 
See `Critical Resources` section in `.roo/rules/01-general.md`.
See `.roo/rules/01-general.md` for modes.

## Primary Code References (Quick Jump)
- App factory and runtime:
  - `def create_app()`, `def load_user()`, `app.py`.
- Config:
  - `class Config`, `class DevelopmentConfig`, `class ProductionConfig`, `class TestingConfig`.
- DB:
  - `db = SQLAlchemy()`, `def init_db()`.
- Models:
  - `class UserType`, `class User`, `class UserSession`, `class UserDevice`, `class Notification`, `class UserAction`.
- Auth routes:
  - `def login()`, `def register()`, `def logout()`, `def forgot_password()`, `def reset_password()`, `def verify_email()`.
- Admin routes:
  - `def dashboard()`, `def view_users()`, `def add_user()`, `def edit_user()`, `def resellers()`.
- User routes:
  - `def profile()`.
- Reseller routes:
  - `def dashboard()`.
- Media routes:
  - `def list_media()`.

## Standards: Behavior
**CRITICAL**
- Follow the rules in `Standards` section in `.roo/rules/01-general.md`.
- Writing code: `Code standards` section in `.roo/rules/01-general.md`.
- Writing markdown: `Markdown standards` section in `.roo/rules/01-general.md`.
- Naming conventions: See `Naming conventions` section in `.roo/rules/01-general.md`.