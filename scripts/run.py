import subprocess
import pathlib
import argparse


root_dir = pathlib.Path(__file__).parent.parent

pytest_config = root_dir / 'pytest.ini'
env_config = root_dir / 'environment.yaml'
print(pytest_config)
print(env_config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='run', description='Automation of tasks')
    
    parser.add_argument('action', type=str, choices=['install', 'build', 'streamlit', 'test'])
    args = parser.parse_args()

    if args.action == 'install':
        subprocess.run('pip install genai_hackathon', cwd='src', shell=True)
    elif args.action == 'build':
        subprocess.run(f"conda env update --name hackathon_venv --file {env_config} --prune", shell=True)
        subprocess.run('pip install -e .', cwd='src', shell=True)
    elif args.action == 'streamlit':
        subprocess.run('streamlit run genai_hackathon/pages/main.py', cwd="src", shell=True)
    else:
        raise NotImplementedError('Unknown. Choose correct component name to be run!')
