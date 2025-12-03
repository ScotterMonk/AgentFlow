# ALL MODES - IMPORTANT

## Environment & Commands
- Windows 11: Use PowerShell/Windows commands.
- For numbered instructions: Execute in exact order.

## Critical Resources

### Sources of knowledge
- App knowledge: `agents.md`.
    From `agents.md`:
    a) Environment & Run Commands.
    b) Critical Non-Standard Patterns.
    c) Documentation.
    d) External API Provider Framework.
    e) Configuration.
    f) Testing Guidance.
- Codebase: `codebase_search`, `read_file`, `search_files`.
- Git diff, recent commits.
- `credentials` for everything: `.env`.

### Database
See `.roo/rules/02-database.md` for all database procedures.

### Other
- Web automation & browsing: `browser_action`
- Make use of and contribute to Useful Discoveries: `.roo/docs/useful.md`.

### Modes
For analysis/plan formation, referencing in Task instructions, or to determine when to mode-switch:
- `/architect` (Planner-simple): Architecting a `plan` by creating `phase(s)` and `task(s)` from `user query`. Q/A. Get user approval. Pass flow to `/orchestrator`.
- `/planner-a` (Planner-complex): Architecting a `plan` using a 3-step process:
    - `/planner-a`: Planning stage 1 - create `phase(s)` from `user query`. Brainstorm with user. Pass flow to `/planner-b`.
    - `/planner-b`: Planning stage 2 - create detailed `tasks` for each `phase`. Get user approval. Pass flow to `/planner-c`.
    - `/planner-c`: Planning stage 3 - Q/A. Get user approval. Finalize `plan`. Pass flow to `/orchestrator`.
- `/orchestrator`: Execute approved `plan` by coordinating tasks across modes.
- `/code-monkey`: Coding, analysis, following instructions.
- `/code`: Complex coding, analysis, debugging.
- `/tester`: Testing.
- `/front-end`: Front-end.
- `/ask`: General Q/A.
- `/task-simple`: Small ops/tasks.
- `/githubber`: Use GitHub commands.
- `/debug`: Troubleshooting, investigating errors, or diagnosing problems.

### Best mode for job
If another mode is more appropriate for your task, pass task and appropriate parameters (concise WTS) on to appropriate one. 
Prefer the most budget-friendly modes in the following order of low-to-high budget sorting.
Budget/Intelligence/Skill:
    a) low (ex: renaming, copying, moving files; doing simple text/value comparison or replacement, copying column names and column parameters from a database): `/task-simple`.
    b) med (ex: refactoring, simple function creation/modification, and writing): `/code-monkey`, `/tester`.
    c) high (ex: complex function modification and writing or failure of med skill modes): `/code`.
    d) higher (ex: complex function modification and writing or failure of high skill modes): `/debug`.
If front-end task with medium or high complexity, use `/front-end`.

## Standards

### Communication
Be brief; don't echo user requests.

### Modularization
CRITICAL: Keep Python and JS files small and modular, prefer less than 400 lines of code. 
Create and reference utility files (`utils/`) liberally.

### Simplification
Reference `.roo/docs/simplification.md` when:
- Implementing similar functionality multiple ways
- Accumulating special case handling
- Complexity spiraling in a module
Look for the unifying principle that eliminates multiple components.

### Flask html templates
When you modify any .html file:
If it is a Flask template, use VS Code's `jinja-html` language mode.
After editing and saving a jinja-html .html file, VS Code tends to change the language mode for that file to "html". Fix by setting language mode to `jinja-html`.

### Naming conventions
Rationale: Domain-first naming groups related code, improves IDE autocomplete, and makes file navigation logical.
Pattern: {specific}_{domain} → {domain}_{specific}
Definitions:
- Domain: Core subject area (user, dashboard, config, sync, auth, billing)
- Specific: Qualifier or action (admin, scott, core, edit, add, delete, list)
Case Rules:
- Files, functions, variables, DB tables/columns: snake_case
- Classes: PascalCase
Examples by Type:
Files:
- `admin_dashboard_utils.py` → `dashboard_utils_admin.py`
- `scott_core_utils.py` → `utils_scott_core.py`
Functions/Variables:
- `edit_user` → `user_edit`
- `add_user` → `user_add`
Classes:
- `AdminPerson` → `PersonAdmin` or even better -> `Person` with type parameter set to "admin"
- `ResellerPerson` -> `PersonReseller` or even better -> `Person` with type parameter set to "reseller"
Do NOT rename without approval:
- Public APIs (HTTP routes, library functions, CLI flags)
- Database tables/columns (requires migration)
- Standard Python patterns (`__init__.py`, `setUp()`)
- Framework conventions (Django's `settings.py`)
Prefer to:
- Apply to new code always
- Refactor internal names when editing that code
- Keep tests/usage in sync
Decision checklist:
1) Public API or DB? → Get approval first
2) Follows {specific}_{domain}? → Needs change
3) Actively editing file? → Good time to rename
4) Can identify domain/specific? → Proceed; otherwise ask
Edge cases:
- Multiple words: Use underscores (`utils_admin_user_profile.py`)
- Ambiguous: Ask user or use most specific grouping
CRITICAL: When renaming, refactor all references (imports, calls, docs, tests)
After renaming, verify:
- All imports updated
- All function calls updated
- Tests still pass
- Documentation references updated
- No VS Code Problems panel errors

### Code standards
- All functions/classes MUST include: `# [Created-or-Modified] by [LLM model ("GPT-5.1", "Grok-4-fast", "Sonnet 4.5", etc)] | yyyy-mm-dd_[iteration]`
- Templates use `jinja-html` language mode
- Compact vertical spacing.
- Multi-line strings for complex SQL queries.
- Prioritize readable code over compact syntax.
- Prioritize quotes over semi-quotes. Ex:
```python
fixed += "."
```
- Simple solutions.
- Prefer: Preserve existing comments.
- CRITICAL: Comment liberally.
- File operations
    - On name collisions, append _[timestamp].
- Tool preference for web:
    - Default: `browser_action`.
    - Fallback: Use any other browser tooling only if `browser_action` is unavailable or misconfigured.

### Markdown syntax

#### Vertical Spacing
- Minimal empty lines between sections
- No empty lines between related list items
- Headers immediately followed by content
- Single empty line between major sections only

#### References (file and otherwise)
Goal is to reduce size and simplify:
- Avoid brackets and parens, prefer succinct, no redundancy, no line numbers. 
Examples:
- [`models/models_user.py`](app/models/models_user.py) -> `models/models_user.py`.
- [`models/models_user.py`](app/models/models_user.py:22) -> `models/models_user.py`.
- See [`.roo/rules/01-general.md`](`.roo/rules/01-general.md:11`) -> See `Critical Resources` section in `.roo/rules/01-general.md`.

#### Formatting
- Use 4-space indentation for nested items.
- Numbered lists with `)` separator: `1)`, `2)`
- Avoid double-asterisks: "**Impact:**" -> "Impact:".
- Use colons for emphasis instead of bold.
- Back-ticks for code/file references, not brackets.
- Simple, direct formatting.
- Compact bullet points without extra spacing.
- Related items grouped tightly.
- Clear section breaks with single empty line.
- Immediate content after headers.

#### Examples
Good:
```
## Section
Content immediately follows.
- Item one
- Item two
- Item three
```

Avoid:
```
## Section

Content with extra spacing.

- Item one

- Item two
```

## Testing

### Running python scripts in terminal
Never run py scripts longer than one line in terminal.
With python scripts longer than a line:
1) Search codebase and memory to determine if exact or similar script already exists.
    (a) Exact one exists: Use the script.
    (b) Similar one exists: 
        - Find what other objects depend on the script.
        - Decide if modification or duplication is better.
        - Modify or duplicate.
2) Run the script.

## Mode Communication
Delegating via `message` param and include:
- If using `plan`: Relevant `plan` details.
- Relevant bug/issue details.
- Implementation instructions.
- Return command when complete.
- Reply requirement via `result` param with outcome summary.

## Error Handling and QA
- Verify console and VS Code Problems panel after changes
- Document notable findings in `.roo/docs/useful.md`
