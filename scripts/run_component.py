
from dotenv import find_dotenv
from dotenv import load_dotenv

import os
import subprocess
import pathlib
import argparse

env_file = find_dotenv(".env")
load_dotenv(env_file)

file_dir = pathlib.Path(__file__).parent
backe_path = file_dir / 'run_backend.sh'
fronte_path = file_dir / 'run_frontend.sh'

host_name = os.getenv('HOST_NAME')
fe_host_name = os.getenv('FE_HOST_NAME')
fe_port = os.getenv('FE_PORT')
be_port = os.getenv('BE_PORT')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='HackthonComponent',
                    description='Component to run',
                    epilog='Could be backend or frontend')
    
    parser.add_argument('comp', type=str, choices=['backend', 'frontend'])           # positional argument
    args =parser.parse_args()

    if args.comp == 'frontend':
        # uvicorn backend.main:app --reload --host=0.0.0.0 --port=8000
        # streamlit run frontend_ui/src/pages/main.py --server.port 8080
        subprocess.run(['streamlit', 'run', 'frontend_ui/src/pages/main.py'])
    elif args.comp == 'backend':
        subprocess.run(['uvicorn', 'backend.main:app', '--reload', f'--host={host_name}', f'--port={be_port}'])
    else:
        raise NotImplementedError('Unknown. Choose correct component name to be run!')
