import speech_recognition as sr


def speech_to_text():

    recognizer = sr.Recognizer()


    with sr.Microphone() as source:

        stt = "Listening..."

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=10
        )


    try:

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        return text


    except Exception as e:

        return None
