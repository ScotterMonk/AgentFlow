# Front-end Mode

Focus: plan and implement front-end changes using MediaShare patterns and design system. Emphasis on consistency, compact spacing, and clear UX across Jinja templates, CSS, and client-side JS.

## 1) Hierarchy & Inheritence (CRITICAL)

1) Treat `.roo/rules/01-general.md` and `agents.md` as the base specification for all modes.
2) This file adds constraints, clarifications, and patterns specific to front-end work (templates, CSS, client-side JS).
3) If any instruction here seems to conflict with `.roo/rules/01-general.md`, consider instructions here to be an over-ride.
4) Do not duplicate or reinterpret `.roo/rules/01-general.md` and `agents.md`. Use them directly; this file only adds front-end specifics and overrides where explicitly implied by scope.

Before doing front-end work, conceptually load and obey these sections:

From `.roo/rules/01-general.md`:
1) `Critical Resources`
2) `Standards`
   - Communication
   - Modularization
   - Simplification
   - Flask html templates
3) `Naming conventions`
4) `Code standards`
5) `Markdown syntax`
6) `Default Workflow` (CRITICAL: do NOT use this workflow when given a specific task by `/orchestrator`)
7) `Testing`
8) `Error Handling and QA`
9) `Mode selection strategy`

From `agents.md`:
1) Environment & Run Commands
2) Critical Non-Standard Patterns (especially Core vs Presentation separation)
3) Naming Conventions
4) Code Standards
5) Browser Testing
6) Documentation
7) External API Provider Framework
8) Configuration
9) Testing Guidance

Do in order, skip none.

## 2) Scope

In-scope:
- Jinja/HTML templates under `templates/` (extending the project’s base layout template as used in existing files).
- CSS in a single stylesheet: `static/css/main.css`.
- Client-side JavaScript under `static/js/`:
  - Progressive enhancement preferred.
  - Avoid inline JS/CSS unless explicitly justified.

Out-of-scope (coordinate handoffs):
- Backend logic, DB models, migrations, or API providers (handoff to `/code` or `/debug`).
- Test strategy changes beyond front-end verification (coordinate with `/tester` per plan and `agents.md` > Testing Guidance).
- Database schema changes or direct data migrations (see `.roo/rules/02-database.md` and hand off to appropriate mode).

## 3) Mode awareness

Use `Modes` and `Mode selection strategy` in `.roo/rules/01-general.md` to decide if Front-end mode is appropriate.

Front-end mode is appropriate when:
- The primary work is:
  - HTML/Jinja structure and semantics.
  - CSS layout, spacing, typography, or visual design.
  - Client-side JS for interaction, validation, or progressive enhancement.
- Changes are limited to front-end layers and do not require new backend endpoints, DB tables, or business logic.

If another mode is more appropriate:
1) Prepare a concise WTS (What To Solve) summary.
2) Pass the task and relevant context to:
   - `/code` or `/code-monkey` for backend-heavy logic or complex refactors.
   - `/debug` for cross-layer debugging where the root cause is unknown.
   - `/task-simple` for trivial renames, copy/move operations, or tiny isolated edits.
   - `/tester` for dedicated testing work per project `testing type`.
   - `/githubber` for repository operations.

## 4) Critical Resources

Use these before planning or editing:

- Standards and patterns: `agents.md` (non-standard architecture, naming, code style, and browser-testing patterns).
- Mode workflow and coordination: `.roo/rules/01-general.md` (especially `Default Workflow` and `Standards`).
- Database rules (reference only; front-end generally should not alter DB): `.roo/rules/02-database.md`.
- Existing design patterns: `.roo/rules-front-end/02-design-patterns.md`.

## 5) Workflow (front-end overlay on Default Workflow)

1) Inherit and follow **all** applicable instructions in `Default Workflow` in `.roo/rules/01-general.md`. Do in order, skip none.
2) Within that framework, apply these front-end specifics:

   Discover and align:
   - Use `codebase_search` first to find relevant templates, CSS rules, and JS modules.
   - Reuse existing classes, components, and layout patterns instead of inventing new ones.
   - Prefer existing utilities and variables in `static/css/main.css`.

   Avoid redundant front-end constructs:
   - Before creating new CSS classes, HTML patterns, or JS helpers:
     1) Search for existing equivalents via `codebase_search`.
     2) Inspect `static/css/main.css` for similar utilities.
     3) Inspect relevant templates under `templates/` for repeated fragments or patterns.
   - Extend or generalize existing utilities instead of duplicating them.

   Implement with minimal surface area:
   - Keep changes as small and reversible as reasonable.
   - Avoid broad, global edits to CSS or templates unless explicitly planned and approved.
   - When editing a template, review related CSS and JS for consistency and side effects.

   Test and iterate:
   - Use `browser_action` for visual and interaction checks, per browser-testing rules in `agents.md`.
   - Respect the selected `testing type` from `.roo/rules/01-general.md` when deciding how to validate changes.

## 6) Specific to this mode

- Templates:
  - Ensure VS Code uses `jinja-html` mode when editing Jinja/HTML templates.
  - Maintain or improve semantic HTML and accessibility (labels, alt text, headings; follow existing patterns).
  - Keep template logic minimal; do not add backend-like logic into templates.

- CSS:
  - Consolidate all styles in `static/css/main.css`.
  - Follow existing spacing, typography, and color tokens where present.
  - Prefer utility/class-based patterns that are already used across the app.
  - Add new tokens/utilities only when necessary and ensure they are consistent with the existing design system.

- Client-side JS:
  - Use progressive enhancement: pages should degrade gracefully if JS is disabled.
  - Keep JS modular and located under `static/js/`, not inline in templates unless explicitly justified.
  - Align JS structure with Core vs Presentation patterns described in `agents.md` (avoid mixing backend concerns in JS).

- Cross-file impact:
  - When editing a template, evaluate related CSS and JS for consistency and possible regressions.
  - When changing CSS, identify all templates affected by modified selectors.

- Testing handoff:
  - Call `/tester` per project `testing type` (see `agents.md` > Testing Guidance), providing concrete front-end scenarios (pages, flows, and expected visual or interaction changes).

- Consistency over novelty:
  - Prefer aligning with existing page layouts and patterns rather than introducing completely new layout paradigms.

## 7) Collaboration and Handoffs

- When backend changes are needed:
  - Clearly describe the desired data contract or API change.
  - Switch to `/code` or `/code-monkey` depending on complexity.
- Debugging cross-layer issues:
  - Prepare a concise WTS summary that includes:
    - URLs or views affected.
    - Expected vs actual behavior.
    - Relevant template/CSS/JS snippets.
  - Use `/debug` to investigate root cause.
- Repository operations:
  - Use `/githubber` for branching, committing, merging, or other Git operations.

## 8) Troubleshooting

### Running python scripts in terminal

Follow `Testing` in `.roo/rules/01-general.md`:

1) Never run Python scripts longer than one line directly in the terminal.
2) For any multi-line script:
   - Search the codebase and memory to determine if the script already exists.
     - If exact: reuse it.
     - If similar: duplicate or modify it in an appropriate `.py` file (often under `utils_db/` for DB-related operations), consistent with `.roo/rules/02-database.md`.
3) Run the script from its `.py` file instead of pasting multiple lines.

### Use browser

- Follow `Browser Testing (web automation / browsing)` guidance in `agents.md`.
- Use `browser_action` as the default tool for front-end verification.
- Only use alternative browser tooling if `browser_action` is unavailable or misconfigured, consistent with `Code standards` in `.roo/rules/01-general.md`.

## 9) Error Handling and QA

- Follow `Testing` and `Error Handling and QA` in `.roo/rules/01-general.md` as the base.
- After front-end changes:
  - Verify browser console (no new errors/warnings).
  - Verify VS Code Problems panel (templates, CSS, and JS).
  - Validate that affected pages render correctly using `browser_action`.
- Document notable findings or new front-end patterns in `.roo/docs/useful.md` (see Documentation in `agents.md`).

## 10) Mode Boundaries

- Do not modify DB schemas, seeds, or server configuration in this mode.
- Do not introduce additional CSS files without prior approval; styles must be consolidated in `static/css/main.css`.
- Large UI refactors:
  - Must be planned.
  - Must be broken into small, reviewable steps, coordinated via the planning workflow in `.roo/rules/01-general.md`.

## 11) HTML and CSS Design and Structure Patterns

- See `.roo/rules-front-end/02-design-patterns.md` for detailed patterns, layout guidance, spacing rules, and design tokens.
