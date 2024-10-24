from setuptools import setup, find_packages

setup(
    name='genai_hackathon',
    version='1.0',
    description='genai hackathon module',
    packages=['genai_hackathon'],
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
