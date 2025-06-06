import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from models.embeddings import embed_model
import os
import tempfile
import pickle

def process_pdf(file_bytes, filename):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    vectordb = FAISS.from_documents(chunks, embed_model)
    
    # Create vectordb directory in the project root
    vectordb_dir = os.path.join(os.path.dirname(__file__), "..", "vectordb")
    os.makedirs(vectordb_dir, exist_ok=True)
    
    # Save the vector database
    vectordb_path = os.path.join(vectordb_dir, "index")
    vectordb.save_local(vectordb_path)

    os.remove(tmp_path)
