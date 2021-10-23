
from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import wave  # создание и чтение аудиофайлов формата wav
import json  # работа с json-файлами и json-строками
import os  # работа с файловой системой
import pyaudio
import io, os, sys, setuptools, tokenize
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

# Создаем словарь частей железного человека с цветами пикселей
slovar2 = {'лицо'      :253,
           'голова'    :252,
           'блики'     :251,
           'грудь'     :250,
           'плечи'     :249,
           'руки'      :248,
           'предплечье':247,
           'предплечья':247,
           'живот'     :246,
           'шея'       :245,
           'глаза'     :244,
           'реактор'   :243,
           'Reactor'   :243,
           }

# Создаем словарь цветов в формате png
colors2 = {'жёлтый' :[255, 255, 0, 255],
           'Жёлтый' :[255, 255, 0, 255],
           'красный':[255, 0, 0, 255],
           'синий'  :[0, 0, 255, 255],
           'зелёный':[0, 255, 0, 255],
           'голубой':[170, 170, 255, 255],
           'черный' :[0, 0, 0, 255],
           'чёрный' :[0, 0, 0, 255]}

# Преобразуем картинку в массив Numpy
im = Image.open("ironman (1).png")
iron = np.array(im)

# Выведем картинку на экран
plt.figure(figsize=(10,18))
plt.imshow(im)
plt.show()

# Функция для изменения цвета, в соответствии с распознанными командами
def avto(arr):
  for ind,k in enumerate(arr):
    if k in slovar2.keys():
      if arr[ind+1] in colors2.keys():
        iron[iron[:,:,0] == slovar2[k]] = colors2[arr[ind+1]]
  return iron

def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит попытка
        # использовать offline-распознавание через Vosk
        except speech_recognition.RequestError:
            print("Trying to use offline recognition...")
            recognized_data = use_offline_recognition()

        return recognized_data


def use_offline_recognition():
    """
    Переключение на оффлайн-распознавание речи
    :return: распознанная фраза
    """
    recognized_data = ""
    try:
        # проверка наличия модели на нужном языке в каталоге приложения
        if not os.path.exists("models/vosk-model-small-ru-0.4"):
            print("Please download the model from:\n"
                  "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit(1)

        # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
        wave_audio_file = wave.open("microphone-results.wav", "rb")
        model = Model("models/vosk-model-small-ru-0.4")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()

                # получение данных распознанного текста из JSON-строки
                # (чтобы можно было выдать по ней ответ)
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]
    except:
        print("Sorry, speech service is unavailable. Try again later")

    return recognized_data


if __name__ == "__main__":

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    while True:
        # старт записи речи с последующим выводом распознанной речи
        # и удалением записанного в микрофон аудио
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")
        print(voice_input)
        voice_input_split = voice_input.split(' ')
        # Раскрашиваем
        iron = avto(voice_input_split)
        # Выведем картинку на экран
        im2 = Image.fromarray(iron)
        plt.figure(figsize=(10, 18))
        plt.imshow(im2)
        plt.show()