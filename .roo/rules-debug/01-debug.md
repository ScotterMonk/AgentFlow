# Debugger Mode

Depending on complexity of the issue, pass the issue on to one of the following:
- `/code`: Complex coding, analysis, some planning.
- `/code-monkey`: Coding, analysis, following instructions.
- `/tester`: Testing.
- `/front-end`: Front-end.
- `/ask`: General Q/A.
- `/task-simple`: Small ops/tasks.
- `/githubber`: Use GitHub commands.

CRITICAL:
- Be sure to use all applicable values from `@\.roo\rules\01-general.md`. 
    Follow those instructions explicitly, especially regarding:
    - `autonomy level`. If unknown, *ask user*.
    - and separate dialog: `testing type`. If unknown, *ask user*.
- `log file`.
- Backup files before edits.
- If database operations, refer to `@\.roo\rules\02-database.md`.

## Critical Resources
Use these resources thoroughly to understand expected behavior and existing patterns before acting. 
See `Critical Resources` section in `@\.roo\rules\01-general.md`.

## Standards
See `Standards` section in `@\.roo\rules\01-general.md`.
- Use for naming folders, files, functions, variables, classes, db columns, etc.
    Pattern: {specific}_{domain} -> {domain}_{specific}
    Examples:
    - scott_utils.py, kim_utils.py -> utils_scott.py, utils_kim.py
    - scott_core_utils.py, kim_core_utils.py -> utils_scott_core.py, utils_kim_core.py
    - app_analysis.md, db_analysis.md -> agents.md, analysis_db.md
    - edit_user, add_user -> user_edit, user_add

## Systematic Debugging Process (in order)
- Gather context: Use `codebase_search` to understand related code and recent changes;
- Reproduce issue: Switch to `/code` mode for file reading, browser testing, or database access as needed;
- Form hypothesis: Reflect on 5-7 possible problem sources, distill to 1-3 most likely;
- Add targeted logging: Insert debug statements to validate assumptions;
- Confirm diagnosis: Present findings to user before implementing fix;
- Create backup: Save current state before making changes.

## Code Analysis & Investigation
- Search for similar functions and patterns using `codebase_search`;
- Look for recent changes that might have introduced the issue;
- Identify dependencies and integration points that could be causing problems.

## Quality Assurance
- Check VS Code Problems panel after changes;
- Don't assume changes work until user confirms testing;
- Call tester mode with specific test scenarios via `message` parameter, requesting reply via `result` parameter with thorough outcome summary;
- Use `codebase_search` to verify impact on other code areas.
- Document `useful discoveries`.

## Troubleshooting

### Running python scripts in terminal
With python scripts longer than a line or 2 that you might run in terminal, instead write them into a temporary .py file and run that file.

### If stuck in loop
Pass task to `/code` mode.