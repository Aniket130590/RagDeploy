from langchain_community.document_loaders import pyPDFDirectoryloader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
import boto3

## Bedrock client
bedrock = boto3.client(service_name='bedrock-runtime')


def data_ingestion():
    loader = pyPDFDirectoryloader("./data")
    document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=1000)
    text_splitter.split_documents(document)

    docs = text_splitter.split_documents(document)
    return docs


def get_vector_store(docs):
    vector_store = FAISS.from_documents(docs, BedrockEmbeddings(bedrock_client=bedrock, model_id="amazon.titan-embed-text-v1"))
    vector_store.save_local("faiss_index")

if __name__ == "__main__":
    data=data_ingestion()
    get_vector_store(data)