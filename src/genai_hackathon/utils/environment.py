from dotenv import find_dotenv, load_dotenv
from genai_hackathon import env_cfg_path
from genai_hackathon.utils.logger import app_logger

def load_env():
    if not env_cfg_path.exists():
        raise FileNotFoundError(
            f"Please create env file {env_cfg_path}. More information is in README file")
    env_file = find_dotenv(env_cfg_path)
    load_dotenv(env_file)
    app_logger.debug("Env file: {env_cfg_path} was loaded!")
