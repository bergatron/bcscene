---
name: Basecamp todo PUT clobbers unsent fields
description: When updating a Basecamp BC3 todo, PUT replaces unsent fields like assignee_ids — always include all fields you want preserved, not just the one you're changing
type: feedback
---

When updating a Basecamp BC3 todo via `PUT /buckets/{bucket}/todos/{id}.json`, sending only the field you want to change (e.g. just `description`) will clear other fields like `assignee_ids`. The BC3 API docs imply partial updates are fine, but in practice the call behaves more like a replacement.

**Why:** Burned once — sent a PUT with just `description` to add hyperlinks to 10 todos, and it silently unassigned every assignee on every todo. User caught it and asked me to re-assign.

**How to apply:** When updating any Basecamp todo field, fetch the existing todo first and include all fields you want preserved (`content`, `description`, `assignee_ids`, `completion_subscriber_ids`, `due_on`, `starts_on`, etc.) in the PUT body — not just the field being changed. Same caution likely applies to other Basecamp resources where PUT is the update verb.
