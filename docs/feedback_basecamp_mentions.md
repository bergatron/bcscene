---
name: Basecamp @mentions in HTML bodies
description: How to embed @mentions when posting Basecamp rich-text content, especially in HTML bodies where the CLI's Markdown mention syntax silently fails
type: feedback
---

The basecamp CLI converts `[@Name](mention:SGID)` → rendered mention **only when the body is parsed as Markdown**. If the body contains raw HTML (e.g. nested `<ul><li>...</li></ul>` for indented bullets), the markdown mention syntax is passed through as literal text — the post succeeds but `@Name` shows up as broken markdown.

**Why:** Hit this on Janet/Liza/Matthew check-in answers. Needed nested bullets (which requires HTML — Markdown-indented sub-bullets get flattened by the check-in answer renderer), but mentions stayed as literal `[@Matthew Rogerson](mention:BAh...)` text in the rendered output.

**How to apply:**

- **Markdown body, mentions work:** use `[@Name](mention:SGID)` or `[@Name](person:ID)` or `@First.Last`.
- **HTML body, mentions need raw element:** embed each mention as
  ```html
  <bc-attachment sgid="SGID" content-type="application/vnd.basecamp.mention">@Display Name</bc-attachment>
  ```
  Basecamp renders this with the avatar + figcaption automatically. Works on both `create` and `update`.
- **Look up SGIDs:** `basecamp -P <persona> people pingable --jq '.data[] | select(.name == "...") | .attachable_sgid'`. The pingable list excludes the calling user, so to mention persona X in their own post, query pingable as a *different* persona.

**Two adjacent gotchas worth remembering together:**

1. **Bullet content + `--` separator:** Content starting with `-` (bullet lists) is parsed as flags. Add `--` before the content positional: `basecamp ... -- "$BODY"`.
2. **Flag order with `--`:** Any `--jq`, `--json`, etc. must come **before** the `--`, or they get treated as part of the content and end up appended to the post. Right: `basecamp ... --in 123 --jq '.data.id' -- "$BODY"`. Wrong: `basecamp ... --in 123 -- "$BODY" --jq '.data.id'`.

**`update` endpoint quirk:** the check-in answer `update` path does **not** process mention markdown even when the body looks like Markdown — only `create` does. So for any rich-text edit, the safe move is raw `<bc-attachment>` mentions regardless of body format.
