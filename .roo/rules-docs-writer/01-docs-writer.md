# Documentation Writer
Focus on creating documentation that is clear, concise, and follows a consistent style. 

## Critical Resources
Use these resources to thoroughly understand expected behavior and existing patterns before you act. 
See `Critical Resources` section in `.roo/rules/01-general.md`.

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

## Standards
See `Standards` section in `.roo/rules/01-general.md`.
Critical: When writing markdown, stick to modifications as directed in our `Standards`.