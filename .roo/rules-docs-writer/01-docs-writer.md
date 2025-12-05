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
- Naming conventions: See `Naming conventions` section in `.roo/rules/01-general.md`.
- Writing markdown: Details below.

### Markdown syntax

#### Vertical Spacing
- Minimal empty lines between sections
- No empty lines between related list items
- Headers immediately followed by content
- Single empty line between major sections only

#### Reference Formatting Rules
Strictly enforce the following formatting for all file paths and references to reduce noise:
- No Markdown Links: Never use [name](path) syntax. Use plain backticks only.
- No Line Numbers: Strip all line number suffixes (e.g., :22).
- No Redundancy: Do not repeat the filename in brackets and parentheses.
- Contextual Pointers: When referencing specific sections, name the section instead of using line numbers.
Examples:
Bad: [app/models/user.py](app/models/user.py)
Good: `app/models/user.py`
Bad: [user.py](app/models/user.py:50)
Good: `app/models/user.py`
Bad: See `.roo/rules/01-general.md`
Good: See `Critical Resources` in `.roo/rules/01-general.md`

#### Formatting Standards
**Strictly enforce** the following minimalist formatting rules.
**Style & Typography**
- **References:** Use inline code backticks (e.g., `file.py`) for files and code. Never use brackets or links.
- **Indentation:** Use exactly 4 spaces for nested items.
**Lists & Spacing**
- **Numbering:** Use `)` as the separator (e.g., `1)`, `2)`). Never use periods (`1.`).
- **Density:** No empty lines between list items. Group related items tightly.
- **Headers:** Content must start on the very next line after a header. Do not insert an empty line.
**Examples**
**Bad** (Wrong list style, extra spacing):
```markdown
## Analysis

**Points:**

1. First item

2. Second item
```

**Good** (Compact, correct list style):
```markdown
## Analysis
**Points:**
1) First item
    - Nested detail
2) Second item
```