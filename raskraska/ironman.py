import cv2
import matplotlib
import numpy as np
from docutils.nodes import inline
from scipy.misc import toimage
from scipy.misc import imshow
from PIL import Image

from matplotlib import pyplot as plt
# %matplotlib inline
# загрузка изображения
# img = cv2.imread('ironman (1).png')
img = cv2.imread("car.jpg", cv2.IMREAD_GRAYSCALE)
# получаем размеры
height, width = img.shape
#
imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_np1 = np.array(imageRGB)

slovarElements = {}


# Функция получения цвета в положении клика мышки
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        #im = np.array(img)
        x1 = img_np1[y, x, 0]
        y1 = img_np1[y, x, 1]
        z1 = img_np1[y, x, 2]
        xy1 = "%d,%d" % (x, y)
        xy = "%d,%d,%d" % (x1, y1, z1)
        #cv2.circle(img, (x, y), 1, (255, 0, 0), thickness = -1)
        cv2.putText(img, xy1, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0,0,0), thickness = 1)
        cv2.imshow("image", img)

        elements = input('Присвойте имя выбранному элементу: ')
        slovarElements[elements] = [x1, y1, z1]
cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)

while(1):
    cv2.imshow("image", img)
    if cv2.waitKey(0)&0xFF==27:
        cv2.destroyAllWindows()
        break

print(slovarElements)
# Создаем словарь цветов в формате png
colors2 = {'жёлтый' :[255, 255, 0],
           'Жёлтый' :[255, 255, 0],
           'красный':[255, 0, 0],
           'синий'  :[0, 0, 255],
           'зелёный':[0, 255, 0],
           'голубой':[170, 170, 255],
           'черный' :[0, 0, 0],
           'чёрный' :[0, 0, 0]}

# img_np = img_np1.copy()
def changeColorElement():
    img_np = img_np1.copy()
    changeElement = input('Какой элемент изменить: ')
    changeColor = input('На какой цвет изменить: ')
    # если элемент есть в словаре
    if changeElement in slovarElements.keys():
        print(1)
        # и значение цвета есть в словаре
        if changeColor in colors2.keys():
            print(2)
            # img_np[img_np[:, :, :] == slovarElements[changeElement]] = colors2[changeColor]
            # и на изображении есть элементы с таким  цветом то переопределяем его цвет на новый
            for i in range(height):
                for j in range(width):
                    if (img_np[i, j, :] == slovarElements[changeElement]).all():
                        print('change')
                        img_np[i, j, :] = colors2[changeColor]
                        #img_np[i, j, 1] = colors2[changeColor][1]
                        #img_np[i, j, 2] = colors2[changeColor][2]

    # print(img_np[251,348])
    # cv2.imshow("image", img_np)
    # img_np = img_np[230:309,173:234,:]
    im2 = Image.fromarray(img_np)

    plt.imshow(im2)

    # plt.savefig('saved_figure.png')
    plt.show()


while(1):
    img_np = changeColorElement()
    # cv2.imshow("image", img_np)
    if cv2.waitKey(0) & 0xFF==27:
        #cv2.destroyAllWindows()
        break

