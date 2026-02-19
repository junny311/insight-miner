# rag_chain.py
from operator import itemgetter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from storage import get_retriever

def format_docs(docs):
    """
    Formats the retrieved documents into a single string.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    """
    Creates and returns the RAG (Retrieval-Augmented Generation) chain.
    """
    print("Initializing RAG chain...")
    retriever = get_retriever()
    
    # The prompt template instructs the AI on how to use the context.
    template = """
    You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Keep the answer concise.

    Context: {context} 

    Question: {question} 

    Answer:
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Initialize the Gemini model.
    # Using gemini-1.5-flash as it's fast and capable for RAG.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # The RAG chain constructed using LangChain Expression Language (LCEL).
    rag_chain = (
        {
            "context": itemgetter("question") | retriever | format_docs, # Extract 'question' for retriever
            "question": itemgetter("question") # Extract 'question' for prompt
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("RAG chain initialized successfully.")
    return rag_chain

if __name__ == '__main__':
    print("Testing the RAG chain...")
    rag_chain = get_rag_chain()
    
    question = "What is this report about?"
    print(f"\nQuerying RAG chain with: '{question}'")
    
    try:
        answer = rag_chain.invoke(question)
        print("\nAnswer:")
        print(answer)
        
        if answer:
            print("\nRAG chain test PASSED.")
        else:
            print("\nRAG chain test FAILED: No answer was returned.")

    except Exception as e:
        print(f"\nAn error occurred during RAG chain test: {e}")
