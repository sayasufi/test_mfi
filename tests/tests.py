import logging
import threading
import time

import pandas as pd

from source.udp import S_UDP_PACK_ODS_DATA
from source.unions import dict_to_byte
from source.window_screen import Screen
from dict_for_test import sds3X_dict, arinc_dict


def valid_color(screen_color, manual_color):
    if abs(screen_color[0] - manual_color[0]) < 5 and abs(screen_color[1] - manual_color[1]) < 5 and abs(
            screen_color[2] - manual_color[2]) < 5:
        return True
    else:
        return False


class TestOneTimeCommands:
    def __init__(self):
        self.screen = Screen()
        self.udp = S_UDP_PACK_ODS_DATA()
        self.default_pack = self.udp.get_package()
        self.flag = True
        self.df = pd.DataFrame(columns=["Имя", "Переменная", "Включено", "Пройдена ли проверка"])

    def send_data(self, pack_in):
        while self.flag:
            self.udp.send(pack_in)
            time.sleep(0.01)

    def test_sds3X(self):
        for key, value in sds3X_dict.items():
            # Запуск цикла в отдельном потоке
            if value:
                # Выключено
                self.flag = True
                send_thread = threading.Thread(target=self.send_data, args=(self.default_pack,))
                send_thread.start()
                time.sleep(0.5)
                self.screen.screen()
                rgb = self.screen.get_pixel_color(value[0], value[1])
                temp_dict = {"Имя": value[4],
                             "Переменная": key,
                             "Включено": "Нет",
                             "Пройдена ли проверка": None}
                if valid_color(rgb, value[2]):
                    logging.info(f"'{value[4]}' - выключено: Пройдено")
                    temp_dict["Пройдена ли проверка"] = "Да"
                else:
                    logging.info(f"'{value[4]}' - выключено: Не пройдено")
                    temp_dict["Пройдена ли проверка"] = "Нет"
                temp_df = pd.DataFrame(temp_dict, index=[0])
                self.df = pd.concat([self.df, temp_df], ignore_index=True)
                self.df.to_csv("data/data.csv", index=False)
                self.flag = False
                send_thread.join()

                # Включено
                self.flag = True
                self.udp.unions.sds3X[key] = 1
                self.udp.unions.sds3X_data = dict_to_byte(self.udp.unions.sds3X)
                self.udp.udp["sds3X"] = int.from_bytes(self.udp.unions.sds3X_data, byteorder='little')
                pack = self.udp.get_package()
                send_thread = threading.Thread(target=self.send_data, args=(pack,))
                send_thread.start()
                time.sleep(0.5)
                self.screen.screen()
                rgb = self.screen.get_pixel_color(value[0], value[1])
                temp_dict = {"Имя": value[4],
                             "Переменная": key,
                             "Включено": "Да",
                             "Пройдена ли проверка": None}
                if valid_color(rgb, value[3]):
                    logging.info(f"'{value[4]}' - включено: Пройдено")
                    temp_dict["Пройдена ли проверка"] = "Да"
                else:
                    logging.info(f"'{value[4]}' - включено: Не пройдено")
                    temp_dict["Пройдена ли проверка"] = "Нет"
                temp_df = pd.DataFrame(temp_dict, index=[0])
                self.df = pd.concat([self.df, temp_df], ignore_index=True)
                self.df.to_csv("data/data.csv", index=False)
                self.flag = False
                send_thread.join()
                self.udp.unions.sds3X[key] = 0
                self.udp.unions.sds3X_data = dict_to_byte(self.udp.unions.sds3X)
                self.udp.udp["sds3X"] = int.from_bytes(self.udp.unions.sds3X_data, byteorder='little')


class TestArincCommands:
    def __init__(self):
        self.screen = Screen()
        self.udp = S_UDP_PACK_ODS_DATA()
        self.default_pack = self.udp.get_package()
        self.flag = True
        self.df = pd.DataFrame(columns=["Имя", "Переменная", "Включено", "Пройдена ли проверка"])

    def send_data(self, pack_in):
        while self.flag:
            self.udp.send(pack_in)
            time.sleep(0.01)

    for key, value in arinc_dict.items():
