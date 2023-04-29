import openai_secret_manager
import json


def get_secret(key_name):
    secrets = openai_secret_manager.get_secret("samsolano_labels")
    return json.loads(secrets[key_name])


def save_secret(key_name, secret):
    secret_json = json.dumps(secret)
    openai_secret_manager.save_secret("samsolano_labels", {key_name: secret_json})
