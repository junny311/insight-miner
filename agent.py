# agent.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableBranch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from rag_chain import get_rag_chain
from langchain_experimental.tools import PythonREPLTool

def create_agent():
    """
    Creates and returns the main reasoning agent.
    """
    
    # 1. Define Tools
    # The RAG chain is one of our tools.
    rag_chain = get_rag_chain()
    # The Python REPL tool allows executing python code.
    python_repl = PythonREPLTool()

    # 2. Create the Router
    # The router decides which tool to use based on the user's question.
    router_template = """
    Given the user question, classify it as either "rag" or "python_repl".
    Do not respond with more than one word.

    - "rag": For questions about the content of the document, like summaries or specific information.
    - "python_repl": For questions that require calculations, data analysis, or running python code.

    Question: {question}
    
    Classification:
    """
    prompt = ChatPromptTemplate.from_template(router_template)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    question_router = prompt | llm | StrOutputParser()

    # 3. Create the Python REPL Chain
    # This chain is responsible for generating python code to answer a question.
    python_repl_template = """
    You are a Python programmer. Given a question, write a Python script to answer it.
    Only output the Python code, with no explanation or markdown.
    
    Question: {question}
    
    Python Code:
    """
    python_repl_prompt = ChatPromptTemplate.from_template(python_repl_template)
    python_chain = python_repl_prompt | llm | StrOutputParser() | python_repl

    # 4. Create the Agent using a RunnableBranch
    # This branch will route the question based on the router's classification.
    agent_branch = RunnableBranch(
        (RunnableLambda(lambda x: "python_repl" in x["topic"]), python_chain),
        rag_chain,  # Default chain
    )

    # 5. Build the final chain
    # This chain passes the original question to the branch, along with the router's classification.
    final_chain = {"topic": question_router, "question": RunnablePassthrough()} | agent_branch
    
    print("Agent created successfully.")
    return final_chain


if __name__ == '__main__':
    agent = create_agent()

    print("\n--- Testing RAG functionality ---")
    question1 = "What is the role of the ESG Committee?"
    print(f"Query: {question1}")
    answer1 = agent.invoke(question1)
    print("Answer:", answer1)
    
    print("\n--- Testing Python REPL functionality ---")
    question2 = "What is 100 * (5 + 5)?"
    print(f"Query: {question2}")
    answer2 = agent.invoke(question2)
    print("Answer:", answer2)
