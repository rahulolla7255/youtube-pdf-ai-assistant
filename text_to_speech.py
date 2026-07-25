from gtts import gTTS


def text_to_audio(text):

    print("text_to_audio() called")

    file_name = "answer.mp3"

    tts = gTTS(
        text=text,
        lang="en"
    )

    print("Saving MP3...")

    tts.save(file_name)

    print("MP3 saved!")

    return file_name