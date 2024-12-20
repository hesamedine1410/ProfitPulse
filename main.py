import json

# Load API keys from config.json
with open("config.json") as config_file:
    config = json.load(config_file)
    api_key = config["api_key"]
    api_secret = config["api_secret"]
