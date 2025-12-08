import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
import boto3

# Initialize Bedrock client (ensure AWS credentials are configured)
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1" # Replace with your desired region
)

# Initialize Bedrock Embeddings
bedrock_embeddings = BedrockEmbeddings(
    client=bedrock_runtime,
    model_id="amazon.titan-embed-text-v1" # Or your preferred Bedrock embedding model
)

def data_ingestion(pdf_path: str):
    """
    Loads a PDF document, splits it into chunks, and returns the processed documents.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: A list of LangChain Document objects.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    docs = text_splitter.split_documents(documents)
    return docs

def get_vector_store(docs, save_path="faiss_index"):
    """
    Creates a FAISS vector store from a list of documents and saves it locally.

    Args:
        docs (list): A list of LangChain Document objects.
        save_path (str): The directory to save the FAISS index.

    Returns:
        FAISS: The created FAISS vector store.
    """
    vector_store = FAISS.from_documents(docs, bedrock_embeddings)
    vector_store.save_local(save_path)
    return vector_store

if __name__ == "__main__":
    # Example usage
    pdf_file = "/Users/aniketkashyap/Developer/RAGProject/data/retrival_augmented_generation.pdf" # Make sure you have a sample.pdf in the same directory

    # Create a dummy PDF for demonstration if it doesn't exist
    if not os.path.exists(pdf_file):
        with open(pdf_file, "w") as f:
            f.write("This is a sample PDF content for testing purposes. " * 50)

    try:
        # Ingest data
        processed_docs = data_ingestion(pdf_file)
        print(f"Ingested {len(processed_docs)} document chunks.")

        # Create and save vector store
        faiss_vector_store = get_vector_store(processed_docs)
        print(f"FAISS vector store created and saved to 'faiss_index'.")

        # You can now load the vector store later for retrieval
        loaded_vector_store = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)
        print("FAISS vector store loaded successfully.")

        # Perform a similarity search (optional)
        query = "What is this document about?"
        results = loaded_vector_store.similarity_search(query, k=2)
        print("\nSimilarity Search Results:")
        for res in results:
            print(f"- {res.page_content[:100]}...")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
