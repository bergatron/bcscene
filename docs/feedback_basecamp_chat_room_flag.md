---
name: basecamp chat post --room flag
description: When posting to a specific chat in a project with multiple rooms, the flag is --room / -r — not --campfire (which is a command alias, not a flag)
type: feedback
---

When posting to a chat in a project that has multiple chat rooms, specify the target with `--room <id>` (or `-r <id>`), **not** `--campfire`. `campfire` is a top-level command alias (`basecamp campfire ...` ≡ `basecamp chat ...`), but as a flag it's unknown and the command errors out.

**Why:** Tripped over this posting a multi-line scene to a specific chat — naturally reached for `--campfire 4261396918` and got "Unknown option: --campfire" on every line. Both names refer to the same concept, so the muscle memory is easy to get wrong.

**How to apply:** `basecamp -P <persona> chat post --in <project> --room <chat_id> -- "<message>"`. Get the chat ID by parsing the URL (`basecamp url parse "https://.../chats/ID"`) or listing chats in the project.
