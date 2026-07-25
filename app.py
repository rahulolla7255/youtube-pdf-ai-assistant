import streamlit as st
import os

from utils.chatbot import ask_question
from utils.vectorstore import create_vectorstore
from utils.speech import speech_to_text
from utils.text_to_speech import text_to_audio
from utils.youtube_loader import load_youtube_transcript


st.set_page_config(
    page_title="YouTube PDF RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 YouTube + PDF RAG  Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = []


if "voice_question" not in st.session_state:
    st.session_state.voice_question = ""


if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""


st.sidebar.title("📚 Knowledge Base")


# Existing PDFs

st.sidebar.subheader("Existing PDFs")


pdf_folder = "data/pdfs"


if os.path.exists(pdf_folder):

    pdf_files = os.listdir(pdf_folder)

    if pdf_files:

        for file in pdf_files:

            if file.endswith(".pdf"):

                st.sidebar.write(
                    "📄 " + file
                )

    else:

        st.sidebar.info(
            "No PDF available"
        )

else:

    st.sidebar.info(
        "PDF folder not found"
    )

# Upload PDF


st.sidebar.divider()

st.sidebar.subheader(
    "📤 Upload New PDF"
)


uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files",
    type="pdf",
    accept_multiple_files=True
)
if uploaded_files:


    if st.sidebar.button(
        "Process Documents"
    ):


        upload_folder = "data/uploads"


        os.makedirs(
            upload_folder,
            exist_ok=True
        )


        for file in uploaded_files:


            file_path = os.path.join(
                upload_folder,
                file.name
            )


            with open(
                file_path,
                "wb"
            ) as f:

                f.write(
                    file.getbuffer()
                )


        with st.spinner(
            "Creating vector database..."
        ):

            create_vectorstore()


        st.sidebar.success(
            "Documents processed successfully"
        )

st.sidebar.divider()

st.sidebar.subheader(
    "▶️ Add YouTube Video"
)

youtube_url = st.sidebar.text_input(
    "Paste YouTube URL"
)
if youtube_url:


    if st.sidebar.button(
        "Process YouTube"
    ):


        with st.spinner(
            "Extracting YouTube transcript..."
        ):


            try:

                youtube_docs = load_youtube_transcript(
                    youtube_url
                )


                create_vectorstore(
                    youtube_docs
                )


                st.sidebar.success(
                    "YouTube video added successfully!"
                )


            except Exception as e:

                st.sidebar.error(
                    str(e)
                )

if st.sidebar.button(
    "🗑 Clear Chat"
):

    st.session_state.messages = []

    st.session_state.last_answer = ""

    st.rerun()


for message in st.session_state.messages:


    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )

st.divider()


col1, col2 = st.columns(
    [10, 1]
)


with col2:

    if st.button(
        "🎤"
    ):

        with st.spinner(
            "Listening..."
        ):

            voice_text = speech_to_text()


        if voice_text:

            st.session_state.voice_question = voice_text

            st.rerun()



with col1:

    typed_question = st.chat_input(
        "Ask your question..."
    )

question = typed_question
if not question:

    question = st.session_state.voice_question

st.session_state.voice_question = ""

if question:


    

    st.session_state.messages.append(

        {
            "role": "user",
            "content": question
        }

    )


    with st.chat_message(
        "user"
    ):

        st.write(
            question
        )


    

    with st.chat_message(
        "assistant"
    ):


        with st.spinner(
            "Searching documents..."
        ):


            answer = ask_question(

                question,

                st.session_state.messages

            )


        st.write(
            answer
        )


        

        st.session_state.last_answer = answer


        st.session_state.messages.append(

            {
                "role": "assistant",
                "content": answer
            }

        )

if st.session_state.last_answer:


    st.divider()


    st.subheader(
        "🔊 Listen Answer"
    )


    if st.button(
        "▶ Play Answer"
    ):


        with st.spinner(
            "Generating audio..."
        ):


            audio_file = text_to_audio(

                st.session_state.last_answer

            )



        if os.path.exists(audio_file):


            with open(
                audio_file,
                "rb"
            ) as audio:


                audio_bytes = audio.read()



            st.audio(

                audio_bytes,

                format="audio/mp3"

            )


        else:


            st.error(
                "Audio file was not created."
            )