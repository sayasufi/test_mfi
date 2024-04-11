import logging
import subprocess
import time

import cv2
import pyautogui
import pytesseract


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

        image = image[x1 - 5:x2 + 5, y1 - 5:y2 + 5]
        # Преобразование изображения в черно-белое
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # # Применение порогового фильтра
        filter_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Распознавание текста с помощью Tesseract
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        text = pytesseract.image_to_string(filter_image, config=custom_config)

        return text.strip()

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
