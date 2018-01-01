

def text_to_speech(filename='auto_generated_audio.mp3',text='Good morning'):
    from gtts import gTTS
    import os
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return os.path.join(os.getcwd(),filename)

text_to_speech()