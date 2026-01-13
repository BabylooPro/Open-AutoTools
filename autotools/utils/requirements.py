import os

# READ REQUIREMENTS FROM A FILE AND RETURN AS A LIST
# HANDLES MISSING FILES GRACEFULLY BY RETURNING AN EMPTY LIST
# THE FILENAME IS RELATIVE TO THE PROJECT ROOT (WHERE SETUP.PY IS LOCATED)
def read_requirements(filename="requirements.txt"):
    project_root = os.path.join(os.path.dirname(__file__), "..", "..")
    requirements_path = os.path.join(os.path.abspath(project_root), filename)

    try:
        with open(requirements_path, "r", encoding="utf-8") as fh:
            requirements = []

            for line in fh:
                line = line.strip()
                if line.startswith("-r") or line.startswith("--requirement"): continue
                if line and not line.startswith("#"): requirements.append(line)

            return requirements
    except FileNotFoundError:
        return []
