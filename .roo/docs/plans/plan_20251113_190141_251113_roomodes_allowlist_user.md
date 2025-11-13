# User Query

Flesh out this plan: `.roo/docs/plans/plan_251113_file_sync_file_stuff.md`

The plan proposes adding support for optionally syncing the `.roomodes` file (which lives at the project root, next to `.roo` directory) across projects while maintaining the existing `.roo`-only safety boundary. This would add:
- A configurable root-level file allowlist feature
- Support for safely including specific root-level files like `.roomodes` in the sync
- Default to empty allowlist (safest option)
- Option to enable `.roomodes` inclusion via config

Goal: Implement the minimal, safe design outlined in the existing plan to allow selective inclusion of root-level files in the sync process while maintaining strict safety boundaries.