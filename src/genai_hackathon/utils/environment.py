from dotenv import find_dotenv, load_dotenv
from genai_hackathon import env_cfg_path

def load_env():
    env_file = find_dotenv(env_cfg_path)
    load_dotenv(env_file)

