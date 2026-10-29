---
name: maintaining-linux-workstations
description: Use when cleaning or updating a Linux workstation.
---

# Maintaining Linux Workstations

## Core principle

Treat workstation maintenance like clinical stabilization: measure first, remove only known waste, update through supported package managers, then repeat the same measurements. A cleanup is incomplete without before/after evidence.

For Dr. Nícholas, “Tijolão” means his notebook. Do not interpret it as a codebase, prompt, or document. Translate the first occurrence of technical terms into plain Brazilian Portuguese and lead with measured results.

## Workflow

1. Establish baseline using the same units and mount point that will be used for final comparison:
   - OS/kernel, CPU, RAM, swap, load, root filesystem usage.
   - Largest top-level directories in the user home.
   - Failed services, journal size, pending update count.
2. Inspect large directories before deletion. Separate:
   - Re-creatable caches and temporary downloads.
   - Application profiles/configuration, credentials, projects, package stores, virtual machines, and user documents.
3. Check privilege early with non-interactive sudo (`sudo -n true`). Never run interactive `sudo` over SSH via `terminal` tool — the prompt is trapped in the agent's PTY and hangs until killed, invisible to the user on the host desktop. If `sudo -n` fails, do NOT attempt a password-prompting sudo variant. Isolate user-owned cleanup, present the exact privileged command for the user to run in their own physical terminal, and continue with user-owned cleanup. Permission from the user authorizes the action; it does not supply an operating-system credential. Continue with user-owned cleanup if system maintenance is blocked.
4. Use supported cleanup paths before raw deletion:
   - `npm cache clean --force`; inspect `~/.npm/_npx` separately because npm cache cleanup does not remove it.
   - `pnpm store prune`; do not erase the active pnpm store wholesale.
   - `flatpak uninstall --unused -y`.
   - Tool-specific cache cleaners such as `uv cache clean` when available.
   - System package managers for system-wide cruft: `sudo apt-get autoremove --purge -y` after identifying the package.
5. Before invoking `sudo` for any system package removal, check for **runtime version conflicts**: if a user-managed runtime (e.g., nvm) already provides a newer version actively in use by a service, removing the system package is safe only if nothing else depends on it. Grep process ExecStart and systemd units before assuming.
6. Browser/Electron application profiles often live under `~/.config`; never delete the whole profile. Only remove explicitly identified cache directories such as `Cache`, `Code Cache`, `GPUCache`, `ShaderCache`, `DawnCache`, or `CachedData`.
7. Remove orphaned root-level npm global installs: inspect `/usr/local/lib/node_modules` and `/usr/local/bin` for packages installed via `sudo npm install -g` (e.g., `9remote`, `better-sqlite3`, `sql.js`, `systray2`). These violate FHS and are invisible to user-managed nvm. Remove them with `sudo rm -rf` only after confirming the user-managed equivalent is installed and active.
8. Preserve projects, Git state, secrets, browser profiles, active runtimes, and application installations unless independently proven obsolete.
9. Re-measure disk, RAM, failed services, and pending updates. Report completed work separately from privilege-blocked work.

## Decision table

| Target | Default action | Reason |
|---|---|---|
| Known cache | Inspect size, then remove | Re-creatable |
| Package-manager cache | Use manager cleanup command | Safer metadata handling |
| Application profile under `~/.config` | Preserve; remove named cache children only | May contain sessions and credentials |
| Package store/runtime | Prune; do not wipe | May support active projects |
| Project/Git repository | Do not alter during PC hygiene | Different scope |
| System packages/journal | Require authenticated privilege | System-wide side effect |

## Verification standard

Report at minimum: used space before/after, free space before/after, amount recovered, failed-service count, and unresolved update count. If `df` and another tool calculate percentages differently, compare like with like instead of claiming false precision.

Warnings caused solely by an intentionally closed application are context, not defects. Example: local IDE connectors may be offline because the IDE is closed.

## Common mistakes

- Conflating disk saturation with RAM load: when the user asks about a machine being "pesada/pesadão", check disk capacity first unless memory was explicitly requested.
- Spawning interactive `sudo` over SSH via terminal tool (prompt remains trapped in the agent's session, invisible to the host desktop; the process hangs until killed).
- Asking which “libraries” to install before examining the machine. Maintenance usually needs no optimizer library.
- Installing “cleaner” utilities that add permanent residue.
- Treating all of `~/.config` or `~/.local/share` as cache.
- Stopping after deletion without proving recovered space.
- Returning privileged commands as if the task were complete.
- Calling a missing administrator credential a user-permission refusal.
- Removing a system Node.js package without first checking whether a user-managed runtime (nvm) is the one actively in use — leads to either breaking active services or leaving dead system cruft behind.
- Removing `/usr/local/lib/node_modules` packages without confirming the user-managed equivalent (via nvm) is installed and active — the system package may be the only working copy.
- Forgetting to `autoremove --purge` after package removal, leaving behind orphaned configuration files that still consume space.
- Inventing a target list of dotfiles or a count of root-level items without first consulting the XDG Base Directory Specification and the FHS home-directory rule. The user corrected this: a cleanup must be validated against the published standards, not an improvised list. Check each candidate file against the specification before deciding to move it.
- Assuming any unrecognized non-dot file belongs to user projects or the agent. Several files (`.xsession-errors`, `.Xauthority`) are hardcoded by the display manager in `/etc/X11/Xsession`; they cannot be moved to `~/.local/state` without editing system files and the cost outweighs the benefit. Verify ownership before reclassifying a file as cruft, and do not delete system-created files during home-directory cleanup.
- Trusting subagent summaries about file ownership instead of inspecting the source directly. Several errors in prior cleanup runs were hidden because a summary said a file was user-created or orphaned when a direct `grep` of the writer script showed otherwise. Always read the writer before moving or deleting.

Machine-specific paths, validated commands, and observed cleanup surfaces belong in `references/workstation-notes.md`; load it only when the current machine matches.