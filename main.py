from datetime import datetime

from logs.logger import setup_logging
from tests.test_one_time import TestOneTimeCommands


def main():
    setup_logging(f"logs/{datetime.now().strftime('%d.%m.%y')}/{datetime.now().time().strftime('%Hh_%Mm_%Ss')}.log")
    test1 = TestOneTimeCommands()
    test1.test_sds3X()



if __name__ == '__main__':
    main()
