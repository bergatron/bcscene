# Getting started with bcscene

A friendly walkthrough for first-time users.

## What this does

bcscene lets you make multiple Basecamp personas (Liza, Alex, Chris,
etc.) chat, post messages, and create todos in your demo account —
without you manually logging in as each one. You describe what you
want in plain English (or write a "scene" file), and bcscene makes the
activity happen in Basecamp.

It's mainly used for producing demo content: videos, screenshots, and
keeping the demo account looking lived-in.

## How you'll actually use it

The recommended day-to-day workflow uses **Claude Desktop's Code tab**
(which runs Claude Code, an AI assistant that has access to your files
and terminal). You'll open Claude Desktop, switch to the Code tab,
launch a Claude Code session in the bcscene folder, and just describe
the scene you want. Claude figures out which personas to use and runs
the right commands.

This is the modern bcscene workflow. Older bcscene used a similar
setup but managed personas more painfully — the new version uses the
official basecamp CLI's profile system, which is much cleaner.

> **Important: don't use Claude Desktop's regular chat with the
> Basecamp connector for this.** That posts everything as you (your
> own account), not as personas. The Code tab is the one that runs
> Claude Code, which uses bcscene's persona profiles. We'll show you
> exactly which tab to click.

## Before you start

You'll need:

- About 45 minutes of focused time the first time through. Most of
  that is logging in as each persona one-by-one (the boring part).
- The login credentials for each persona you want to use. These are in
  1Password. When prompted for the persona, go into 1Password, search
  for the person's first name, then click on the result titled
  "Basecamp Demo."
- A Mac. (Linux works too, but this guide assumes Mac.)
- Claude Desktop installed (the chat app from Anthropic).
- Basecamp CLI installed.

You don't need to know git, Python, or what a YAML file is. We'll
explain everything.

## A note on the Terminal

Some setup steps happen in an app called **Terminal** — it comes with
macOS and lets you type commands instead of clicking. If you've never
used it, that's fine. We'll tell you exactly what to type.

To open it: press `Cmd+Space`, type "Terminal", press Return. A window
opens with a prompt that ends in `%` or `$`. That's where you type.

When this guide shows commands in boxes like this:

    cd ~/Code

...you type or paste them at the prompt and press Return.

**When commands ask for a password** (the Mac password or a website
password), the Terminal hides what you type. No dots, no asterisks,
just a blank space. That's normal. Type the password and press Return.

Once setup is done, you'll spend most of your time in Claude Desktop's
Code tab — not Terminal.

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

You should see files like `README.md`, `GUIDE.md`, `bin`, `lib`,
`scenes`, `personas.example.yaml`, and `CLAUDE.md`.

---

# Phase 2: Configure your personas

This tells bcscene which Basecamp personas you want to use.

## Step 7: Make your own personas file

Copy the template:

    cp personas.example.yaml personas.yaml

This creates `personas.yaml` — your personal copy. The template stays
unchanged. Your personal copy never gets uploaded to GitHub (it's
gitignored).

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
  so fewer = faster setup.** A reasonable approach: start with 3 to
  validate things work, then come back later and add the rest.

Save with **Ctrl+O**, press Return, exit with **Ctrl+X**.

---

# Phase 3: Authorize each persona

This is the longest part. For each persona, you'll log into Basecamp
once and authorize bcscene. The basecamp CLI saves the login so you
never have to do it again (until tokens expire after a long period of
inactivity).

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

> **Need a break?** No problem. Press **Ctrl+C** to exit the script.
> When you come back, just run `bin/bcscene-setup-personas` again — it
> picks up where you left off. Already-authorized personas get skipped
> automatically.

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

This is where you stop using Terminal and switch to Claude Desktop's
Code tab. From here on, you describe scenes in plain English.

## Step 12: Open Claude Code in the bcscene folder

1. Open **Claude Desktop**.
2. Click the **Code** tab. (It's a separate tab from the regular chat.)
3. The Code tab gives you a terminal-like input where you can type
   commands. In it, type:

       cd ~/Code/bcscene

   Press Return.

4. Then type:

       claude

   Press Return.

This launches a Claude Code session that knows about your bcscene
repo, your personas, and the scene format. It also reads a special
`CLAUDE.md` file in the repo that explains how bcscene works — so you
don't have to.

## Step 13: Describe a scene in plain English

Try this for your first scene:

> Have Liza post a quick standup message in our test project, then
> have Alex respond saying he's blocked on the API spec, then have
> Chris apologize and create a todo to write the spec.

Claude will:

1. Probably ask you which project to use (it doesn't assume — coworker
   safety). Tell it the project ID.
2. Probably ask which todolist for the todo. Find one with
   `basecamp -P liza todolists --in <project_id>` in another Terminal
   window, or ask Claude to find one for you.
3. Generate the messages, dry-run the scene first to show you a
   preview, and ask if you want to proceed.
4. On your approval, run the scene live. Posts and todo appear in
   Basecamp under the right personas.

If you want Claude to skip the dry-run preview when you're confident,
just say "skip the dry-run and run it directly." Claude follows your
preference.

## Step 14: Watch it happen

Open Basecamp in your browser, navigate to the project, and watch the
chat fill in as Claude executes the scene. The whole thing takes 5-10
seconds.

Done! You've run your first scene.

---

# What's next

## Run more scenes

Just keep prompting Claude. Some things you can ask for:

- **Replay a saved scene** — "Run the morning-standup scene file
  again." (Claude finds it in the `scenes/` folder.)
- **Variations** — "Run morning-standup again but make Alex's blocker
  about a different topic."
- **Original scenes** — "Have Liza, Sara, and Marco have a debate
  about whether to use Postgres or MySQL. Make it last 6-8 messages."
- **Ambient activity** — "Make 4 random personas post something
  realistic about their day in our project."

## Adjust pacing for video

If you're recording a video and want viewers to register each action:

> Run morning-standup with 5-second pauses between steps.

## Save scenes for reuse

Ask Claude to save a scene to a file:

> Make a scene where Liza onboards a new team member, three personas
> welcome them, and someone creates a "review onboarding doc" todo.
> Save it as scenes/onboarding.yaml so I can run it again later.

Once saved, you can just say "run scenes/onboarding.yaml" anytime.

---

# Common needs

## Adding a new persona later

If a new persona gets added to the demo account and you want to use
them in scenes:

1. Open `personas.yaml` in nano:

       nano personas.yaml

2. Add the new persona at the bottom of the `personas:` list,
   following the same format as existing entries:

       - name: newperson
         display_name: "New Person"
         email: newperson@enormicom.com

3. Save and exit (Ctrl+O, Return, Ctrl+X).

4. Re-run the setup script:

       bin/bcscene-setup-personas

   It'll skip everyone you already authorized and just OAuth the new
   persona.

## Fixing a persona authorized as the wrong identity

If `basecamp -P liza me` returns your name instead of Liza's (or any
persona's profile is attached to the wrong account), you OAuth'd the
wrong session. Fix it:

1. Delete the broken profile:

       basecamp profile delete liza

2. Make sure you're logged out of Basecamp in your browser.

3. Re-run the setup script:

       bin/bcscene-setup-personas

   It'll skip authorized personas and re-OAuth just `liza`. Pay
   attention to the browser this time — make sure the right persona
   is logging in.

## Writing scenes by hand (instead of asking Claude)

If you prefer to write scenes as YAML files yourself, see `SETUP.md`
in the repo for the format and full action reference. Then run them
with `bin/bcscene scenes/your-scene.yaml`.

---

# When something goes wrong

## "command not found"

The Terminal doesn't recognize what you typed. Either:

- You misspelled it. Check the spelling.
- You're in the wrong folder. Run `pwd` to see where you are. If
  you're not in `/Users/<yourname>/Code/bcscene`, run
  `cd ~/Code/bcscene` to get back.
- You skipped an install step. Go back to Phase 1.

## "permission denied" when running scripts

Fix it with:

    chmod +x bin/bcscene bin/bcscene-setup-personas

Then try again.

## A scene fails partway through

Steps that already ran stay in Basecamp — bcscene doesn't undo
anything. Either ask Claude to clean up (it can delete posts and
todos), or clean up manually in Basecamp's UI. Then re-run the part
that failed.

## "No todolist specified"

A scene's `todo-create` step is missing the `list` field. Either ask
Claude to fix it, or find a todolist ID with:

    basecamp -P <persona> todolists --in <project_id>

...and add it to the scene file.

## Claude Desktop's chat says "I can only post as you"

You're in the wrong tab. The regular chat with the Basecamp connector
posts via API as your account, which can't be different personas.
Switch to the **Code tab** instead — that runs Claude Code, which uses
bcscene's persona profiles.

## Everything is broken and I don't know why

Ping Chad — that's me. Or open an issue on the repo:
https://github.com/younotcooking/bcscene/issues
