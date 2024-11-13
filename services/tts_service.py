from gtts import gTTS


def generate_tts(word):
    tts = gTTS(text=word, lang="zh")
    tts.save(f"static/audio/{word}.mp3")
    return f"/static/audio/{word}.mp3"
