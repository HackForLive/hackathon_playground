import pytest
import pathlib
import chromadb

root_dir = pathlib.Path(__file__).parent.parent
vector_db_dir = root_dir / 'db' / 'vector_db'


@pytest.mark.db_connection
def test_connection():
    assert vector_db_dir.exists()
    _ = chromadb.PersistentClient(path=vector_db_dir.as_posix())
