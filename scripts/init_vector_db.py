import pathlib

import chromadb
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

root_dir = pathlib.Path(__file__).parent.parent
vector_db_dir = root_dir / 'db' / 'vector_db'
data_dir = root_dir / 'data'

if __name__ == "__main__":
    client = chromadb.PersistentClient(path=vector_db_dir.as_posix())
    collection = client.get_or_create_collection(name='corp_credit_collection')

    # loading the document

    loader = PyPDFDirectoryLoader(data_dir.as_posix())

    raw_documents = loader.load()

    # splitting the document

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(raw_documents)

    # preparing to be added in chromadb

    documents = []
    metadata = []
    ids = []

    i = 0

    for chunk in chunks:
        documents.append(chunk.page_content)
        ids.append("ID"+str(i))
        metadata.append(chunk.metadata)

        i += 1

    # adding to chromadb

    # print(documents)
    # print(metadata)
    # print(ids)
    collection.add(
        documents=documents,
        metadatas=metadata,
        ids=ids
    )
