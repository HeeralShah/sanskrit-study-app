# Plugin Wrappers

This directory contains thin integration wrappers that import shared Sanskrit lookup logic from the main repo codebase.

Current wrapper:

- `sanskrit-dictionary-lookup`: Codex plugin + skill wrapper

Future wrappers such as MCP servers or higher-level agents should live alongside this plugin and reuse `src/sanskrit_lookup` rather than duplicating parsing or normalization logic.
