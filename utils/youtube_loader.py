from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document

def extract_video_id(url):

    if "watch?v=" in url:

        return url.split("watch?v=")[1].split("&")[0]


    elif "youtu.be/" in url:

        return url.split("youtu.be/")[1].split("?")[0]


    else:

        raise Exception(
            "Invalid YouTube URL"
        )

def load_youtube_transcript(url):

    video_id = extract_video_id(url)


    try:

        api = YouTubeTranscriptApi()


        transcript = api.fetch(
            video_id
        )


        text = ""


        for item in transcript:

            text += item.text + " "



        document = Document(

            page_content=text,

            metadata={
                "source": "YouTube Transcript",
                "video_id": video_id
            }

        )


        return [document]


    except Exception as e:

        raise Exception(
            f"Transcript error: {e}"
        )
