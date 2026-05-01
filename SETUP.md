# Setup

This guide walks through everything from a clean macOS install. Estimated
time for first-time setup: 30-45 minutes (most of it is the OAuth dance
for your personas).

## Prerequisites

You need:

- macOS or Linux
- The basecamp CLI (v0.7.2 or later)
- Homebrew (for installing yq)
- yq (YAML query tool)
- Python 3.10+ with pyyaml
- OAuth credentials for each persona you want to set up

### Installing the basecamp CLI

If you don't have it already:

    brew install basecamp/tap/basecamp

Or follow instructions at https://github.com/basecamp/basecamp-cli for
your platform. Verify with:

    basecamp --version

You should see v0.7.2 or later.

### Installing yq

    brew install yq

### Installing pyyaml

    pip3 install pyyaml

## Configure your roster

### 1. Copy the template

    cp personas.example.yaml personas.yaml

`personas.yaml` is gitignored — never commit it.

### 2. Fill it in

Open `personas.yaml` in your editor. Replace:

- `YOUR_ACCOUNT_ID` — your demo Basecamp account ID. Find it in the URL
  when you're logged into the account: `https://3.basecamp.com/<account_id>/...`
- `YOUR_PROJECT_ID` — a project ID you'll use for testing. Find it in
  the project URL.
- The persona list — replace the three sample personas with your real
  ones. Keep `name` lowercase with no spaces (it becomes the basecamp
  profile name).

You can start with just 2-3 personas to validate the setup before
authorizing your full roster.

## Create profiles

### 3. Log out of Basecamp in your browser

Before running the setup script, log out of any Basecamp session you
have open as yourself. The script will open browser windows to authorize
each persona, and any active session will interfere.

### 4. Run the setup script

    bin/bcscene-setup-personas

For each persona, the script will pause and ask you to press Return.
When you do:

1. The basecamp CLI opens a browser window to authorize.
2. Log in as that persona's Basecamp identity.
3. Click "Authorize" when prompted.
4. The CLI captures the token; you return to the terminal.
5. **Log that persona out of Basecamp before continuing to the next.**

If you skip the logout step, the next persona's OAuth flow will silently
use the previous persona's session.

### 5. Verify

    basecamp profile list

You should see one profile per persona, all marked authenticated.

To verify each profile is actually a different identity (not all secretly
you):

    basecamp -P <persona-name> me

Run this for each persona. Each should return a different name and email.
If two return the same identity, your OAuth flow leaked — delete the
duplicate profile (`basecamp profile delete <name>`) and re-authorize.

## Run a scene

### 6. Customize the example scene

Open `scenes/morning-standup.yaml` and replace:

- `YOUR_PROJECT_ID` — your project ID (3 places).
- `YOUR_TODOLIST_ID` — a todolist ID in that project. Find it with
  `basecamp todolists --in <project_id>`.
- The persona names (`liza`, `alex`, `jordan`) — match names in your
  `personas.yaml`.

### 7. Dry-run first

    bin/bcscene scenes/morning-standup.yaml --dry-run

This prints what would run without actually invoking the CLI. Verify the
commands look right before running for real.

### 8. Run for real

    bin/bcscene scenes/morning-standup.yaml

Each step will fire with a 1-second pause between them. Adjust pacing
with `--pause N` (e.g., `--pause 3` for 3-second gaps).

## Writing your own scenes

Copy `scenes/morning-standup.yaml` to a new file in `scenes/` and edit.
The YAML format is documented in README.md.

For new action types not in the default list, edit
`lib/executor.py`'s `ACTION_HANDLERS` dict — each handler is a one-line
lambda mapping scene args to basecamp CLI arguments.

## Troubleshooting

**"profile X not authenticated"** — re-run `bin/bcscene-setup-personas`.
Tokens expire (typically after 14 days of inactivity).

**"No todolist specified"** — your scene's `todo-create` step is missing
the `list` arg. Find the todolist ID with
`basecamp todolists --in <project_id>` and add it to the scene.

**Scene fails partway through** — already-completed steps stay completed
in Basecamp; bcscene doesn't roll back. Edit the scene to remove the
finished steps and re-run, or just clean up manually.

**OAuth captured the wrong identity** — `basecamp profile delete <name>`
removes the profile, then re-run setup with strict logout discipline.
