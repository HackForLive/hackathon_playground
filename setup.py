from setuptools import setup, find_packages

setup(
    name='hackthon_playground',
    version='1.0',
    description='A user interface module',
    author='Test User',
    author_email='testuser@test',
    packages=['frontend_ui', 'backend'],
    install_requires=[
        'streamlit',
        'pydantic',
        'fastapi',
        'uvicorn',
        'setuptools',
        'python-dotenv',
        'openai'
   ], #external packages as dependencies
)
