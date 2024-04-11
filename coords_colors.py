import time

import cv2
import pytesseract
from source.window_screen import Screen
a = time.time()
image = cv2.imread("temp/application_screenshot2.png")
image = image[352-5:372+5, 783-5:834+5]
# Преобразование изображения в черно-белое
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # Применение порогового фильтра
gray_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# Распознавание текста с помощью Tesseract
custom_config = r'--oem 3 --psm 6 outputbase digits'
text = pytesseract.image_to_string(gray_image, config=custom_config)

print(float(text.strip()))

cv2.imshow("g", gray_image)
cv2.waitKey(0)
