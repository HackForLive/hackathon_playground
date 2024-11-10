import pathlib

import chromadb
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

root_dir = pathlib.Path(__file__).parent.parent
vector_db_dir = root_dir / 'db' / 'vector_db'
data_dir = root_dir / 'data'
financials_dir = data_dir / 'financials'


def load_test_corp_credit_guide():
    collection = client.get_or_create_collection(name='corp_credit_collection')

    # loading the document

    loader = PyPDFDirectoryLoader(data_dir.as_posix(), recursive=False, glob='*.pdf')

    raw_documents = loader.load()

    # splitting the document

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(raw_documents)

    # preparing to be added in chromadb

    documents = []
    metadata = []
    ids = []

    for i, chunk in enumerate(chunks):
        documents.append(chunk.page_content)
        ids.append("ID"+str(i))
        metadata.append(chunk.metadata)

    # adding to chromadb
    collection.add(
        documents=documents,
        metadatas=metadata,
        ids=ids
    )


def load_financial_reports():
    collection = client.get_or_create_collection(name='financial_report_collection')

    # loading the document

    loader = PyPDFDirectoryLoader(financials_dir.as_posix(), recursive=True)

    raw_documents = loader.load()

    # splitting the document

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(raw_documents)

    # preparing to be added in chromadb

    documents = []
    metadata = []
    ids = []

    for i, chunk in enumerate(chunks):
        documents.append(chunk.page_content)
        ids.append("ID"+str(i))
        metadata.append(chunk.metadata)

    # adding to chromadb
    collection.add(
        documents=documents,
        metadatas=metadata,
        ids=ids
    )



if __name__ == "__main__":
    client = chromadb.PersistentClient(path=vector_db_dir.as_posix())

    load_financial_reports()
    load_test_corp_credit_guide()
