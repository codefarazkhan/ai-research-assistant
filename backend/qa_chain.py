import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from models.llm import llm_model
from models.embeddings import embed_model
import os

def qa_pipeline(question: str):
    # Check if vector database exists
    vectordb_path = os.path.join(os.path.dirname(__file__), "..", "vectordb", "index")
    vectordb_faiss_path = os.path.join(vectordb_path, "index.faiss")
    
    if not os.path.exists(vectordb_path) or not os.path.exists(vectordb_faiss_path):
        return "No documents have been uploaded yet. Please upload a PDF document first using the /upload endpoint."
    
    try:
        vectordb = FAISS.load_local(vectordb_path, embed_model, allow_dangerous_deserialization=True)
        retriever = vectordb.as_retriever(search_kwargs={"k": 5})

        qa = RetrievalQA.from_chain_type(
            llm=llm_model,
            retriever=retriever,
            chain_type="stuff"
        )

        result = qa.run(question)
        return result
    except Exception as e:
        return f"Error processing question: {str(e)}. Please make sure documents are properly uploaded."
