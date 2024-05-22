import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader

import shutil

# Speed up embedding tokenizer by parallelizing
os.environ['TOKENIZERS_PARALLELISM'] = 'true'

# Directory containing the PDFs
documents_directory = './documents'

# Initialize the PDF loader and text splitter for chunking and splitting
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)

# Initialise Nomic's embedding model through HuggingFace
embedding = HuggingFaceEmbeddings(
    model_name="nomic-ai/nomic-embed-text-v1.5",
    model_kwargs={"trust_remote_code": True},
)

chromadb_path = "./chromadb"

# Delete any existing indexed documents before re-indexing
# Make sure the path exists and it's a directory
if os.path.exists(chromadb_path) and os.path.isdir(folder_path):
    shutil.rmtree(chromadb_path)
    print(f"'{chromadb_path}' has been reset")
else:
    print(f"'{chromadb_path}' does not exist or is not a directory.")


# Create a new Chroma database for indexing run
chroma = Chroma("lawdify", embedding_function=embedding, persist_directory=chromadb_path)

file_counter = 0

# Iterate over all files in the directory
for filename in os.listdir(documents_directory):
    if filename.endswith('.pdf'):
        # Construct the full path to the file
        file_path = os.path.join(documents_directory, filename)

        # Load the PDF content and split into chunks
        pdf_content = PyPDFLoader(file_path)
        chunks = pdf_content.load_and_split(text_splitter)

        print(f"Indexing chunks from: {filename}")
        chroma.add_documents(documents=chunks)
        file_counter += 1

print(f"Finished indexing {file_counter} PDFs in '{documents_directory}'")
