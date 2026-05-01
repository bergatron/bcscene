# Getting started with bcscene

A friendly walkthrough for first-time users.

## What this does

bcscene lets you make multiple Basecamp personas (Liza, Alex, Chris,
etc.) appear to chat, post messages, and create todos in your demo
account — without you manually logging in as each one. You write a
"scene" describing what each persona does, run one command, and watch
the activity unfold in Basecamp.

It's mainly used for producing demo content: videos, screenshots, and
keeping the demo account looking lived-in.

## Before you start

You'll need:

- About 45 minutes of focused time the first time through. Most of
  that is logging in as each persona one-by-one (the boring part).
- The login credentials for each persona you want to use. These are in
  1Password under the demo account vault — ask if you don't know
  where to find them.
- A Mac. (Linux works too, but this guide assumes Mac.)

You don't need to know git, Python, or what a YAML file is. We'll
explain everything.

## A note on the Terminal

Everything in this guide happens in an app called **Terminal** — it
comes with macOS and lets you type commands instead of clicking. If
you've never used it, that's fine. We'll tell you exactly what to type.

To open it: press `Cmd+Space`, type "Terminal", press Return. A window
opens with a prompt that ends in `%` or `$`. That's where you type.

When this guide shows commands in boxes like this:

    cd ~/Code

...you type or paste them at the prompt and press Return. The Terminal
runs the command and shows you the result.

**Important:** When commands ask for a password (like the Mac password
or a website password), the Terminal hides what you type. No dots, no
asterisks, just a blank space. That's normal. Type the password and
press Return.

---

# Phase 1: One-time setup

Do this once on your Mac. It takes about 15 minutes.

## Step 1: Install Homebrew

Homebrew is a tool for installing other tools. To check if you have it:

    brew --version

If it prints a version number (like `Homebrew 4.x.x`), skip to Step 2.

If it says "command not found," install it by pasting this command:

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/main/install.sh)"

It'll ask for your Mac password and take a few minutes. When it's
done, it usually prints two or three lines telling you to run extra
commands — do whatever those say. Then verify with `brew --version` again.

## Step 2: Install the basecamp CLI

The basecamp CLI is what bcscene uses to actually post things to
Basecamp.

    brew install basecamp/tap/basecamp

Verify:

    basecamp --version

You should see `basecamp version 0.7.2` or higher.

## Step 3: Install yq

yq reads the YAML files bcscene uses.

    brew install yq

## Step 4: Install Python's YAML library

Python is already on your Mac, but it needs a little extra to read YAML.

    pip3 install pyyaml

## Step 5: Install the GitHub CLI

This makes downloading the bcscene repo easy.

    brew install gh

Then log in (it'll open a browser):

    gh auth login

Pick: GitHub.com → HTTPS → Yes (authenticate Git) → Login with web
browser. Follow the prompts.

## Step 6: Download bcscene

Make a folder for code projects (if you don't already have one):

    mkdir -p ~/Code
    cd ~/Code

Download the bcscene repo:

    gh repo clone younotcooking/bcscene

Go into the new folder:

    cd bcscene

You're now in the bcscene folder. Verify with:

    ls

You should see files like `README.md`, `SETUP.md`, `bin`, `lib`,
`scenes`, and `personas.example.yaml`.

---

# Phase 2: Configure your personas

This tells bcscene which Basecamp personas you want to use.

## Step 7: Make your own personas file

Copy the template:

    cp personas.example.yaml personas.yaml

This creates `personas.yaml` — your personal copy. The template stays
unchanged. Your personal copy never gets uploaded to GitHub (it's
listed in something called `.gitignore` that keeps it private).

## Step 8: Edit your personas file

Open it with a simple editor called nano:

    nano personas.yaml

The bottom of the screen shows shortcuts. The two you need:

- **Ctrl+O** to save (then press Return when it asks the filename)
- **Ctrl+X** to exit

Use the arrow keys to move around. Edit these things:

- The line that says `account_id: "YOUR_ACCOUNT_ID"` — replace
  `YOUR_ACCOUNT_ID` with the demo Basecamp account ID. To find it: go
  to your demo Basecamp account in a browser. The URL looks like
  `https://3.basecamp.com/5185276/...`. The number after
  `3.basecamp.com/` is the account ID.

- The line that says `default_project_id: "YOUR_PROJECT_ID"` — replace
  with a project ID you'll use for testing. To find it: open a project
  in Basecamp. The URL has the project ID at the end.

- The personas list — leave it alone for now, or delete personas you
  don't need. **Each persona requires a separate login during setup,
  so fewer = faster setup.** Start with 3 to validate things work, then
  add more later.

Save with **Ctrl+O**, press Return, exit with **Ctrl+X**.

---

# Phase 3: Authorize each persona

This is the longest part. For each persona, you'll log into Basecamp
once and authorize bcscene. The basecamp CLI saves the login so you
never have to do it again (until tokens expire after ~14 days of inactivity).

## Step 9: Log out of Basecamp in your browser

Important: log out of any Basecamp session you have open as yourself.
The setup script will open browser windows to authorize each persona —
if you're already logged in as yourself, it'll authorize you instead
of the persona. Bad.

## Step 10: Run the setup script

    bin/bcscene-setup-personas

For each persona in your file, the script will:

1. Print "Press Return to continue."
2. Wait for you.

When you press Return:

3. The basecamp CLI opens a browser window.
4. Log in with that persona's credentials (from 1Password).
5. Click "Authorize" when Basecamp asks.
6. The CLI captures the login. You return to the Terminal.
7. **Log that persona out of Basecamp** before pressing Return for the
   next one. Otherwise the next persona gets logged in as the previous
   one. (To log out: avatar in top-right → Log out.)

Repeat until done. Don't rush — getting the wrong identity attached to
a profile is annoying to undo.

## Step 11: Verify

Check that all personas got created:

    basecamp profile list

You should see one row per persona, all marked "yes" under
Authenticated.

To make sure each profile is actually a different identity (not all
secretly you), pick one and run:

    basecamp -P liza me

Replace `liza` with whichever persona you want to check. It'll print a
name and email. The name and email should match that persona — not
your name. Repeat for the others.

---

# Phase 4: Run your first scene

## Step 12: Edit the example scene

The example scene is at `scenes/morning-standup.yaml`. It has
placeholders that need real values:

    nano scenes/morning-standup.yaml

Replace:

- `YOUR_PROJECT_ID` (appears 4 times) — your project ID, same one you
  put in `personas.yaml`.
- `YOUR_TODOLIST_ID` (appears once) — a todolist ID. To find one, exit
  nano (Ctrl+X) and run:

      basecamp -P liza todolists --in YOUR_PROJECT_ID

  Replace `YOUR_PROJECT_ID` with your real project ID. It'll print a
  list of todolists with IDs. Pick one, copy the ID, then re-open the
  scene file and paste it in.

- The persona names (`liza`, `alex`, `jordan`) — change `jordan` to a
  persona that exists in your `personas.yaml` (or change the others
  too if liza/alex aren't in your file).

Save and exit.

## Step 13: Test without actually running it

Before posting anything to Basecamp, do a "dry run" to preview what
would happen:

    bin/bcscene scenes/morning-standup.yaml --dry-run

This prints out what bcscene would do without actually doing it. You
should see four steps printed, each with `[dry-run] basecamp -P ...`
in front of it, and "Scene complete" at the end.

If anything looks wrong (typos, wrong project ID, etc.), fix the scene
file and dry-run again.

## Step 14: Run for real

When the dry run looks right:

    bin/bcscene scenes/morning-standup.yaml

The four steps will fire one by one with a 1-second pause between
them. Open Basecamp in your browser to watch the activity appear.

Done! You've run your first scene.

---

# What's next

## Run the same scene again

Just run the same command — it'll repost everything. Useful if you're
shooting a video and need a clean take.

## Adjust pacing

Add `--pause N` to slow things down (or speed them up):

    bin/bcscene scenes/morning-standup.yaml --pause 5

This puts 5 seconds between each step. Good for video where you want
viewers to register each action.

## Write your own scenes

Make a copy of `morning-standup.yaml`, give it a new name, and edit
it. The format is fairly intuitive — read the example and you'll see
the pattern.

If you want full details on what actions are available and how to
write more complex scenes, see `SETUP.md` in the repo.

---

# When something goes wrong

## "command not found"

You typed a command that the Terminal doesn't recognize. Either:

- You misspelled it. Check the spelling.
- You're in the wrong folder. Run `pwd` to see where you are. If
  you're not in `/Users/<yourname>/Code/bcscene`, run
  `cd ~/Code/bcscene` to get back.
- You skipped an install step. Go back to Phase 1.

## "permission denied"

The script doesn't have permission to run. Fix it with:

    chmod +x bin/bcscene bin/bcscene-setup-personas

Then try again.

## A persona authorization went to the wrong identity

If `basecamp -P liza me` returns your name instead of Liza's, the
OAuth flow caught your session. Fix:

    basecamp profile delete liza

Then re-run `bin/bcscene-setup-personas`. This time make absolutely
sure you're logged out of Basecamp as yourself before the browser
opens.

## A scene fails partway through

Steps that already ran stay in Basecamp — bcscene doesn't undo
anything. Just edit the scene to remove the steps that already worked,
then re-run. Or clean up manually in Basecamp.

## "No todolist specified"

Your scene's `todo-create` step is missing the `list` field. Add a
real todolist ID to the scene's args. Find one with:

    basecamp -P <persona> todolists --in <project_id>

## Everything is broken and I don't know why

Ping Chad — that's me. Or open an issue on the repo:
https://github.com/younotcooking/bcscene/issues
