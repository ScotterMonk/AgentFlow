# Planning

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
- Credentials for everything: `.env`.
- Database: `.roo/rules/02-database.md` for all database procedures.

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

### Mode selection strategy
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
    - CRITICAL: At start of `phase` instructions, put "Backup [files in this phase that will be changed] to `.roo/docs/old_versions/[file name]_[timestamp]`" into `plan`.
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
    - Incorporate testing into the plan based on user's `testing type` choice.
    - If creating tests: First be sure test does not already exist.
    - Remember you are creating a plan for another mode to build, not building.
    - Use `Sources of knowledge` to check if proposed functionality already exists.
    - Explicitely add refactoring to appropriate stages as tasks.
    - For all of the following, keep in mind the values and guidelines in `Critical Resources` and `Standards`.
    - You MUST complete each step below before proceeding to the next.
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
            - Look in `utils/` and `utils_db\` folders for similar or same functionality.
        - Add mode hints, integration points, and acceptance criteria.
		- Q/A mode hints. 
            CRITICAL that this is done accurately. Consult user if unsure which mode to assign for a task.
            Prefer the most budget-friendly modes in the following order of low-to-high budget sorting:
            See `Mode selection strategy` above.
		- Task structure example (Follow this format exactly):
			```markdown
			[High level description of goal.]
			- Task 01: [Task description.]
				Mode hint: /task-simple. Pass `path` param
				[Notes relevant to this task.]
				[Potential code or pseudocode.]
				[Potential instructions to test.]
                CRITICAL: Log your progress to [`log file`].
			- Task 02: [Task description.]
				Mode hint: /code-monkey.
				[Notes relevant to this task.]
				[Potential code or pseudocode.]
   				[Potential instructions to test.]
                CRITICAL: Log your progress to [`log file`].
			```
            Include pseudo-code or code where appropriate to clarify concepts and create ease/efficiency for worker.
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
