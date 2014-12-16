# coding: utf-8
from argparse import ArgumentParser
from subprocess import Popen, PIPE
from traceback import print_exc
from time import sleep
from logging import getLogger, DEBUG
from logging.handlers import RotatingFileHandler


logger = getLogger('trasfer')
handler = RotatingFileHandler('transfer.log', maxBytes=10*1024*1024, backupCount=10)
logger.addHandler(handler)
logger.setLevel(DEBUG)


def transfer(source, destination, timeout):
    """Файлы отправляются через ssh, соответственно нужно иметь публичный ключ на удаленном сервере.
     Синхронизируются файлы, которых не существует на удалённом сервере.
     Папки и файлы на хосте-отправителе удаляются.
    """
    while True:
        try:
            command = 'rsync -rv --remove-source-files --ignore-existing -e ssh {0} {1} && rm -rfv {0}*'.format(source, destination)
            child_proc = Popen(command, stdout=PIPE, shell=True)
            output = child_proc.stdout.read()
            logger.info(output)
        except Exception as e:
            logger.error(print_exc())
        sleep(timeout)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-t', '--timeout', dest='timeout', type=int, required=True)
    parser.add_argument('-s', '--source', dest='source', required=True)
    parser.add_argument('-d', '--destination', dest='destination', required=True)
    args = parser.parse_args()

    transfer(args.source, args.destination, args.timeout)