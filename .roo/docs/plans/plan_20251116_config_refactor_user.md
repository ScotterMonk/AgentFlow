# User Query - Config Refactoring

Make a plan that consists of:
1) Examine 'config.txt'. Notice the following 4 params: 
   - include_roo_only=true (obsolete)
   - root_allowlist=.roomodes
   - include_roomodes=true (obsolete)
   - ignore_patterns=.git,__pycache__,.venv,.idea,.vscode,node_modules,*.pyc,database_schema.md,useful.md

2) Notice how the application uses those params.

3) Let's make include_roo_only and include_roomodes obsolete from app, removing them from app use, making these behaviors governed by the following 2 params:
   - param 1: root_allowlist=.roomodes (verify this can have more values, comma separated)
   - param 2: ignore_patterns=.git,__pycache__,.venv,.idea,.vscode,node_modules,*.pyc,database_schema.md,useful.md

4) Verify both of those 2 params allow for their comma-separation to be "," or ", " and defaulting to ", " for writing from app.