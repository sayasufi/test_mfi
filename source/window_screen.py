import logging
import subprocess
import time

import cv2
import numpy as np
import pyautogui
import pytesseract
import easyocr
from tests.dict_for_test import tabs


class Screen:
    def __init__(self):
        logging.info("Откройте окно МФИ...")
        time.sleep(3)
        # Получите идентификатор активного окна с помощью xdotool
        self.active_window_id = int(subprocess.check_output(['xdotool', 'getactivewindow']).decode())

        # Получите информацию об активном окне с помощью xwininfo
        self.xwininfo_output = subprocess.check_output(['xwininfo', '-id', str(self.active_window_id)]).decode()

        self.name = self.xwininfo_output.splitlines()[1].strip()
        self.x = int(self.xwininfo_output.splitlines()[3].split(":")[1].strip())
        self.y = int(self.xwininfo_output.splitlines()[4].split(":")[1].strip())
        self.width = int(self.xwininfo_output.splitlines()[7].split(":")[1].strip())
        self.height = int(self.xwininfo_output.splitlines()[8].split(":")[1].strip())

        self.path_to_png = 'temp/application_screenshot'

    def screen(self):
        # Сделайте скриншот только для определенного окна
        screenshot = pyautogui.screenshot(region=(self.x, self.y, self.width, self.height))

        # Сохраните скриншот в файл
        screenshot.save(f"{self.path_to_png}.png")

    def get_pixel_color(self, x, y):
        # Откройте изображение
        image = cv2.imread(f"{self.path_to_png}.png")

        pixel_color = image[y, x]

        # Выведите RGB значения цвета
        return pixel_color[::-1]

    def img_to_text(self, x1, x2, y1, y2, path=None):

        if path is None:
            image = cv2.imread(f"{self.path_to_png}.png")
        else:
            image = cv2.imread(path)

        image = image[y1-5:y2+5, x1-5:x2+5]

        # Преобразование изображения в черно-белое
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # # Применение порогового фильтра
        # filter_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

        # Создание маски для выделения только чисел
        white_mask = cv2.merge((binary_image, binary_image, binary_image))
        # Создание черного фона для результата
        black_background = np.zeros_like(image)
        # Копирование только чисел на черный фон
        image = cv2.bitwise_and(image, white_mask) + black_background

        # Нахождение контуров
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Создание маски для удаления не черных элементов на границе
        mask = np.zeros_like(gray_image)
        cv2.drawContours(mask, contours, -1, (255), 1)

        # Применение маски к изображению
        result = cv2.bitwise_and(image, image, mask=mask)


        cv2.imshow('filter', image)
        cv2.waitKey(0)


        # Распознавание текста с помощью Tesseract
        custom_config = r'--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789.'

        text = pytesseract.image_to_string(result, config=custom_config, lang='eng').strip()
        return text

        # # Операция эрозии для удаления шума и уменьшения объектов
        # kernel = np.ones((3, 3), np.uint8)
        # eroded_image = cv2.erode(filter_image, kernel, iterations=1)
        # # Операция дилатации для восстановления границ белых чисел в середине
        # dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)
        # # Создание маски только для границ белых чисел
        # edge_mask = cv2.absdiff(dilated_image, eroded_image)
        # # Применение инверсии маски для выделения границ
        # edge_mask_inv = cv2.bitwise_not(edge_mask)
        # # Создание черного фона для результата
        # black_background = np.zeros_like(image)
        # # Копирование только границ белых чисел на черный фон
        # result_image = cv2.bitwise_and(image, image, mask=edge_mask_inv) + black_background

    def get_coordinates(self, path=None):
        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                print(self.get_pixel_color(x, y))
                return x, y
        if path is None:
            image = cv2.imread(f"{self.path_to_png}.png")
        else:
            image = cv2.imread(path)

        cv2.imshow('Image', image)
        cv2.setMouseCallback('Image', click_event)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def change_tab(self, number):
        x = tabs[number]
        y = tabs[number]
        pyautogui.click(x+self.x, y+self.y)
        time.sleep(1)


