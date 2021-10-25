from AudioR import record_and_recognize_audio
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import os

if __name__ == '__main__':

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # старт записи речи с последующим выводом распознанной речи
    # и удалением записанного в микрофон аудио
    voice_input = record_and_recognize_audio()
    os.remove("microphone-results.wav")
    print(voice_input)