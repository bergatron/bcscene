---
name: basecamp todos update --due is silently broken
description: The `basecamp todos update <id> --due <date>` CLI flag reports success but does not actually apply the due date; use raw API PUT instead
type: feedback
---

`basecamp todos update <id> --due <YYYY-MM-DD>` returns `ok: true` and a "Updated todo" summary, but the due date is **not** actually saved — a follow-up GET still shows `due_on: null`. Same behavior with natural-language dates.

**Why:** Observed while bulk-assigning due dates across an Enormicom HQ todoset. CLI claimed every update succeeded; verification via the API showed none had taken effect.

**How to apply:** When you need to set a due date on a BC3 todo, skip `basecamp todos update --due` and PUT directly:

```
basecamp api put "/buckets/<bucket>/todos/<id>.json" \
  --data '{"content":"<existing content>","due_on":"YYYY-MM-DD"}'
```

Always include `content` (and any other fields you want preserved — see `feedback_basecamp_todo_put.md`) since BC3 PUT clobbers unsent fields. Verify with a GET after; do not trust the CLI's success message for due-date changes.
