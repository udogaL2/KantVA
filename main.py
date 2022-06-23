import config
import stt
import analyzer
import tts

if __name__ == '__main__':
    print(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ...")
    tts.va_speak("Привет! ... Меня зовут Имману+ил Кант. ... Приятно познокомиться. ... Когда захочешь обратиться ко мне,"
                 "то начни свою фразу моим именем или фамилией.", 'start')
    stt.va_listen(analyzer.va_respond)
