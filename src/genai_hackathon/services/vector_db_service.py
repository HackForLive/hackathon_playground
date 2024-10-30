import chromadb
from pathlib import Path

from genai_hackathon.utils.logger import app_logger



class LocalVectorDbService:
    def __init__(self, db_path: Path) -> None:
        app_logger.debug(db_path.as_posix())
        self._chroma_client = chromadb.PersistentClient(path=db_path.as_posix())
 
    @property
    def db_client(self):
        return self._chroma_client
