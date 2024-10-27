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
    
    parser.add_argument('action', type=str, choices=[
        'install', 'build', 'streamlit', 'init_db', 'test', 'test_smoke'])
    args = parser.parse_args()

    if args.action == 'install':
        subprocess.run('pip install .', cwd='src', shell=True)
    elif args.action == 'build':
        subprocess.run(f"conda env update --name hackathon_venv --file {env_config} --prune", shell=True)
        subprocess.run('pip install -e .', cwd='src', shell=True)
    elif args.action == 'streamlit':
        subprocess.run('streamlit run genai_hackathon/pages/app.py', cwd="src", shell=True)
    elif args.action == 'init_db':
        subprocess.run(f'python init_vector_db.py', cwd='scripts', shell=True)
    elif args.action == 'test':
        subprocess.run(f'python -m pytest -rpP -c {pytest_config}', cwd="test", shell=True)
    elif args.action == 'test_smoke':
        subprocess.run(f'python -m pytest -rpP -c {pytest_config} -m "smoke"', cwd="test", shell=True)
    else:
        raise NotImplementedError('Unknown. Choose correct component name to be run!')
