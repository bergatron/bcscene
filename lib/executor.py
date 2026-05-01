"""Execute a scene: run each step as the appropriate profile."""

import time
from cli_wrapper import run, BasecampError


def _todo_args(a):
    """Build args for todo creation. --list is required by the CLI."""
    cmd = ["todo", a["title"], "--in", str(a["project"])]
    if "list" in a:
        cmd += ["--list", str(a["list"])]
    if "description" in a:
        cmd += ["--description", a["description"]]
    if "assignee" in a:
        cmd += ["--assignee", a["assignee"]]
    if "due" in a:
        cmd += ["--due", a["due"]]
    return cmd


# Map scene-level action names to basecamp CLI verbs + arg builders.
# Each builder takes the step's `args` dict and returns a list of CLI args.
ACTION_HANDLERS = {
    "chat-post": lambda a: ["chat", "post", a["message"], "--in", str(a["project"])],
    "todo-create": _todo_args,
    "todo-complete": lambda a: ["done", str(a["todo_id"])],
    "comment": lambda a: ["comment", str(a["target_id"]), a["message"]],
    "message-post": lambda a: ["message", "post", a["title"], a["body"], "--in", str(a["project"])],
}


def execute_scene(scene, dry_run=False, pause=1.0):
    """Run each step in the scene sequentially.

    pause: seconds to wait between steps.
    """
    print("Running scene: " + scene.get("name", "unnamed"))
    if scene.get("description"):
        print("  " + scene["description"])
    print()

    steps = scene["steps"]
    for i, step in enumerate(steps, 1):
        persona = step["persona"]
        action = step["action"]
        args = step.get("args", {})

        if action not in ACTION_HANDLERS:
            raise ValueError("Unknown action: " + action)

        cli_args = ACTION_HANDLERS[action](args)
        print("[{}/{}] {}: {}".format(i, len(steps), persona, action))

        try:
            run(persona, cli_args, dry_run=dry_run)
        except BasecampError as e:
            print("  FAIL: " + str(e))
            raise

        print("  OK")

        if i < len(steps) and not dry_run:
            time.sleep(pause)

    print("\nScene complete")
