def get_api_key(api_key_name):
    secret = openai_secret_manager.get_secret(api_key_name)
    if "error" in secret:
        raise ValueError(secret["error"])
    return secret["api_key"]

openai = {
    'api_key': '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 '
}