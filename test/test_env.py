import importlib
import pytest
import pandas as pd

@pytest.mark.smoke
def test_env():
    assert pd.__version__ == '2.2.3'

@pytest.mark.smoke
@pytest.mark.parametrize("pkg", ["streamlit", "openai"])
def test_import(pkg: str):
    importlib.import_module(pkg)
