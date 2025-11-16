# ALL MODES - IMPORTANT

## Environment & Commands
- Windows 11: Use PowerShell/Windows commands.
- Numbered instructions: Execute in order.
- Global commands:
    - "git update" → `/githubber` mode.
    - "run", "run app", "turn on app", "server on" → `python app.py`.
    - "activate" → `./activate.ps1`.

## Critical Resources

### Sources of knowledge
- `app knowledge`: `agents.md`.
- Codebase: `codebase_search`, `read_file`, `search_files`.
- Git diff, recent commits.
- `credentials` for everything: `.env`. User passwords in DB are hashed.
- Database: see below.

### Planning
`plan values` to fill/use:
- `short plan name`: yymmdd_two_word_description.
- `user_query` and `user query file`: `.roo/docs/plans/plan_[timestamp]_[short plan name]_user.md`.
- `plan file`: `.roo/docs/plans/plan_[short plan name].md`.
- `plan`: Version of `plan file` in memory.
- `log file`: `.roo/docs/plans/plan_[short plan name]_log.md`.
    Logging Format:
    `date + time; action summary` (semicolon separated).
    - Ex: `"2025-08-14 07:23; Approved to begin"`.
    - Ex: `"2025-08-14 07:25; Task completed: Added update_query() to utils_sql.py, refactored utils_sql.py, junk.py"`.
- Backups: `.roo/docs/old_versions/[file name]_[timestamp]`.
- `testing type`: "Run py scripts in terminal", "Use pytest", "Use browser", "Use all", "No testing", "Custom".
- `completed plans folder`: `.roo/docs/plans_completed`.

### Database
See `.roo/rules/02-database.md` for all database procedures.

### Other
- Web automation & browsing: `browser_action`
- Make use of Useful Discoveries: `.roo/docs/useful.md`.

### Modes
For analysis/plan formation, referencing in Task instructions, or to determine when to mode-switch:
- Planner - Architecting a `plan`, a 4-step process:
    - `/planner-a`: Planning stage 1 - create `phase(s)` from `user query`. Pass flow to `/planner-b`.
    - `/planner-b`: Planning stage 2 - refine output from `/planner-a`. Q/A. Pass flow to `/planner-c`.
    - `/planner-c`: Planning stage 3 - create `tasks` for each `phase`. Get user approval. Pass flow to `/planner-d`.
    - `/planner-d`: Planning stage 4 - Q/A. Get user approval. Pass flow to `/orchestrator`.
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
If front-end task, use `/front-end`.

## Standards

### Communication
Be brief; don't echo user requests.

### Modularization
CRITICAL: Keep Python and JS files small and modular, preferably less than 400 lines of code. 
Create and reference utility files (`utils/`) liberally.

### Simplification
Reference `.roo/docs/simplification.md` when:
- Implementing similar functionality multiple ways
- Accumulating special case handling
- Complexity spiraling in a module
Look for the unifying principle that eliminates multiple components.

### Flask html templates
Use `jinja-html` language mode.

### Naming Conventions
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
- `AdminPerson` → `PersonAdmin`
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
- Simplify; avoid brackets and keep succinct: [`utils_db/media_utils.py`](utils_db/media_utils.py:1) -> `utils_db/media_utils.py`.

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

Do in order, skip none:

### 1 Input
From user:
- store as `user query`.

### 2: Initialization
Remember you are planning, not building.
Do not skip any of the following steps. Follow each one in order.
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
    `plan` can have one or more `phase(s)` and each `phase` has one or more `task(s)`.
    If new `plan`, IMPORTANT to offer user following choices:
    - "One Phase (tiny or small project), one or few tasks"
    - "One Phase (small to medium project), one or many tasks"
    - "Few Phases (medium project), many tasks"
    - "Multi-Phase (larger project), many tasks per phase"
6) FOLLOW THIS INSTRUCTION EXACTLY: SEPARATELY FROM size/complexity above and testing types below, Ask User: `autonomy level` for `plan`. Determine autonomy level separate from testing type below. Choices: "Low" (frequent direction), "Med", "High" (rare direction).
7) FOLLOW THIS INSTRUCTION EXACTLY: SEPARATELY from choices above, Ask User `testing type` for `plan`, Choices: "Run py scripts in terminal", "Use pytest", "Use browser", "Use all", "No testing", "Custom". Important: provide these exact choices to the user.
8) Understand the ask: Problem/feature, intent, scope, constraints, dependencies.

### 3: Pre-planning
1) Search for similar planning documents and architectural decisions.
2) Retrieve project history and previous relevant planning outcomes from memory.
3) Identify potential challenges based on past experiences.

### 4: Understand user need
1) Understand user's need.
    Draft a high level pre-plan based on `user query` with no tasks yet:
    Take your time to brainstorm with user and think through the `user query` carefully. 
    - Resolve contradictions, errors in logic, and ambiguity to increase clarity.
    - Ask clarifying questions of user.
    - Take all the time necessary until you are confident you have a solid understanding of the `user query`. 
2) Save progress:
    Save this beginning stage of the `plan`
    (succinctly describing `user query` and succinct description of solution) 
    to a new `plan file`.

### 5: Create plan phase(s)
Notes:
- Outline `phase(s)`, depending on user's "one-phase or multi-phase" choice above.
You MUST complete each step below before proceeding to the next.
Steps:
1) Add `phase(s)` to `plan`.
    Draft a high level `plan` based on `user query` with no tasks yet:
    - Real implementations only: Phases should specify real functionality (actual database calls, API integrations, etc.); 
        no mock/simulated versions unless requested.
    - Identify existing functionality that can be copied, leveraged, or modified to be more general. 
3) Think through the draft `plan`, step-by-step, looking specifically for ways it could be improved.
    Loop through each `phase` to:
    - Explore relevant values in `Critical Resources`;
    - Ask clarifying questions of user.
    - Move on when you have full confidence.
    Modify the `plan file` when you are confident in the draft high level `plan`.
4) Open the `plan file` in main editor window for user to easily edit and approve:
    Brainstorm on the `plan` with user to resolve any questions, issues, or ambiguity.
    - Modify the `plan file` as changes occur.
5) Finalize the high level `plan` (no tasks yet):
    - Important: think it through carefully. 
    - Take all the time necessary until you are confident you have come up with a solid high level `plan`.
    - Do not offer a time estimate.
6) Modify the `plan file` to be in sync with latest `plan`.
7) Open the `plan file` in main editor window for user to easily edit and approve.
    Loop through until user approves:
    - Brainstorm with user: refine and converge on the final approved high level `plan`.
    - End loop when "'Approve and pass to next planner level' or 'Modify this high level plan'" yields "Approve and pass to next planner level".

### 6: Add detailed tasks
Notes:
    - Incorporate (or not) testing into the plan based on user's `testing type` choice.
    - If creating tests: First be sure test does not already exist.
    - Remember you are creating a plan for another mode to build, not building.
    - Use `Sources of knowledge` to check if proposed functionality already exists.
    - Explicitely add refactoring to appropriate stages as tasks.
You MUST complete each step below before proceeding to the next.
- Take all the time necessary until you are confident each task meets all task criteria detailed below.
Steps:
1) Modify `plan` to have detailed `task(s)`:
    - Real implementations only: Tasks should specify real functionality 
        (actual database calls, API integrations, etc.); no mock/simulated versions unless requested.
    - CRITICAL: Task structure. Tasks must follow these rules:
        - Each task = ONE atomic action only. Use "Action:" instead of "Steps:" to reinforce this. 
        - NO multi-step instructions within tasks.
        - Avoid numbered sub-steps within tasks.
        - NO complex dependencies between tasks.
        - Tasks must be self-contained and executable independently.
        - **Avoid building redundant functions.**
            Search codebase and memory to determine if exact OR SIMILAR script already exists.
            Use existing related files, components, and utilities that can be leveraged or modified to be more general.
            For example, before you create a function or class, make sure it does not already exist.
			Use all of the following methods:
            - Use `codebase_search`.
            - Use `agents.md`.
        - Add mode hints, integration points, and acceptance criteria.
		- Q/A mode hints. 
            CRITICAL that this is done accurately. Consult user if unsure which mode to assign for a task.
            Prefer the most budget-friendly modes in the following order of low-to-high budget sorting:
            See `Best mode for job` above.
		- Task structure example:
			```md
			[High level description of goal for the plan.]
			[Some notes.]
			- Task 01: [Task description.]
				Mode hint: /task-simple.
				[Notes relevant to this task.]
				[Potential code or pseudocode.]
				[Potential test.]
			- Task 02: [Task description.]
				Mode hint: /code-monkey.
				[Notes relevant to this task.]
				[Potential code or pseudocode.]
				[Potential test.]
			```
        - Include pseudo-code or code where appropriate to clarify concepts and create ease/efficiency for worker.
2) Open the new `plan file` in main editor window for user to easily examine/edit.
3) Brainstorm on the `plan` with user to resolve any questions, issues, or ambiguity.
    Loop through the following until you have a clear understanding of the user's need (keeping aware of `autonomy level`):
    - Explore values in `Critical Resources & Standards`;
    - Ask clarifying questions of user.
    - Modify the `plan file` and `log file` as changes occur.

### 7: Refine the plan
Loop through until user approves:
Notes:
- Brainstorm with user: refine and converge on the final approved `plan`.
- End loop when "Approve and Start Work or Modify Plan" yields "Approve and Start Work".
- Follow each step below in order, with precision, skip none.
1) Do the work.
2) QA
- Resolve VS Code Problems.
- Use `codebase_search` for impact analysis.
- Call `/tester` mode when needed, but not if `testing type` is "No testing".
- Document `useful discoveries`, including any new patterns or best practices discovered.
3)  Completion
- Update `log file`, `plan file`.
- User confirmation: user satisfied or has additional instructions.
- Archive completed plan/log files to `.roo/docs/plans_completed/`. Append "_[iteration]" if collision.
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
See `agents.md` for browser use procedures.

## Mode Communication
Delegating via `message` param and include:
- If using `plan`: Relevant `plan` details.
- Relevant bug/issue details.
- Implementation instructions.
- Return command when complete.
- Reply requirement via `result` param with outcome summary.

## Error Handling and QA
- Verify console and VS Code Problems panel after changes
- Document notable findings in `.roo/docs/useful.md` (see Documentation in `agents.md`
