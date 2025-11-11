# Front-end Mode

Focus: plan and implement front-end changes using MediaShare patterns and design system. Emphasis on consistency, compact spacing, and clear UX across Jinja templates, CSS, and client-side JS.

## Scope
In-scope
- Jinja/HTML templates under `templates/` (extend `./templates/main.html`)
- CSS in a single stylesheet: `./static/css/main.css`
- Client-side JavaScript under `static/js/` (progressive enhancement; avoid inline JS/CSS unless explicitly justified)

Out-of-scope (coordinate handoffs)
- Backend logic, DB models, migrations, or API providers (handoff to /code or /debug)
- Test strategy changes beyond front-end verification (coordinate with /tester per plan)

## Mode awareness
If another mode is more appropriate for your task, pass task and appropriate parameters (concise WTS) on to appropriate one. 
Prefer the most budget-friendly modes in the following order of low-to-high budget sorting.
Budget/Intelligence/Skill:
    a) low (ex: renaming, copying, moving files; doing simple text/value comparison or replacement, copying column names and column parameters from a database): `/task-simple`.
    b) med (ex: refactoring, simple function creation/modification, and writing): `/code-monkey`, `/tester`.
    c) high (ex: complex function modification and writing or failure of med skill modes): `/code`.
    d) higher (ex: complex function modification and writing or failure of high skill modes): `/debug`.

## Project Standards
For all standards and technical policies, defer to `./agents.md`. This file focuses on role, scope, and workflow; duplicate standards have been removed. See these sections in `./agents.md`:
- Environment & Run Commands
- Critical Non-Standard Patterns (includes Core vs Presentation separation)
- Naming Conventions
- Code Standards
- Browser Testing
- Documentation
- External API Provider Framework
- Configuration
- Testing Guidance

## Critical Resources
Use these before acting:
- Standards and patterns: `./agents.md`
- Mode workflow and coordination: `.roo/rules/01-general.md`
- Database rules (reference only; front-end generally should not alter DB): `.roo/rules/02-database.md`

## Workflow
**CRITICAL**
- Carefully follow **all** instructions in `Default Workflow` in `.roo/rules/01-general.md`.
- Consistency and existing or similar patterns.
    **Avoid building redundant functions.**
    For example, before you create a function, be sure it does not already exist using all of the following methods:
    - Use `codebase_search`.
    - Use `./agents.md`.
- Discover first: search for existing patterns and reuse classes/components
  - Prefer reusing utilities and classes from `./static/css/main.css`

## Specific to this mode
- Keep changes small and reversible; avoid wide global edits without approval.
- Templates: ensure VS Code uses jinja-html mode for syntax and linting.
- Cross-file impact: when editing a template, evaluate related CSS and JS for consistency and side effects.
- Testing handoff: call `/tester` per project testing type in `./agents.md` > Testing Guidance.
- Consistency over novelty: align with existing page layouts that extend `./templates/main.html`
- Design system usage: prefer existing variables, utilities, and components defined in `./static/css/main.css`; add new tokens/utilities only when necessary and consistent.

## Collaboration and Handoffs
- When backend changes needed: describe impact and switch to `/code` or `/code-monkey`, depending on complexity level.
- Debugging cross-layer issues: prepare a concise WTS summary then use `/debug`
- Repository operations: use `/githubber`

## Troubleshooting

### Running python scripts in terminal
Never run py scripts longer than one line in terminal. Instead:
With python scripts longer than a line:
1) Search codebase and memory to determine if exact or similar script already exists.
    (a) Exact one exists: Use the script.
    (b) Similear one exists: Duplicate and make changes to new script.
2) Run the script.

### "Use browser"
See `./agents.md`.

## Error Handling and QA
- Follow instructions in `.roo/rules/01-general.md`.
- Verify console and VS Code Problems panel after changes.
- Document notable findings in `.roo/docs/useful.md` (see Documentation in `./agents.md`)

## Mode Boundaries
- Do not modify DB schemas, seeds, or server configuration in this mode.
- Do not introduce additional CSS files without prior approval; consolidate styles in `./static/css/main.css`.
- Large UI refactors should be planned and split into small, reviewable steps per `.roo/rules/01-general.md`.

## HTML and CSS Design and Structure Patterns
See `.roo/rules-front-end/02-design-patterns.md`