from langchain_community.document_loaders import PyPDFLoader


def load_pdfs(pdf_paths):

    all_documents = []


    for pdf_path in pdf_paths:

        loader = PyPDFLoader(
            pdf_path
        )

        documents = loader.load()

        all_documents.extend(documents)


    return all_documents



if __name__ == "__main__":


    pdf_files = [
        "data/pdfs/Data Science Python all notes.pdf",
        "data/pdfs/Deep_Learning_Notes.pdf"
    ]


    docs = load_pdfs(pdf_files)


    print("Total pages loaded:", len(docs))


    print("\nFirst page content:")
    print(docs[0].page_content[:500])


    print("\nMetadata:")
    print(docs[0].metadata)
