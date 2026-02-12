##################################################
# PDF ingestion & vector storage (Local storage) #
##################################################

# Packages to load and preprocess PDF files, split into chunks
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Packages to create embeddings of PDF files, and store in FAISS vector
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

import os


# Define embedding model to convert text to vectors
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def build_vectorstore(folder_path, output_path):
    """
    Loads all PDF files from a folder, splits them into chunks,
    embeds the chunks and stores them in a FAISS vector index.
    """

    documents = []

    # Load all PFD files from the folder
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, file))
            documents.extend(loader.load())

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)

    # Create FAISS vector index from chunks and save to disk
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(output_path)


# Build vectorstores for domain-specific PDF files
if __name__ == "__main__":
    build_vectorstore("/Users/hephaisteon/Desktop/Coding/Sources/Installation/", "vectorstores/installation")
    build_vectorstore("/Users/hephaisteon/Desktop/Coding/Sources/Roles_rights/", "vectorstores/roles_rights")
    build_vectorstore("/Users/hephaisteon/Desktop/Coding/Sources/User_manual/", "vectorstores/user_manual")
    build_vectorstore("/Users/hephaisteon/Desktop/Coding/Sources/Customisation/", "vectorstores/customization")



    