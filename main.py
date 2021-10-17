from kivymd.app import MDApp
from kivy.lang import Builder
from plyer import filechooser
import numpy as np
from tensorflow.keras.models import load_model # из кераса подгружаем  метод загрузки предобученной модели
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

    def recognition(image):
        model = load_model('First/best_model+815.h5')
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

        #img_path = '2450MHz_12.5MSps_17.05.2021_11-24-03_duration=37.1917ms_feature_type=fft_spectrogram_6.png'  # путь к отдельному экземпляру данных
        #img = image.load_img(filename, target_size=(img_height, img_width))  # загружаем фото в переменную
        #img = Image.crop(0,0,img_height,img_width)
        img = np.array(image)  # переводим в массив
        img = img / 255.0  # нормализуем
        img = np.expand_dims(img, axis=0)  # добавляем дополнительную размерность, так как НС просит размер батч сайза
        listProbablyImg = model.predict(img)

        predClass = np.argmax(listProbablyImg)
        percentClass = round(listProbablyImg[0,predClass]*100,2)
        nameClass = numClass[predClass]
        # выводим информацию по распознованию в лейбл
        text_elem.update("This image belongs to {} class with probability {} %".format(predClass, listProbablyImg))

if __name__ == "__main__":
    ImageClassify().run()