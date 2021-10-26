import AudioR
import cv2
import os
import numpy as np
import pickle
from PIL import Image
from matplotlib import pyplot as plt


def save_obj(obj, name):
    with open('raskraska/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


# Функция получения цвета в положении клика мышки
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # im = np.array(img)
        x1 = img_np1[y, x, 0]
        y1 = img_np1[y, x, 1]
        z1 = img_np1[y, x, 2]
        xy1 = "%d,%d" % (x, y)
        xy = "%d,%d,%d" % (x1, y1, z1)
        # cv2.circle(img, (x, y), 1, (255, 0, 0), thickness = -1)
        cv2.putText(img, xy1, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)
        elements = AudioR.record_and_recognize_audio(flag=1)
        try:
            os.remove("microphone-results.wav")
        except:
            pass
        # elements = input('Присвойте имя выбранному элементу: ')
        if elements is not None:
            slovarElements[elements] = [x1, y1, z1]
            print(elements)
            print(slovarElements[elements])


def changeColorElement():
    img_np = img_np1.copy()

    changeElement = AudioR.record_and_recognize_audio(flag=2)
    print(changeElement)
    changeColor = AudioR.record_and_recognize_audio(flag=3)
    print(changeColor)
    # если элемент есть в словаре
    if changeElement in slovarElements.keys():
        print(1)
        # и значение цвета есть в словаре
        if changeColor in colors.keys():
            print(2)
            # и на изображении есть элементы с таким  цветом то переопределяем его цвет на новый
            for i in range(height):
                for j in range(width):
                    if (img_np[i, j, :] == slovarElements[changeElement]).all():
                        # print('change')
                        img_np[i, j, :] = colors[changeColor]
    im2 = Image.fromarray(img_np)
    plt.imshow(im2)
    plt.show()

# # Функция для изменения цвета, в соответствии с распознанными командами
# def avto(arr, image_np):
#   for ind,k in enumerate(arr):
#     if k in slovar2.keys():
#       if arr[ind+1] in colors.keys():
#         image_np[image_np[:,:,0] == slovar2[k]] = colors[arr[ind+1]]
#   return image_np

# def save_obj(obj, name):
#     with open('raskraska/'+ name + '.pkl', 'wb') as f:
#         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#
# def load_obj(name):
#     with open('raskraska/' + name + '.pkl', 'rb') as f:
#         return pickle.load(f)

if __name__ == '__main__':

    # загружаем изображение для разметки\\раскраски
    # img = cv2.imread("car.jpg", cv2.IMREAD_GRAYSCALE)
    img = cv2.imread("ironman (1).png", cv2.IMREAD_GRAYSCALE)
    # получаем размеры
    height, width = img.shape
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_np1 = np.array(imageRGB)

    mFlag = 1  # флаг для выхода из цикла при выборе модуля
    while mFlag:
        voice_input = AudioR.record_and_recognize_audio(flag=0)
        print(voice_input)
        try:
            os.remove("microphone-results.wav")
        except:
            pass
        if (voice_input == 'разметка' or voice_input == 'раскраска'):
            mFlag = 0
    #######################################################
    # РАЗМЕТКА #
    #######################################################
    if voice_input == 'разметка':
        print("Этот модуль предназначени для разметки изображения с целью использовния его при раскраске голосом."
              "Для проведения разметки наведите курсор мыши на элемент изображения нажмите левую кнопку мыши и назвите выбранный элемент."
              "Далее название этого элемента будет использована для обращения к области изображения и изменения ее цвета")
        # словарь для наименований элементов изображений
        slovarElements = {}
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
        while True:
            cv2.imshow("image", img)
            if cv2.waitKey(0) & 0xFF == 27:
                cv2.destroyAllWindows()
                break
        with open('iron.txt', 'wb') as out:
            pickle.dump(slovarElements, out)

    #######################################################
    # РАСКРАСКА #
    #######################################################
    if voice_input == 'раскраска':
        print("Этот модуль предназначени раскраски голосом изображения"
              "Назовите элемент и укажите цвет")
        # Создаем словарь частей железного человека с цветами пикселей
        with open('iron.txt', 'rb') as inp:
            slovarElements = pickle.load(inp)
        colors = {'жёлтый': [255, 255, 0],
                  'Жёлтый': [255, 255, 0],
                  'красный': [255, 0, 0],
                  'синий': [0, 0, 255],
                  'зелёный': [0, 255, 0],
                  'голубой': [170, 170, 255],
                  'черный': [0, 0, 0],
                  'чёрный': [0, 0, 0]}
        im2 = Image.fromarray(img_np1)
        plt.imshow(im2)
        plt.show()
        while True:
            img_np = changeColorElement()
            if cv2.waitKey(0) & 0xFF == 27:
                break
