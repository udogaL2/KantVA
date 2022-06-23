import config
import parser
import tts
from fuzzywuzzy import fuzz
import datetime
from num2t4ru import num2text
from parser import get_quotes
from random import choice


def va_respond(voice: str):
    if voice:
        print(voice)
    if voice.startswith(config.VA_ALIAS):
        filter_voice = filter_cmd(voice)
        cmd = recognize_cmd(filter_voice)

        print(filter_voice)

        if cmd['percent'] < 39:
            text, anim = choice(config.VA_ANS_LIST['error'])
            tts.va_speak(text, anim)
        else:
            execute_cmd(cmd['cmd'])


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
        quote = get_quotes()
        tts.va_speak(quote, 'quotes')

    elif cmd == 'events':
        parser.generate_nearest_event()
        tts.va_speak('Я знаю несколько вариантов, предлагаю рассмотреть вот этот.', 'event')
        #
        # вывести qrcode на экран
        #

    elif cmd == 'place':
        parser.generate_place()
        tts.va_speak("Я знаю много знаменитых мест, ... вот одно из них.", "place")
        #
        # вывести qrcode на экран
        #

    elif cmd == 'gratitude':
        tts.va_speak('Всегда пожалуйста...', 'thx')
