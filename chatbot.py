import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def load_database():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    vectorstore = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )


    return vectorstore


def ask_question(question, chat_history):


    # Load vector database

    vectorstore = load_database()



    # Create retriever

    retriever = vectorstore.as_retriever(

        search_kwargs={
            "k":3
        }

    )



    # Retrieve relevant documents

    documents = retriever.invoke(
        question
    )



    context = ""

    sources = []


    for doc in documents:


        context += (
            doc.page_content
            + "\n\n"
        )



        source = doc.metadata.get(
            "source",
            "Unknown"
        )


        page = doc.metadata.get(
            "page",
            None
        )



        if page is not None:

            sources.append(
                f"{source} (Page {page + 1})"
            )

        else:

            sources.append(
                source
            )



    history = ""


    for message in chat_history:


        history += (

            message["role"]
            +
            ": "
            +
            message["content"]
            +
            "\n"

        )



    llm = ChatGroq(

        model="llama-3.1-8b-instant",

        temperature=0

    )




    prompt = f"""

You have open hand to tell anything information assistant.

Follow these rules:

1. If information is not available in the documents,
say:
"I don't know from the provided documents."

Conversation History:
{history}
Context:
{context}
Question:
{question}


Answer:
"""



    # Generate response

    response = llm.invoke(
        prompt
    )


    answer = response.content

    unique_sources = list(
        set(sources)
    )


    answer += "\n\n### Sources:\n"


    for source in unique_sources:

        answer += (
            f"- {source}\n"
        )



    return answer


if __name__ == "__main__":


    question = input(
        "Ask your question: "
    )


    answer = ask_question(

        question,

        []

    )


    print("\nAnswer:")

    print(answer)