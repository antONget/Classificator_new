import cv2

# img = cv2.imread('car.jpg')
img = cv2.imread("car.jpg", cv2.IMREAD_GRAYSCALE)
ret, thresh = cv2.threshold(img, 84, 255, 0)
countours, hierarchy = cv2.findContours(thresh, 1, 2)

print(countours[200])
# img = cv2.drawContours(img, countours, 500, (0, 0, 255), 3)
cv2.imshow("image", cv2.drawContours(img, countours, -1, (0, 0, 255), 1))
cv2.waitKey(0)