# storage.py
import os
import time
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document as LangchainDocument

# Load environment variables
load_dotenv()

CHROMA_PATH = "chroma_db"

def get_embedding_function():
    """
    Initializes and returns the Google Generative AI embedding function.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file.")
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=google_api_key)
    return embeddings

def add_documents(documents):
    """
    Converts Llama-index documents to Langchain documents and adds them 
    to the ChromaDB vector store in batches.
    """
    print(f"Converting and storing {len(documents)} documents in ChromaDB...")
    
    langchain_docs = [LangchainDocument(page_content=doc.text, metadata=doc.metadata) for doc in documents]

    # Initialize Chroma with a persistent client
    vector_store = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Add documents in batches to avoid rate limiting
    batch_size = 10 # Reduced batch size
    for i in range(0, len(langchain_docs), batch_size):
        batch = langchain_docs[i:i+batch_size]
        print(f"Adding batch {i//batch_size + 1}/{(len(langchain_docs) - 1)//batch_size + 1}...")
        vector_store.add_documents(batch)
        print(f"Batch {i//batch_size + 1} added. Waiting for 60 seconds before next batch...")
        time.sleep(60) # Increased delay to 60 seconds

    vector_store.persist()
    print(f"Successfully stored documents in '{CHROMA_PATH}'.")


def get_retriever():
    """
    Initializes and returns a retriever for the ChromaDB vector store.
    """
    retriever = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=get_embedding_function()
    ).as_retriever()
    
    return retriever

if __name__ == '__main__':
    # This is for testing purposes.
    # It creates a dummy retriever and tests a similarity search.
    print("Testing the storage module...")

    # Create dummy documents (simulating LlamaParse output)
    class LlamaDoc:
        def __init__(self, text, metadata=None):
            self.text = text
            self.metadata = metadata or {}

    dummy_llama_docs = [
        LlamaDoc(text="The sky is blue."),
        LlamaDoc(text="The grass is green."),
    ]
    
    # Add documents
    add_documents(dummy_llama_docs)
    
    # Get retriever and test
    retriever = get_retriever()
    results = retriever.invoke("What color is the sky?")
    
    if results and "blue" in results[0].page_content:
        print("\nStorage module test PASSED.")
        print(f"Query: 'What color is the sky?'")
        print(f"Result: '{results[0].page_content}'")
    else:
        print("\nStorage module test FAILED.")
        print(f"Retriever did not return the expected document.")
