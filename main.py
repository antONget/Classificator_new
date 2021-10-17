from kivymd.app import MDApp
from kivy.lang import Builder
from plyer import filechooser
import numpy as np
from tensorflow.keras.models import load_model  # из кераса подгружаем  метод загрузки предобученной модели
import tensorflow as tf

KV = """
ScreenManager:
    MDScreen:
        id: home

        MDLabel:
            text: "Загрузите изображение для распоснания"
            #theme_text_color: "Custom"
            #text_color: .5, .5, .45, .8
            pos_hint: {"center_x": .5, "center_y": .93}
            halign: "center"
            font_style: "H4"

        MDCard:
            orientation: "vertical"
            elevation: 15
            size_hint: .7, .7
            pos_hint: {"center_x": .5, "center_y": .5}
            radius: [15, 15, 15, 15]

            FitImage:
                id: img
                #size_hint: .7, .7
                #pos_hint: {"center_x": .5, "center_y": .5}
                radius: [15, 15, 15, 15]

        MDRaisedButton:
            text: "Load Image"
            pos_hint: {"center_x": .5, "center_y": .3}
            on_press: app.file_chooser()

        MDRoundFlatButton:
            text: "Начать распознование"
            pos_hint: {"center_x": .5, "center_y": .1}


"""


class ImageClassify(MDApp):

    def build(self):
        return Builder.load_string(KV)

    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        if selection:
            self.root.ids.img.source = selection[0]
            print(selection[0])
            self.recognition(selection[0])

    def recognition(self, image):
        # Convert the model
        model = tf.lite.TFLiteConverter.from_keras_model('best_model+815.h5')  # path to the SavedModel directory
        #tflite_model = converter.convert()
        #model = load_model('best_model+815.h5')
        # наименование класса попорядку
        numClass = ['DJI_Inspire_2',
                    'DJI_Matrice_210-RTK',
                    'DJI_Matrice_600_Pro',
                    'DJI_Mavic_Moscow',
                    'DJI_Mavic_Pro_Platinum',
                    'DJI_Phantom_4',
                    'DJI_Phantom_4_Pro_Plus',
                    'DJI_Spark',
                    'Moscow_Noise']

        img_width = 227  # Ширина изображения
        img_height = 227  # Высота изображения

        img = np.array(image)  # переводим в массив
        img = img / 255.0  # нормализуем
        img = np.expand_dims(img, axis=0)  # добавляем дополнительную размерность, так как НС просит размер батч сайза
        listProbablyImg = model.predict(img)

        predClass = np.argmax(listProbablyImg)
        percentClass = round(listProbablyImg[0, predClass] * 100, 2)
        nameClass = numClass[predClass]
        # выводим информацию по распознованию в лейбл
        print("This image belongs to {} class with probability {} %".format(predClass, listProbablyImg))


if __name__ == "__main__":
    ImageClassify().run()
