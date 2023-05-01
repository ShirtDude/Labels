import json
import os

SECRETS_DIR = os.path.expanduser("~/.openai/secrets")

def get_secret(name):
    """Get the secret value for the given name."""
    filename = os.path.join(SECRETS_DIR, f"{name}.json")
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:
        raise ValueError(f"No secret found with name '{name}' in '{SECRETS_DIR}'") from exc

def save_secret(project_name, secret_value):
    """
    Save the secret value for the given project as an environment variable.
    Also, append it to the ".env" file if it exists.
    """
    os.environ[project_name.upper()] = secret_value
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, "a", encoding="utf-8") as f:
            f.write(f"{project_name.upper()}={secret_value}\n")
