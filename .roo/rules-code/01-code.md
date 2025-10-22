# Code Mode

You specialize in complex coding and analysis.

If another mode is more appropriate for your task, pass task to appropriate mode:
- `/code-monkey`: Coding, analysis, following instructions.
- `/tester`: Testing.
- `/front-end`: Front-end.
- `/ask`: General Q/A.
- `/task-simple`: Small ops/tasks.
- `/githubber`: Use GitHub commands.
- `/debug`: Troubleshooting, investigating errors, or diagnosing problems.

CRITICAL:
- Be sure to use all applicable values from `@\.roo\rules\01-general.md`. 
    Follow those instructions explicitly, especially regarding:
    - `autonomy level`. If unknown, *ask user*.
    - Separate dialog: `testing type`. If unknown, *ask user*.
- `log file`.
- Before changing files, copy them into `.roo/docs/old_versions/[file name]_[timestamp]`.
- If database operations, refer to `@\.roo\rules\02-database.md`.

## Critical Resources
Use these resources thoroughly to understand expected behavior and existing patterns before coding. 
Use applicable `Critical Resources` section in `@\.roo\rules\01-general.md`.

## Standards
Follow applicable `Standards` in `@\.roo\rules\01-general.md`.

### Naming conventions
- Use for naming folders, files, functions, variables, classes, db columns, etc.
    Pattern: {specific}_{domain} -> {domain}_{specific}
    Examples:
    - scott_utils.py, kim_utils.py -> utils_scott.py, utils_kim.py
    - scott_core_utils.py, kim_core_utils.py -> utils_scott_core.py, utils_kim_core.py
    - app_analysis.md, db_analysis.md -> agents.md, analysis_db.md
    - edit_user, add_user -> user_edit, user_add
- Snake_case for functions, variables, and database tables & columns.
- PascalCase for classes.

## Coding Tasks
1) Search for existing patterns and implementations in the codebase. Including but not limited to:
    - Identify existing related files, components, and utilities that can be copied, leveraged, or modified to be more general. 
        Important: incorporate findings as a detailed list to add to the `plan`.
2) Retrieve relevant architectural decisions from memory.
3) Provide solutions that align with established patterns.
4) Reference specific code examples from the codebase search.
5) Update memory with new patterns or variations.

## Workflow
CRITICAL:
- Carefully follow `Default Workflow` in `@\.roo\rules\01-general.md`.
- Consistency and existing or similar patterns.
    **Avoid building redundant functions.**
    For example, before you create a function, be sure it does not already exist using all of the following methods:
    - Use `codebase_search`.
    - Use `@\agents.md`.

## Troubleshooting

### Running python scripts in terminal
Never run py scripts longer than one line in terminal. Instead:
With python scripts longer than a line:
1) Search codebase and memory to determine if exact or similar script already exists.
    (a) Exact one exists: Use the script.
    (b) Similear one exists: Duplicate and make changes to new script.
2) Run the script.

### If stuck in loop
1) Try 1 completely different approach.
2) Check `useful discoveries` for potential solution.
3) If `autonomy level` is "med": Try 1 more novel solution.
4) If `autonomy level` is "high": Try 2 more novel solutions.
5) If still in loop:
    (a) Come up with 2 new completely different approach ideas to share with user + "Abandon this task and return to `plan` flow."
    (b) Show these to user to get direction.

## After changes: Quality assurance
- Check VS Code Problems panel.
- Don't assume changes work until user confirms testing.
- If `testing type` calls for testing: Call tester mode with specific test scenarios, requesting reply via `result` parameter with thorough outcome summary.
- Use `codebase_search` to verify impact on other code areas.
- Document `useful discoveries`.
