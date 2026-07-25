import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.document_loaders import PyPDFLoader

def load_pdfs():

    documents = []


    pdf_folder = "data/pdfs"


    if not os.path.exists(pdf_folder):

        return documents



    for file in os.listdir(pdf_folder):


        if file.endswith(".pdf"):


            path = os.path.join(
                pdf_folder,
                file
            )


            loader = PyPDFLoader(path)


            docs = loader.load()


            documents.extend(docs)



    return documents

def load_uploaded_pdfs():

    documents = []


    folder = "data/uploads"


    if not os.path.exists(folder):

        return documents



    for file in os.listdir(folder):


        if file.endswith(".pdf"):


            path = os.path.join(
                folder,
                file
            )


            loader = PyPDFLoader(path)


            docs = loader.load()


            documents.extend(docs)



    return documents

def create_vectorstore(youtube_docs=None):


    all_documents = []



    # Load existing PDFs

    pdf_docs = load_pdfs()

    all_documents.extend(pdf_docs)



    # Load uploaded PDFs

    upload_docs = load_uploaded_pdfs()

    all_documents.extend(upload_docs)



    # Load YouTube transcript

    if youtube_docs:

        all_documents.extend(
            youtube_docs
        )



    print(
        "Total Documents:",
        len(all_documents)
    )



    # Split documents

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )



    chunks = splitter.split_documents(
        all_documents
    )



    print(
        "Total Chunks:",
        len(chunks)
    )



    # Embeddings

    embeddings = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"

    )



    # Create FAISS

    vectorstore = FAISS.from_documents(

        chunks,

        embeddings

    )



    os.makedirs(
        "vectorstore",
        exist_ok=True
    )



    vectorstore.save_local(
        "vectorstore"
    )



    print(
        "Vector database created successfully!"
    )



    return vectorstore





if __name__ == "__main__":


    create_vectorstore()