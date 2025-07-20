from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv
from tqdm import tqdm



os.environ["HF_HOME"] = "./hf_cache"

load_dotenv(dotenv_path=".env")
PDF_FOLDER = "pdfs"
VECTOR_STORE_FOLDER = "vector_store"

def pdf_loader(pdf_folder):

    all_documents=[]
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder,filename)
            print(f"Loading {filename}...")
            loader = PyPDFLoader(pdf_path)
            documents=loader.load()
            all_documents.extend(documents)
    
    return all_documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        separators =  ["\n\n", "\n","."," "]
    )
    return splitter.split_documents(documents)

def create_embeddings(split_docs):
    print("Creating embedding using HuggingFace...")
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": False}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    vectorstore= FAISS.from_documents(split_docs,embeddings)
    return vectorstore

def save_vectorstore(vectorstore, folder):
    os.makedirs(folder, exist_ok=True)
    vectorstore.save_local(folder)
    print(f"Vector store saved to {folder}")

def main():
    print("Starting PDF ingestion...")

    #1. Load all PDF documents

    documents = pdf_loader(PDF_FOLDER)
    print(f"Loaded {len(documents)} pages")

    #2. Split into chunks
    split_docs = split_documents(documents)
    print(f"Split into {len(split_docs)} chunks")

    #3. Create embeddings
    vectorStore = create_embeddings(split_docs)

    #4. Save vectorstores
    save_vectorstore(vectorStore, VECTOR_STORE_FOLDER)

    print("Ingestion complete!")

if __name__ == "__main__":
    main()


