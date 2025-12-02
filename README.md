# Custom Instructions

Your customizable AI coding team!
Use it to create apps or make changes/additions to existing ones. 

This set of instructions (markdown files) enhances and extends the modes/agents that come with many coding agents/assistants. The instructions are tailored to work with Roo Code (free highly customizable VS Code extension) but will work with many others, including Cursor, CLine, Kilo,Github Copilot, etc.

Using the built-in-to-Roo ability to use "rules" files, this archive is a set of custom instructions for the built-in modes/agents and some new ones, including:
- **Architect Super Team**: a 3-step "Planner" process (planner-a, planner-b, planner-c). Brainstorms with user. While planning and working, creates detailed files to keep track of its goals, progress, and lessons learned.
- **Architect Quick**: a 1-step "Planner" process; modified Roo's built-in Architect mode to be more detailed but for smaller tasks than full on 3-step "Planner" process.
- **Coder on Crack**: Juiced up "Code" mode to follow The Plan, whether created by the new superpowered Architect or hastily typed out by a user running 3 days on caffeine.
- **Code Monkey** (Junior coder): Supplemented "Code" with a tightly controlled budget-friendly "Code Monkey" created to work with the short, detailed tasks created for it by Planner.
- **Other new modes**: Added "Front-end", "Debugger", "Tester", "GitHubber", "Docs Writer", etc.
Notes:
- **Smart but cheap**: Designed both Architect and Planner modes  to "front load" spend on high "intelligence" thinking models to create a plan that is so detailed, the "Workers" like "Coder", "Code Monkey", etc. can be faster/cheaper models. Overall, I'm finding this method burns *far less* tokens, has *far less* errors, and runs longer without a need for human intervention.
- **Look how fast they grow up**: This set of instructions is ever-evolving. 
- **Virtuous circle**: The author, Scott Howard Swain, is always eager to hear ideas to improve this.

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
    - How do you want the work plan to be structured in terms of size, phase(s), and task(s)?
        - It will automatically create tasks so they are "bite-size" chunks less smart/lower-cost LLM models can more easily do the actual work.
    - What level of autonomy do you want it to have when it does the work?
    - What type of testing (browser, unit tests, custom, none) do you want it to do as it completes tasks?
- It will create a high level plan and ask you if you want to modify it or approve.
- It will also create plan and log files to help itself and you keep track of goals, progress, and lessons learned.
- Once you approve the plan, it will pass on to the other planner modes to flesh out and add detail to the plan.
- Eventually, once you approve, it will pass the plan (with detailed instructions, mode hints, etc.) on to the "orchestrator" mode.
- Note: This workflow sets the plan to prefer "code monkey" mode (lower budget than "code" mode) for the coding parts. If "code monkey" gets confused because a task is too difficult or complex, it has instructions to pass the task on to "code" mode which I assign a "smarter" LLM to.

## Folder structure
These files go in your project root. You'll see they coincide with where your current .roo folder is.

```
app
├── agents.md
└── .roomodes
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
    ├── rules-project-mgr
    │   └── 01-project-mgr.md
    ├── rules-task-simple
    │   └── 01-task-simple.md
    └── rules-tester
        └── 01-tester.md
```

## Agentflow File Sync Utility

**Helpful utility included**: A Python utility for synchronizing `.roo` directories across multiple project folders based on file modification times.

### Overview
The Agentflow File Sync Utility scans `.roo` subdirectories in multiple project folders (you designate), identifies files that need updating based on modification times, and performs intelligent file synchronization with atomic operations and backup support.

### GUI Usage
Launch the graphical interface with:
```bash
python main_gui.py
```

Use the interface to:
- Select multiple folders containing `.roo` directories.
- Configure sync settings via the Settings window and config.txt (dry-run mode, backup options).
- Monitor live progress during synchronization.
- Overwrite preview panel that shows planned overwrites before execution.
- Favorite folder sets (based on folders_faves in config) to quickly re-load common project combinations.
- Auto-creates .bak versions of all modified files.
- Button to remove all .bak files.

### CLI Usage
Run headless synchronization with:
```bash
python cli_sync.py <folder1> <folder2> ...
```

Example:
```bash
python cli_sync.py /path/to/project1 /path/to/project2 /path/to/project3
```

### Configuration
Settings are stored in `config.txt` See `README-file-sync.MD` for details.


## Fit to you
Be sure to modify the content of files to fit your project. Especially:
- "agents.md" (In root, "above" .roo folder)
- ".roo/docs/database_schema.md"
- ".roo/rules/01-general.md"
- ".roo/rules/02-database.md"
- ".roo/rules-front-end/02-design-patterns.md"
Really, I'd look through all the rules files to modify to YOUR preferences.

### Misc
- I've added "Orchestrator" to .roomodes local mode file so that I can give it read, edit, and command permissions. Without those permissions, it can sometimes have issues, depending on what LLM model you have it using. Example: I've seen it find an issue with The Plan and spend extra tokens to delegate minor textual changes to The Plan when it could have more quickly done the changes itself.

### IMPORTANT: agents.md
If your agentic assistant has an /init or other command that analyzes your codebase and creates tailored configuration files, use it. Roo Code uses /init. 

#### Init
Optimally, use a high reasoning, large context-window model.
Type into chat: "/init note: only create agents.md file in project root. Do not create any other agents.md files or modify any rules files."
Note: If you type only "/init", the LLM may create agent.md files in other folders (like within the various rules subfolders in the .roo folder). I don't know if that was a bug or feature. I researched how useful those extra agents.md files are. Came to the conclusion it's better to fold all into the one agents.md file in app root.

Here's a prompt I give a "thinking/reasoning" model with large context:
"
/init Goal: Modify `agents.md` so it can be a succinct but detailed enough reference for any coder, ai, or team to use for understanding the application enough to be able to modify it. Be sure to analyze the entire application and think carefully through your investigation and conclusions. Do not modify any other files. 

CRITICAL: Reference `.roo/rules/01-general.md` liberally with section references, rather than duplicating *anything* that is in `.roo/rules/01-general.md`.
Example: 
"

### Naming Convention
Follow `Naming Conventions` section in `.roo/rules/01-general.md`
"

After the agents.md file is produced, you may wish to add something like the following (to fit your app) to the appropriate section of that file:
```md
### Critical instructions and reference
Highest priority - follow to the letter:
`.roo/rules/01-general.md`
```

## My recipe for getting a lot done very inexpensively:
Some of the tips below are subject to change often, especially which models to use for which mode.
1) Use *free* Roo Code.
2) Use *free* AgentFlow (just a bunch of .md files telling modes exactly how to act, delegate, and more).
3) Set Architect or AgentFlow's "Planner" subteam to use GPT-5.1-R-H or M | Sonnet 4.5-R.
4) Set "Code" (Senior Coder), Front-end, Debugger, Tester modes to use a smart-model like Sonnet 4.5 or GPT-5.1-R-M.  Seriously, on paper, GPT 5.1 seems far more expensive than it really is but I find it runs so efficiently that it ends up doing a lot for pennies! I use it through OpenRouter or through OpenAI, choosing "Flex" service tier because I'm fine with how slow it is for saving $.
5) Set "Code Monkey" (Jr Coder) mode to use a cheaper coding model like GPT-5.1-Low or GLM 4.6 or Kimi K2 or Gemini 2.5 Flash (through OpenRouter is least expensive) or any comparable model because that "Planner" team I mentioned writes a very detailed plan that even includes pseudocode or code so that when the plan gets delegated by Orchestrator, Code and Code Monkey know exactly what they are expected to do.
6) Set "Task-Simple" mode to use GPT-5.1-non-reasoning or one of those dumb-and-cheap models like the Gemini 2.5 Flash I mentioned above. The AgentFlow's "Architect" and "Planner" subteam both know to delegate all file copying, and other simple tasks to this mode so you don't have your expensive models wasting money on stuff like that.

## Markdown vs XML
For LLM instruction following, which should you choose?

### If Roo Code, your choice is clear
Roo Code's native architecture employs Markdown files (.md or .txt) stored in `.roo/rules/` directories for all custom instructions. After reviewing 171+ community-created custom modes, zero use XML formatting. Roo Coderoocode The platform concatenates these Markdown files directly into Claude's system prompt in alphabetical order. YAML or JSON handle mode configuration, while instruction content remains plain Markdown.

This universal adoption of Markdown isn't documented as a deliberate choice over XML—the official Roo Code documentation simply doesn't address XML at all. The format appears to be selected for developer experience and ecosystem compatibility rather than AI performance optimization. Markdown files integrate seamlessly with version control, text editors, and documentation workflows that developers already use.

2025-11-19: Talked with a Roo Code dev. He said he uses XML and - from within the Roo Code extension - download "Mode Writer" from the Marketplace. It's now part of this repo. I used it to make an XML version of my custom version of the Architect mode. So, according to him, you *can* use XML instead of MD for your custom mode instructions. Because I find XML to be so wordy and ugly, I'll stick with MD until I see a clear problem with models getting confused by or ignoring my instructions. 

### If not Roo Code, model preferences
GPT-5.1, Sonnet 4.5, Gemini 3 all prefer XML and will score a few percentage points higher in prompt adherence when XML is used but understand MD.

### The human factor
Why I still use and prefer markdown:
- Ease of human read/write.
- Roo Code (my current favorite framework) prefers it.
- I find that no matter what model I'm using, they follow the rules I've created in markdown format.

## Use and share as you wish
Created in 2025 by
Scott Howard Swain
https://OceanMedia.net

Free to use, modify, and share.

You are responsible for 
any benefits or problems
encountered as a result
of using this archive.

Also, I'm looking for work.