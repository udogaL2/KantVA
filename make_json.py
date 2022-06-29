import json

r_json = {'cmd': '', 'text': '', 'time': 0, 'qr': ''}


def make_json(cmd, text: str, time, qr=None):
    r_json['cmd'] = cmd
    r_json['text'] = ' '.join(text.replace('...', '').replace('+', '').split())
    r_json['time'] = time
    r_json['qr'] = qr

    with open("cmd_json.json", "w", encoding='utf-8') as write_file:
        json.dump(r_json, write_file, ensure_ascii=False)

    write_file.close()