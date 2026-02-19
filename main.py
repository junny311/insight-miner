# main.py
import streamlit as st
import os
import tempfile

# It's good practice to import your project modules after standard libraries
from ingestion import parse_document
from storage import add_documents
from agent import create_agent

# --- Page Configuration ---
st.set_page_config(
    page_title="Insight-Miner 🔍",
    page_icon="🔍",
    layout="wide"
)

# --- Session State Initialization ---
def initialize_session_state():
    """Initializes session state variables if they don't exist."""
    if "agent_chain" not in st.session_state:
        st.session_state.agent_chain = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "processed_file_name" not in st.session_state:
        st.session_state.processed_file_name = None

initialize_session_state()

# --- Main App Logic ---
st.title("Insight-Miner 🔍")
st.write("Welcome! Upload a PDF document to begin asking questions about its content.")

# --- Sidebar for PDF Upload and Processing ---
with st.sidebar:
    st.header("1. Process Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="file_uploader")

    # If a file is uploaded, and it's a new file, process it.
    if uploaded_file and uploaded_file.name != st.session_state.get("processed_file_name"):
        st.session_state.messages = [] # Clear previous chat history
        st.session_state.agent_chain = None # Reset agent
        
        with st.spinner(f"Processing {uploaded_file.name}... This might take a few minutes depending on the document size and API limits."):
            # Save uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            try:
                # 1. Parse Document
                st.info("Step 1/3: Parsing document with LlamaParse...")
                parsed_docs = parse_document(tmp_file_path)
                
                # 2. Add documents to Vector Store
                st.info("Step 2/3: Storing document content in ChromaDB...")
                add_documents(parsed_docs)
                
                # 3. Create Agent
                st.info("Step 3/3: Initializing AI Agent...")
                st.session_state.agent_chain = create_agent()
                
                # 4. Update session state
                st.session_state.processed_file_name = uploaded_file.name
                st.success(f"'{uploaded_file.name}' processed successfully. You can now ask questions.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.processed_file_name = None # Reset on error
            finally:
                os.remove(tmp_file_path) # Clean up temp file
    
# --- Main Chat Interface ---
st.header("2. Ask Questions")

if not st.session_state.agent_chain:
    st.info("Please upload a PDF document in the sidebar to activate the agent.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about the document..."):
    if not st.session_state.agent_chain:
        st.warning("Agent not ready. Please upload and process a PDF first.")
        st.stop()

    # Add user message to display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent_chain.invoke(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {e}")
