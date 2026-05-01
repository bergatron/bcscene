# bcscene

Run scripted multi-persona activity in a Basecamp demo account.

You write a scene as a YAML file (who does what, in what order) and bcscene
executes it by invoking the official basecamp CLI as a different
authenticated profile per persona. The result: realistic-looking activity
across multiple users in seconds.

## What it's for

Producing demo content. Specifically:

- Recording videos that show realistic Basecamp activity without
  manually logging in as multiple people.
- Capturing screenshots that need cross-persona context (a chat with
  three replies, a project with mixed contributors, etc.).
- Keeping a demo Basecamp account looking lived-in over time.

## How it works

bcscene is a thin runner on top of the basecamp CLI's native multi-profile
support. Each persona maps to a `basecamp profile` — a separately
authenticated identity — and bcscene runs each scene step using the
right profile.

There is no credential juggling. The basecamp CLI handles tokens; you
authorize each persona once via OAuth and bcscene just invokes the CLI.

## Quick start

1. Install prerequisites (see SETUP.md).
2. Clone this repo and cd into it.
3. Copy `personas.example.yaml` to `personas.yaml` and fill in your data.
4. Run `bin/bcscene-setup-personas` to create a profile per persona.
5. Edit `scenes/morning-standup.yaml` with your project ID and persona names.
6. Run `bin/bcscene scenes/morning-standup.yaml --dry-run` to preview.
7. Drop `--dry-run` to actually execute.

Full setup walkthrough in SETUP.md.

## Writing scenes

A scene is a YAML file with a list of steps. Each step has a persona
(matching a name in personas.yaml), an action, and args.

Available actions:

- `chat-post` — post to a project chat (args: message, project)
- `todo-create` — create a todo (args: title, project, list, optionally
  description, assignee, due)
- `todo-complete` — complete a todo (args: todo_id)
- `comment` — comment on a target (args: target_id, message)
- `message-post` — post a message board entry (args: title, body, project)

To add new actions, edit `lib/executor.py`'s `ACTION_HANDLERS` dict.
Each handler is a one-line lambda that maps scene args to basecamp CLI
arguments.

## Limitations

- One scene at a time (no parallel execution — the CLI uses a per-machine
  profile store, so two scenes running at once could collide).
- No undo. Posts and todos created by a scene stay in Basecamp.
- Personas must be real Basecamp users. There's no way to fake activity
  from a user you don't have a real OAuth token for.

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
└── personas.yaml                  # your real roster (gitignored)
```
