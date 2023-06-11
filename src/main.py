import sys
from models import create_tables
from utils import bot


def run():
    bot.polling()


if __name__ == '__main__':
    if sys.argv[1] == 'create_tables':
        create_tables()
    elif sys.argv[1] == 'run':
        run()
