import api_keys

# use the API keys from api_keys.py
my_secret = api_keys.openai['api_key']


# import openai_secret_manager where save_secret is defined
def save_openai_secret():
    import openai_secret_manager

    # save the secret
    openai_secret_manager.save_secret('openai', my_secret)


# call the function to save the secret
save_openai_secret()
