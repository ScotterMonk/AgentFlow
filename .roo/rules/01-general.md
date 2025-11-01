# ALL MODES - IMPORTANT

## Environment & Commands
- Windows 11: Use PowerShell/Windows commands.
- Numbered instructions: Execute in order.
- Global commands:
    - "git update" → `/githubber` mode.
    - "run", "run app", "turn on app", "server on" → `python app.py`.
    - "activate" → `.\activate.ps1`.

## Critical Resources
- `app knowledge`: `@/agents.md`.
- Codebase: `codebase_search`, `read_file`, `search_files`.
- `short plan name`: yymmdd_two_word_description.
- `user_query` and `user query file`: `@\.roo\docs\plans\plan_[timestamp]_[short plan name]_user.md`.
- `plan file`: `@\.roo\docs\plans\plan_[short plan name].md`.
- `plan`: Version of `plan file` in memory.
- `log file`: `@\.roo\docs\plans\plan_[short plan name]_log.md`.
    Logging Format:
    `date + time; action summary` (semicolon separated).
    - Ex: `"2025-08-14 07:23; Approved to begin"`.
    - Ex: `"2025-08-14 07:25; Task completed: Added update_query() to utils_sql.py, refactored utils_sql.py, junk.py"`.
- Backups: `@\.roo\docs\old_versions/[file name]_[timestamp]`.
- `testing type`: "Run py scripts in terminal", "Use pytest", "Use browser", "Use all", "No testing", "Custom".
- `completed plans folder`: `@\.roo\docs\plans_completed`.
- Git diff, recent commits.
- `credentials`: `@\.env`. User passwords in DB is hashed.
- Web automation & browsing: `browser_action`
- Database: 
    - `@\.roo\rules\02-database.md`
    - [`database_schema.md`](.roo/docs/database_schema.md:1)
    - `@\utils\database.py`
    - `@\models\models_*.py`
    - `db = SQLAlchemy()`
	- db port = 5433
    - When creating a script to "check the database", write a temp .py file in the `@\temp` folder and run it. Do NOT paste the script into the terminal.
- `useful discoveries`: `@\.roo\docs\useful.md`.

### Modes
For analysis/plan formation, referencing in Task instructions, or to determine when to mode-switch:
- Planner - Architecting a `plan`, a 4-step process:
    - `/planner-a`: Planning 1 - create `phase(s)` from `user query`. Pass flow to `/planner-b`.
    - `/planner-b`: Planning 2 - refine output from `/planner-a`. Q/A. Pass flow to `/planner-c`.
    - `/planner-c`: Planning 3 - create `tasks` for each `phase`. Get user approval. Pass flow to `/planner-d`.
    - `/planner-d`: Planning 4 - Q/A. Get user approval. Pass flow to `/orchestrator`.
- `/orchestrator`: Execute approved `plan` by coordinating tasks across modes.
- `/code-monkey`: Coding, analysis, following instructions.
- `/code`: Complex coding, analysis, debugging.
- `/tester`: Testing.
- `/front-end`: Front-end.
- `/ask`: General Q/A.
- `/task-simple`: Small ops/tasks.
- `/githubber`: Use GitHub commands.
- `/debug`: Troubleshooting, investigating errors, or diagnosing problems.

## Standards

### Communication
Be brief; don't echo user requests.

### Modularization
CRITICAL: Keep Python and JS files small and modular, preferably less than 400 lines of code. 
Create and reference utility files (`@\utils`) liberally.

### Flask html templates
Use `jinja-html` language mode.

### Naming Conventions
- Use for naming folders, files, functions, variables, classes, db columns, etc.
    Pattern: {specific}_{domain} -> {domain}_{specific}
    Examples:
    - `admin_dashboard_utils.py`, `user_dashboard_utils.py` -> `dashboard_utils_admin.py`, `dashboard_utils_user.py`
    - `scott_utils.py`, `kim_utils.py` -> `utils_scott.py`, `utils_kim.py`
    - `scott_core_utils.py`, `kim_core_utils.py` -> `utils_scott_core.py`, `utils_kim_core.py`
    - `edit_user`, `add_user` -> `user_edit`, `user_add`
- Snake_case for functions, variables, database tables & columns.
- PascalCase for classes.

### Code Standards
- All functions/classes MUST include: `# [Created-or-Modified] by [LLM model] | yyyy-mm-dd_[iteration]`
- Templates use `jinja-html` language mode
- Compact vertical spacing.
- Multi-line strings for complex SQL queries.
- Prioritize readable code over compact syntax.
- Prioritize quotes over semi-quotes. Ex:
```python
fixed += "."
```
- Simple solutions.
- Preserve existing comments.
- Comment liberally.
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

#### File References
- Use back-ticks liberally: `filename.py`, `@\.roo\docs\file.md`
- Avoid brackets: `file.py` not `[file.py](path)`
- File paths with `@\` prefix for project root references

#### Formatting
- Use 4-space indentation for nested items.
- Numbered lists with `)` separator: `1)`, `2)`
- Avoid double-asterisks: "**Impact:**" -> "Impact:".
- Keep it small/no redundancy: [`models/models_user.py`](app/models/models_user.py) -> `models/models_user.py`.
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

## Default Workflow

### Initialization
1) Determine if this is a new `plan` or continuation. If unknown, examine files below to determine.
- `log file` (create new if needed):
	- If an existing log is non-empty or references a previous plan, move it to `completed plans folder`.
    - Log entries: `date + time; action summary`.
        - Ex: `"2025-08-14 07:23; Approved to begin"`.
        - Ex: `"2025-08-14 07:24; Task completed: Added update_query() to utils_sql.py, refactored utils_sql.py, junk.py"`.
2) Determine `short plan name` based on user query.
3) Save `user query` into `user query file`.
4) Create or modify `plan file`.
- If an existing plan is non-empty or from a past project, move it to `completed plans folder`.
- Create a fresh `plan file`.
For the following steps 5 through 6, be sure to determine these 2 settings as separate questions to user.
5) Project size/complexity?
    Hierarchy: `plan` can have one or more `phase(s)` and each `phase` has one or more `task(s)`.
    If new `plan`, IMPORTANT to offer user following choices:
    - "One Task (tiny or small project)"
    - "One Phase (small to medium project), one-or-many tasks"
    - "Multi-Phase (larger project), many tasks per phase"
6) FOLLOW THIS INSTRUCTION EXACTLY: SEPARATELY FROM size/complexity above and testing types below, Ask User: `autonomy level` for `plan`. Determine autonomy level separate from testing type below. Choices: "Low" (frequent direction), "Med", "High" (rare direction).
7) FOLLOW THIS INSTRUCTION EXACTLY: SEPARATELY from choices above, Ask User `testing type` for `plan`, Choices: "Run py scripts in terminal", "Use pytest", "Use browser", "Use all", "No testing", "Custom". Important: provide these exact choices to the user.
8) Understand the ask: Problem/feature, intent, scope, constraints, dependencies.

### Planning

#### 1 Pre-planning
1) Search for similar planning documents and architectural decisions.
2) Retrieve project history and previous relevant planning outcomes from memory.
3) Identify potential challenges based on past experiences.

#### 2 Create plan with detailed tasks
Notes:
- Incorporate (or not) testing into the plan based on user's `testing type` choice.
- Outline `task(s)`.
Steps:
1) Pull or create high level `plan file` into memory as `plan`.
2) Modify `plan` to have detailed task(s):
    - CRITICAL: Task structure. To prevent execution loop errors, tasks must follow these rules:
        - Each task = ONE atomic action only. Use "Action:" instead of "Steps:" to reinforce this. 
        - NO multi-step instructions within tasks.
        - Avoid numbered sub-steps within tasks.
        - NO complex dependencies between tasks.
        - Tasks should be self-contained and executable independently.
        - Real implementations only: Tasks should specify real functionality 
            (actual database calls, API integrations, etc.);
            no mock/simulated versions unless requested.
    - The following will be incorporated into tasks as information to be passed on to 
        specifid modes when orchestrator follows the `plan`:
        - Add mode hints, integration points, and acceptance criteria.
        - Identify existing related files, components, and utilities that can be copied,
            leveraged, or modified to be more general.
    - Take all the time necessary until you are confident you have come up with a 
        solid new `plan` that includes tasks. 
3) Open the new `plan file` in main editor window for user to easily edit and approve.
4) Brainstorm on the `plan_file` with user to resolve any questions, issues, or ambiguity.
    Loop through the following until you have a clear understanding of the user's need, ignoring `autonomy level`:
    - Keep in mind the values in `Critical Resources`;
    - Ask clarifying questions of user.
    - Modify the `plan file` as changes occur.
5) Finalize the `plan`:
    - Important: take your time to think it through carefully (depth/persistence NOT depending on `autonomy level`). 
    - Take all the time necessary until you are confident you have come up with a solid `plan` to show user.
    - Do not offer a time estimate.
6) Open the new `plan file` in main editor window for user to easily edit and approve.
7) Get `plan` approval.
    Loop through until user approves:
    - Brainstorm with user: refine and converge on the final approved `plan`.
    - End loop when "'Approve and Start Work' or 'Modify Plan'" yields "Approve and Start Work".
8) Get `plan` approval.

Loop through until user approves:
- Brainstorm with user: refine and converge on the final approved `plan`.
- End loop when "Approve and Start Work or Modify Plan" yields "Approve and Start Work".
1) Do the work.
2) QA
- Resolve VS Code Problems.
- Use `codebase_search` for impact analysis.
- Call `/tester` mode when needed, but not if `testing type` is "No testing".
- Document `useful discoveries`, including any new patterns or best practices discovered.
3)  Completion
- Update `log file`, `plan file`.
- User confirmation: user satisfied or has additional instructions.
- Archive completed plan/log files to `\plans_completed\`. Append "_[iteration]" if collision.
4)  Continuous Learning Protocol.
- Analyze what worked well and what could be improved.
- Store successful approaches and solutions in memory.
- Update memory with lessons learned from the work.
- Identify areas where additional codebase exploration might be beneficial.

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

### Browser Testing (web automation / browsing)
See `@/agents.md` for browser use procedures.

## Mode Communication
Delegating via `message` param and include:
- If using `plan`: Relevant `plan` details.
- Relevant bug/issue details.
- Implementation instructions.
- Return command when complete.
- Reply requirement via `result` param with outcome summary.

## Error Handling and QA
- Verify console and VS Code Problems panel after changes
- Document notable findings in `/.roo/docs/useful.md` (see Documentation in `@/agents.md`
