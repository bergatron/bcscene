# bcscene

Run scripted multi-persona activity in a Basecamp demo account.

You describe what you want in plain English (in Claude Desktop's Code
tab) or write a YAML scene file, and bcscene executes the activity by
invoking the official basecamp CLI as a different authenticated
profile per persona. The result: realistic-looking activity across
multiple users in seconds.

## What it's for

Producing demo content. Specifically:

- Recording videos that show realistic Basecamp activity without
  manually logging in as multiple people.
- Capturing screenshots that need cross-persona context (a chat with
  three replies, a project with mixed contributors, etc.).
- Keeping a demo Basecamp account looking lived-in over time.

## Getting started

**New to this?** Read **[GUIDE.md](GUIDE.md)** — a step-by-step walkthrough
written for non-technical users. Covers everything from installing
prerequisites to running your first scene through Claude Desktop. About
45 minutes start to finish, mostly waiting on OAuth flows.

**Already comfortable with the command line?** See
**[SETUP.md](SETUP.md)** for the condensed reference.

## How it works

bcscene is a thin runner on top of the basecamp CLI's native
multi-profile support. Each persona maps to a `basecamp profile` — a
separately authenticated identity — and bcscene runs each scene step
using the right profile.

There is no credential juggling. The basecamp CLI handles tokens; you
authorize each persona once via OAuth and bcscene just invokes the
CLI.

The recommended day-to-day workflow uses **Claude Desktop's Code tab**
(which runs Claude Code). You launch a Claude Code session in the
bcscene folder and describe scenes in plain English. The repo includes
a `CLAUDE.md` file that primes Claude Code with everything it needs to
know — what the personas are, what actions are available, when to ask
for clarification, when to dry-run.

You can also write scene files by hand in YAML and run them with
`bin/bcscene <scene-file>`. Both workflows work; pick what suits you.

## Available scene actions

A scene step uses one of these actions:

- `chat-post` — post to a project chat (args: message, project)
- `todo-create` — create a todo (args: title, project, list, optionally
  description, assignee, due)
- `todo-complete` — complete a todo (args: todo_id)
- `comment` — comment on a target (args: target_id, message)
- `message-post` — post a message board entry (args: title, body, project)

To add new actions, edit `lib/executor.py`'s `ACTION_HANDLERS` dict.

## Limitations

- One scene at a time (no parallel execution — the CLI uses a
  per-machine profile store, so two scenes running at once could
  collide).
- No undo. Posts and todos created by a scene stay in Basecamp.
- Personas must be real Basecamp users. There's no way to fake
  activity from a user you don't have a real OAuth token for.

## Repo layout

```
bcscene/
├── bin/
│   ├── bcscene                    # scene runner
│   └── bcscene-setup-personas     # one-time profile creation
├── lib/
│   ├── cli_wrapper.py             # subprocess calls to basecamp CLI
│   ├── executor.py                # runs a scene
│   └── loader.py                  # parses YAML
├── scenes/
│   └── morning-standup.yaml       # example scene
├── personas.example.yaml          # template roster
├── personas.yaml                  # your real roster (gitignored)
├── GUIDE.md                       # step-by-step walkthrough
├── SETUP.md                       # condensed setup reference
└── CLAUDE.md                      # context for Claude Code
```
