import openai_secret_manager
import json
import openai_secret_manager

# define your secret key name
secret_key = "my_secret_key"

# retrieve your secret
my_secret = "my_super_secret_password"

# save your secret
openai_secret_manager.save_secret(secret_key, my_secret)


def get_secret(key_name):
    secrets = openai_secret_manager.get_secret(key_name)
    return secrets['value']


def save_secret(key_name, secret):
    secrets = openai_secret_manager.get_secrets()
    secrets[key_name] = {'value': secret}
    with open(openai_secret_manager.get_secret_file_path(), 'w') as f:
        json.dump(secrets, f)


class OpenAISecretManager:
    def __init__(self, secrets_name):
        self.secrets_name = secrets_name
        self.secrets = openai_secret_manager.get_secret(secrets_name)

    def get_secret(self, secret_name):
        return self.secrets.get(secret_name)['value']

    def set_secret(self, secret_name, value):
        self.secrets[secret_name]['value'] = value
        save_secret(self.secrets_name, self.secrets)

    def delete_secret(self, secret_name):
        del self.secrets[secret_name]
        save_secret(self.secrets_name, self.secrets)
