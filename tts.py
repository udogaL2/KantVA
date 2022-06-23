import torch
import sounddevice as sd
import time

language = 'ru'
model_id = 'v3_1_ru'
sample_rate = 48000  # 48000
voice_path = 'kant_voice.pt'
speaker = 'random'  # aidar, baya, kseniya, xenia, random
put_accent = True
put_yo = True
device = torch.device('cpu')

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)

model.to(device)


# воспроизводим
def va_speak(what: str, cmd):
    audio = model.apply_tts(text=what + "..",
                            speaker=speaker,
                            sample_rate=sample_rate,
                            voice_path=voice_path,
                            put_accent=put_accent,
                            put_yo=put_yo)

    #
    #  отправка команды для запуска анимации мимики
    #

    sd.play(audio, sample_rate * 1.05)
    time.sleep((len(audio) / sample_rate) + 0.5)
    sd.stop()
