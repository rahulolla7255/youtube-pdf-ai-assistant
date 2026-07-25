from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)
import re


import re

def extract_video_id(url):
    patterns = [
        r"youtu\.be\/([a-zA-Z0-9_-]{11})",
        r"youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})",
        r"youtube\.com\/embed\/([a-zA-Z0-9_-]{11})",
        r"youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_transcript(url):
    video_id = extract_video_id(url)

    if not video_id:
        return "❌ Invalid YouTube URL."

    try:
        # Create API object
        ytt_api = YouTubeTranscriptApi()

        # Fetch transcript
        fetched_transcript = ytt_api.fetch(video_id)

        # Convert transcript snippets into one string
        text = " ".join(snippet.text for snippet in fetched_transcript)

        return text

    except NoTranscriptFound:
        return "❌ No transcript found."

    except TranscriptsDisabled:
        return "❌ Transcript is disabled."

    except VideoUnavailable:
        return "❌ Video unavailable."

    except Exception as e:
        return f"❌ Error: {e}"
