# Custom Instructions

Your customizable AI coding team!
Use it to create apps or make changes/additions to existing ones. 

This set of instructions (markdown files) enhances and extends the modes/agents that come with many coding agents/asisstants (or make your own). The instructions are tailored to work with Roo Code (free highly customizable VS Code extension) but will work with many others, including Github Copilot and CLine.

Using the built-in-to-Roo ability to use rules files, this archive is a set of custom instructions for the built-in modes and some new ones, including:
- Supercharged alternative to "Architect": a 4-step "Planner" process (planner-a, planner-b, planner-c, planner-d).
- Modified Architect mode to be more detailed and for smaller tasks than full on "Planner" process.
- Designed both Architect and Planner modes  to "front load" spend on high "intelligence" thinking models to create a plan that is so detailed, the "Workers" like "Code", "Code Monkey", etc. can be faster/cheaper models. Overall, I'm finding this method burns far less tokens, has far less errors, and runs longer without human intervention.
- Supplemented "Code" with a tightly controlled budget-friendly "Code Monkey" created to work with the short, detailed tasks created for it by Planner.
- Added "Front-end", "Debugger", "Tester", "GitHubber", "Docs Writer", etc.
- While planning and while working, creates detailed files to keep track of its goals, progress, and lessons learned.

Notes: 
- This set of instructions is ever-evolving. 
- The author, Scott Howard Swain, is always eager to hear ideas to improve this.

## When/how to use?

### Building a new app
If building a new app, it assumes you already know *specs* (what platform, language(s), database type, etc.) for the project. 
That's just one layer "higher" than these instructions are built for.
Possibly coming soon: a level above "Planner" where you brainstorm on a high level to get ideas for *specs* to feed planner.
Until then, use "Ask" mode or query your favorite LLM chat to help you sculpt your *specs*.

### Use cases for modifying your existing app

#### Example of small modification
Scenario: Fixing a bug, modifying front-end, or adding a function.
- Use "code", "code monkey", "front-end", "debug", "tester", etc., as appropriate.

#### Example of large/medium modification
Scenario: Building a new dashboard screen from scratch.
- Start with "planner-a" mode. For this mode, I choose a model with high reasoning and large-as-possible context window.
- Tell it what you want.
- It will brainstorm with you, asking questions, including:
    - How do you want the work plan to be structured in terms of phase(s) and task(s)?
        - It will automatically create tasks so they are "bite-size" chunks so you can use a less smart/lower-cost LLM model for the actual work.
    - What level of autonomy do you want it to have when it starts the work?
    - What type of testing (browser, pytest, custom, none) do you want it to do as it completes tasks?
- It will create a high level plan and ask you if you want to modify it or approve.
- It will also create plan and log files to help itself and you keep track of goals, progress, and lessons learned.
- Once you approve the plan, it will pass on to the other planner modes to flesh out and add detail to the plan.
- Eventually, once you approve, it will pass the plan (with detailed instructions, mode hints, etc.) on to the "orchestrator" mode.
- Note: This workflow sets the plan to prefer "code monkey" mode (lower budget than "code" mode) for the coding parts. If "code monkey" gets confused because a task is too difficult or complex, it has instructions to pass the task on to "code" mode which I assign a "smarter" LLM to.

## Folder structure

These files should go in your project root. You'll see they coincide with where your current .roo folder is.

```
app
├── agents.md
└── .roo
    ├── docs
    │   ├── database_schema.md
    │   ├── sharing.md
    │   ├── useful.md
    │   ├── old_versions
    │   ├── plans
    │   └── plans_completed
    ├── rules
    │   ├── 01-general.md
    │   └── 02-database.md
    ├── rules-architect
    │   └── 01-architect.md
    ├── rules-ask
    │   ├── 01-ask.md
    │   ├── 02-ask-health.md
    │   └── 03-ask-flora-growing.md
    ├── rules-code
    │   └── 01-code.md
    ├── rules-code-monkey
    │   └── 01-code-monkey.md
    ├── rules-debug
    │   └── 01-debug.md
    ├── rules-docs-writer
    │   └── 01-docs-writer.md
    ├── rules-front-end
    │   └── 01-front-end.md
    ├── rules-githubber
    │   └── 01-githubber.md
    ├── rules-orchestrator
    │   └── 01-orchestrator.md
    ├── rules-planner-a
    │   └── 01-planner-a.md
    ├── rules-planner-b
    │   └── 01-planner-b.md
    ├── rules-planner-c
    │   └── 01-planner-c.md
    ├── rules-planner-d
    │   └── 01-planner-d.md
    ├── rules-project-mgr
    │   └── 01-project-mgr.md
    ├── rules-task-simple
    │   └── 01-task-simple.md
    └── rules-tester
        └── 01-tester.md
```

## Agentflow File Sync Utility

A Python utility for synchronizing `.roo` directories across multiple project folders based on file modification times.

### Overview
The Agentflow File Sync Utility scans `.roo` subdirectories in multiple project folders, identifies files that need updating based on modification times, and performs intelligent file synchronization with atomic operations and backup support.

### GUI Usage
Launch the graphical interface with:
```
python main_gui.py
```

Use the interface to:
- Select multiple folders containing `.roo` directories
- Configure sync settings via the Settings window (dry-run mode, backup options)
- Monitor live progress during synchronization
- Overwrite preview panel that shows planned overwrites before execution.
- Favorite folder sets (based on folders_faves in config) to quickly re-load common project combinations.

### CLI Usage
Run headless synchronization with:
```
python cli_sync.py <folder1> <folder2> ...
```

Example:
```
python cli_sync.py /path/to/project1 /path/to/project2 /path/to/project3
```

### Configuration
Settings are stored in `config.txt` with options for:
- `dry_run`: Enable/disable dry-run mode
- `backup_mode`: Configure backup behavior (none, timestamped)

## Fit to you
Be sure to modify the content of files you see in the .roo/docs folder to fit your project. Especially:
- "agents.md" (In root, "above" .roo folder)
- ".roo/docs/database_schema.md"
- ".roo/rules/01-general.md"
- ".roo/rules/02-database.md"
- ".roo/rules-front-end/02-design-patterns.md"
and really, I'd look through all the rules files to modify to YOUR style.

### Misc
- I've added "Orchestrator" to .roomodes local mode file so that I can give it read, edit, and command permissions.

### IMPORTANT agents.md
If your agentic assistant has an /init command, use it. 
Roo Code has /init. 
If not, skip down to "No Init" section.

#### Init
Optimally, use a high reasoning, large context-window model.
Type into chat: "/init note: only create agents.md file in project root. Do not create any other agents.md files or modify any rules files."
Note: If you type only "/init", the LLM may create agent.md files in other folders (like within the various rules subfolders in the .roo folder). I talked with a few different LLMs about how useful those extra agents.md files are. Came to the conclusion it's better to fold all into the one agents.md file in app root.

#### No init
Here's an example prompt I'd give a "thinking/reasoning" model with large context:
"Goal: Modify 'agents.md' so it can be a succinct but detailed enough reference for any coder, ai, or team to use for understanding the application enough to be able to modify it. Be sure to analyze the entire application and think carefully through your investigation and conclusions. Do not modify any other files. Reference `.roo/rules/01-general.md` liberally, rather than duplicating *anything* that is in `.roo/rules/01-general.md`."

After the agents.md file is produced, you may wish to add something like the following (to fit your app) to the appropriate section:
```md
### Critical instructions and reference
Highest priority - follow to the letter:
`.roo/rules/01-general.md`
```

## Use and share as you wish

Created in 2025 by
Scott Howard Swain
https://OceanMedia.net

Free to use, modify, and share.

You are responsible for 
any benefits or problems
encountered as a result
of using this archive.
