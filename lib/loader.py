"""Load a scene from YAML."""

import yaml


def load_scene(path):
    """Load a scene file. Returns the parsed scene dict."""
    with open(path) as f:
        scene = yaml.safe_load(f)

    if "steps" not in scene:
        raise ValueError("Scene {} has no 'steps' key".format(path))

    return scene
