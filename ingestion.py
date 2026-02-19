import os
from dotenv import load_dotenv
from llama_parse import LlamaParse

def parse_document(file_path: str):
    """
    Parses a document using LlamaParse to extract text, tables, and images.
    
    Args:
        file_path (str): The path to the PDF document.
        
    Returns:
        list: A list of Document objects containing parsed elements.
    """
    load_dotenv()
    llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")

    if not llama_cloud_api_key:
        raise ValueError("LLAMA_CLOUD_API_KEY not found in .env file.")

    parser = LlamaParse(
        api_key=llama_cloud_api_key,
        result_type="markdown",  # You can also use "json"
        verbose=True
    )
    
    # LlamaParse returns a list of Document objects
    documents = parser.load_data(file_path)
    return documents

def save_documents_to_markdown(documents, output_dir="parsed_output"):
    """
    Saves the text content of parsed documents into a single Markdown file.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, "parsed_report.md")
    
    with open(output_file_path, "w", encoding="utf-8") as f:
        for i, doc in enumerate(documents):
            f.write(f"# Document {i+1}\n\n")
            if doc.metadata:
                f.write(f"## Metadata\n")
                for key, value in doc.metadata.items():
                    f.write(f"- {key}: {value}\n")
                f.write("\n")
            f.write(f"{doc.text}\n\n")
            f.write("---\n\n") # Separator between documents
    print(f"\n[INFO] Parsed content saved to '{output_file_path}'")

if __name__ == "__main__":
    from storage import add_documents

    pdf_file_name = "samsung sds sustainability report 2024.pdf"
    
    if not os.path.exists(pdf_file_name):
        print(f"Error: The file '{pdf_file_name}' was not found in the root directory.")
        print("Please ensure the PDF file is placed in the project's root directory.")
    else:
        print(f"Starting to parse '{pdf_file_name}' using LlamaParse...")
        try:
            parsed_documents = parse_document(pdf_file_name)
            print(f"\nSuccessfully parsed '{pdf_file_name}'.")
            print(f"Total documents extracted: {len(parsed_documents)}")

            # Add parsed documents to the vector store
            print("\n--- Storing documents in vector store ---")
            add_documents(parsed_documents)

            # Save parsed documents to Markdown file for verification
            save_documents_to_markdown(parsed_documents)

        except Exception as e:
            print(f"An error occurred: {e}")
