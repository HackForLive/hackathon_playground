from setuptools import setup, find_packages

setup(
   name='frontend_ui',
   version='1.0',
   description='A user interface module',
   author='Test User',
   author_email='testuser@test',
   packages=['frontent_ui'],  #same as name
   install_requires=[
       'streamlit'
   ], #external packages as dependencies
)
