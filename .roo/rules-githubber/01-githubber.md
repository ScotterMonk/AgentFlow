# Githubber Mode

When in this mode, the following commands will run the processes below:
- "update": Stage, commit, and push all changes to the remote repository.
- "create issue": Create a new GitHub issue with a title and body provided by the user.
- "create branch": Create a new branch with a name provided by the user.
- "checkout branch": Switch to an existing branch with a name provided by the user.
- "list branches": List all branches in the repository.
- "status": Show current git status.
- "log": Show recent git commit history.
- "branch": Show current branch name.
- "revert": Revert a specific commit by its hash, provided by the user.

## Keep responses concise
- Do not share what your to-do list or plan is. Just do it.
- No need for anything like, "Now I need to..." or "Now I will..."
- Only feedback to user is at the end of the following tasks, except item 5 below, or if problems.

## Use terminal window
- Note: This is Windows PowerShell within `VS Code`; using `SSH`.

## Research
**Determine what was changed**
The commit message should be more than just the file names that were changed.
Sculpt a useful commit message, using as needed:
- `codebase_search`
- `read_file`
- `search_files`

## Update: Stage, Commit, and Push Git Changes
**Carefully follow** all of the following steps:
1) **Errors**: Provide troubleshooting if any step encounters errors.
2) **Examine** repository's current status, showing all modified, untracked, and staged files
3) **Stage all changes**: Handle special cases as needed. **Do not ask user for permission to run this command**. Run the command.
4) **Commit message**: Craft a meaningful commit message that follows best practices:
   - Concise subject line.
   - Detailed body (keep it short as possible while not leaving out things that were done).
   - Using a Windows PowerShell terminal.
   - Make sure the entire message is passed as a single argument to -m by enclosing it in quotes.
   - Include file paths for all changed files.
   - Escape anything in the commit message that may be interpreted as a file path.
5) **Commit**: **Do not ask user for permission to run this command**. Run the command. 
   **You have permission** to run any variation of `git commit`, including `git commit -m "[commit message here]"` without asking user for permission.
6) **Verify** the commit was successful and show its hash/details.
7) **Push changes** to the remote repository on current branch. **Do not ask user for permission to run this command**. Run the command. 
   Pay attention to the terminal where it may ask you for a password. 
   If so, get that password using your project knowledge; it may be referenced via the `Critical Resources` section in `.roo/rules/01-general.md`.
8) **Confirm** the synchronization status between local and remote repositories.
9)  **Virtual environment**: If environment has become deactivated: `./activate` in terminal.