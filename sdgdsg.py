import threading
import time

from source.udp import S_UDP_PACK_ODS_DATA
from source.window_screen import Screen


def send_data(pack_in):
    while True:
        udp.send(pack_in)
        time.sleep(0.01)

udp = S_UDP_PACK_ODS_DATA()
pack = udp.get_package()
send_thread = threading.Thread(target=send_data, args=(pack,))
send_thread.start()

screen = Screen()
screen.screen()
time.sleep(5)
screen.screen()
time.sleep(5)
screen.screen()
time.sleep(5)

