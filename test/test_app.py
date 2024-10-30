import pathlib

import pytest
from streamlit.testing.v1 import AppTest


@pytest.mark.e2e
def test_app_run():
    root_dir = pathlib.Path(__file__).parent.parent
    app_path = root_dir / 'src' / 'genai_hackathon' / 'app.py'

    assert app_path.exists()

    app = AppTest.from_file(app_path.as_posix())
    app.run()

    assert not app.exception


@pytest.mark.e2e
def test_click_on_button():
    root_dir = pathlib.Path(__file__).parent.parent
    app_path = root_dir / 'src' / 'genai_hackathon' / 'pages' / 'rag.py'

    assert app_path.exists()

    app = AppTest.from_file(app_path.as_posix())
    app.run()

    assert not app.exception

    app.button(key='cc_button_id').click()

    assert not app.exception