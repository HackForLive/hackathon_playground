import os

from dotenv import find_dotenv, load_dotenv
from genai_hackathon import env_cfg_path
from genai_hackathon.utils.logger import app_logger

def _load_env():
    if not env_cfg_path.exists():
        app_logger.debug(f"Env file: {env_cfg_path} does not exist!")
        raise FileNotFoundError(
            f"Please create env file {env_cfg_path}. More information is in README file")
    env_file = find_dotenv(env_cfg_path)
    load_dotenv(env_file)
    app_logger.debug(f"Env file: {env_cfg_path} is loaded.")
    

def get_env_var(key: str):
    value = os.getenv(key=key, default=None)

    if not value:
        app_logger.debug(f"Key: {key} does not exist, try to load env variables.")
        _load_env()
    
    return os.getenv(key=key)
