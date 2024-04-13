from datetime import datetime

from logs.logger import setup_logging
from tests.tests import TestOneTimeCommands, TestArincCommands


def main():
    setup_logging(f"logs/{datetime.now().strftime('%d.%m.%y')}/{datetime.now().time().strftime('%Hh_%Mm_%Ss')}.log")
    test1 = TestArincCommands()
    test1.test_arinc_data()



if __name__ == '__main__':
    main()
