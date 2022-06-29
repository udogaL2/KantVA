import config as config
import stt
import tts
import parser
import os
from fuzzywuzzy import fuzz
import datetime
from num2t4ru import num2text
from random import choice


def search_name(text: str):
    text = text.split()
    for name in config.VA_ALIAS:
        try:
            index = text.index(name)
            return ' '.join(text[index:])
        except Exception:
            pass

    return ''


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}

    for c, v in config.VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    if cmd == 'help':
        text = "Я достаточно занят+ой человек, поэтому много времени не смогу уделить... " \
               "Если хочешь, то я могу дать тебе наставление..., рассказать о грядущих мероприятиях... " \
               "и интересных местах... или же сделать с тобой фотогр+афию..."
        tts.va_speak(text, 'help0')

    elif cmd == 'greeting':
        text, anim = choice(config.VA_ANS_LIST['greeting'])
        tts.va_speak(text, anim)

    elif cmd == 'ctime':
        now = datetime.datetime.now()
        text = "Сейч+ас " + num2text(now.hour) + " " + num2text(now.minute)
        tts.va_speak(text, 'time')

    elif cmd == 'photo':
        text, anim = choice(config.VA_ANS_LIST['photo'])
        tts.va_speak(text, anim)

    elif cmd == 'quote':
        quote = parser.get_quotes()
        tts.va_speak(quote, 'quotes')

    elif cmd == 'events':
        parser.generate_nearest_event()
        tts.va_speak('Я знаю несколько вариантов, предлагаю рассмотреть вот этот.', 'event',
                     qr=os.path.abspath(os.curdir) + 'qrcodes\\qr_event.png')

    elif cmd == 'place':
        parser.generate_place()
        tts.va_speak("Я знаю много знаменитых мест, ... вот одно из них.", "place",
                     qr=os.path.abspath(os.curdir) + 'qrcodes\\qr_place.png')

    elif cmd == 'gratitude':
        tts.va_speak('Всегда пожалуйста...', 'thx')


def va_respond(voice: str):
    if voice:
        print(voice)
        voice = search_name(voice)

    if voice.startswith(config.VA_ALIAS):
        filter_voice = filter_cmd(voice)
        cmd = recognize_cmd(filter_voice)

        print(filter_voice)

        if cmd['percent'] < 39:
            text, anim = choice(config.VA_ANS_LIST['error'])
            tts.va_speak(text, anim)
        else:
            execute_cmd(cmd['cmd'])


class KantVA:
    def __init__(self, path_to_config: str):
        config.load_config(path_to_config)
        print(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ...")

        tts.va_speak(
            "Привет! ... Меня зовут Имману+ил Кант. ... Приятно познакомиться. ... Когда захочешь обратиться ко мне,"
            "то начни свою фразу моим именем или фамилией.", 'start')
        stt.va_listen(va_respond)
