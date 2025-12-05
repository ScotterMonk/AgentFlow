# ALL MODES

## Environment & Commands
- **Platform:** Windows 11. Use PowerShell syntax.
- **Sequence:** Execute numbered steps in strict linear order. Do not skip or reorder.

---

## Critical Resources

### Sources of knowledge
- **App knowledge**: `agents.md`.
    - *Contains:* Environment, Patterns, Docs, API Framework.
- **Codebase**: `codebase_search`, `read_file`, `search_files`.
- Git diff, recent commits.
- **Credentials**: `.env`.
- **Web automation** & **browsing**: `browser_action`
- **Useful Discoveries**: Make use of and contribute to `.roo/docs/useful.md`.

### Database
See `.roo/rules/02-database.md` for all database procedures.

### Modes
**Planning & Orchestration**
- `/architect`: Simple planning. Create phases and tasks -> QA -> User Approval -> Switch to `/orchestrator`.
- `/planner-a`: Complex Plan Stage 1. Create phases -> Brainstorm -> Switch to `/planner-b`.
- `/planner-b`: Complex Plan Stage 2. Create detailed tasks -> User Approval -> Switch to `/planner-c`.
- `/planner-c`: Complex Plan Stage 3. QA -> Finalize -> Switch to `/orchestrator`.
- `/orchestrator`: Manage execution. Coordinate implementation modes to fulfill plan.

**Implementation & Ops**
- `/code`: Complex engineering, analysis, deep debugging.
- `/code-monkey`: Routine coding, strict instruction adherence.
- `/front-end`: UI implementation.
- `/tester`: Test creation and execution.
- `/debug`: Error investigation and diagnosis.
- `/githubber`: GitHub CLI operations.
- `/task-simple`: Small, isolated operations.
- `/ask`: General inquiries.

### Mode selection strategy
**Evaluate** the current `task`. If another mode is more appropriate, **pass** the `task` and parameters (concise WTS) to that mode.
**Prioritize** budget-friendly modes in this order (Low to High):
1.  **Low Budget** (Renaming, moving files, simple text replacement, DB column copying)
    - Use `/task-simple`
2.  **Medium Budget** (Refactoring, simple function creation, writing)
    - Use `/code-monkey` or `/tester`
3.  **High Budget** (Complex modification, or if Medium fails)
    - Use `/code`
4.  **Highest Budget** (Debugging, or if High fails)
    - Use `/debug`
**Special Exception:**
- **Front-End Tasks** (Medium or High complexity): **Always use** `/front-end`

---

## Standards

### Communication
Be brief; don't echo user requests.

### Modularization
**Scope**: Critical for Python, JS, and logic files.
- **Exception**: Do NOT apply this to CSS.

**Hard Limit**:
- **Enforce** a maximum of **450 lines of code** per file.
- **Split** larger files: Create more files with fewer functions rather than exceeding this limit.

**Utility Strategy**:
- **Extract** logic liberally into utility folders.
- **Naming Convention**: Use `utils/` or `utils_db/`.

### Simplification
Triggers: Redundancy, special cases, complexity.
Action: Consult `.roo/docs/simplification.md`. Refactor to unifying principles.

### Flask HTML Templates
Constraint: Use `jinja-html` language mode for Flask templates.
Enforcement: Re-apply `jinja-html` mode immediately after every save to prevent reversion.

### Naming Conventions: Domain-First
**Rationale**: Group related code by **Domain** (Subject) first, then **Specific** (Action/Qualifier).

#### 1. The Core Pattern
**Invert the standard naming order:**
- **Bad**: `{specific}_{domain}` (e.g., `edit_user`)
- **Good**: `{domain}_{specific}` (e.g., `user_edit`)

**Casing Rules**:
- **snake_case**: Files, functions, variables, DB tables/columns.
- **PascalCase**: Classes.

#### 2. Transformation Examples
| Type | Old Pattern | **New Pattern (Target)** | Note |
| :--- | :--- | :--- | :--- |
| **Files** | `admin_dashboard_utils.py` | `dashboard_utils_admin.py` | Domain is `dashboard` |
| **Functions** | `edit_user` | `user_edit` | Domain is `user` |
| **Classes** | `AdminPerson` | `PersonAdmin` | Better: Use `Person` w/ type param |

#### 3. Scope & Restrictions
**When to Apply**:
- **New Code**: **Always** apply this pattern.
- **Existing Code**: Apply **only** if you are already actively editing the file.

**STOP! Do NOT rename without explicit approval:**
- **Public APIs**: HTTP routes, library exports, CLI flags.
- **Database**: Tables and columns (requires migration).
- **Standards**: `__init__.py`, `setUp()`, `settings.py` (Django).

---

#### 4. CRITICAL: Refactoring Checklist
**If you rename a symbol, you MUST fix all references.**
Before finishing, verify:
1.  [ ] **Imports**: Updated in all other files?
2.  [ ] **Calls**: Function/Class usage updated everywhere?
3.  [ ] **Tests**: Do tests still pass?
4.  [ ] **Docs**: Updated docstrings/comments?
5.  [ ] **VS Code**: No errors in the Problems panel?

### Code Standards

#### 1. Mandatory Metadata
**Every** function or class you touch MUST have this comment header:
```python
# [Created-or-Modified] by [Model_Name] | YYYY-MM-DD_[Iteration]
# Example: # Modified by Claude-3.5-Sonnet | 2024-10-27_01
```
#### 2. Syntax & Style
Quotes: Enforce Double Quotes (") over Single Quotes (').
Good: x += "."
Bad: x += '.'
SQL: Always use Multi-line strings (""") for complex queries.
Templates: Set language mode to jinja-html.
Spacing: Keep vertical spacing compact (no excessive blank lines).
Readability: Prioritize Readable Code over "clever" one-liners.

#### 3. Comments
Preserve: Do NOT delete existing comments.
Add: Comment liberally. Explain why, not just what.

#### 4. Logic & Operations
File Collisions: If a file exists, append _[timestamp] to the new filename.
Simplicity: Choose the simplest working solution.

#### 5. Tooling Preference (Web)
Primary: browser_action (ALWAYS try this first).
Fallback: Other browser tools (Only if browser_action fails).

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

---

## Testing

### Python Script Execution
**Constraint:** Do not execute multi-line Python scripts directly in the terminal.

**Procedure for Multi-line Scripts:**
1) **Search:** Check codebase and memory for existing scripts.
2) **Evaluate:**
    - **Exact Match Found:** Execute the existing script.
    - **Similar Match Found:**
        - Analyze dependencies (what relies on this script?).
        - Determine strategy: Modify existing vs. Duplicate new.
        - Execute the modified or duplicated script.
    - **No Match:** Create a new script file, then execute it.

---

Here is the improved version, focusing on strict payload requirements and clear protocols:

## Mode Communication
**Mechanism:** Delegate tasks strictly via the `message` parameter.

**Payload Requirements:**
- **Context:** Include relevant bug/issue details. If a `plan` is active, include pertinent sections.
- **Instructions:** Provide specific, actionable implementation steps.
- **Completion Trigger:** Specify the exact command to return when the task is finished.

**Response Protocol:**
- Mandate a reply via the `result` parameter containing a concise summary of the outcome.

---

Here is the improved version, emphasizing mandatory checks and knowledge retention:

## Error Handling & QA
**Validation**
- **Immediate Check:** Inspect terminal output and VS Code Problems panel after *every* edit.
- **Fix First:** Resolve regressions or new errors before proceeding.

**Documentation**
- **Log Findings:** Append significant bugs, non-obvious fixes, or environment quirks to `.roo/docs/useful.md`.