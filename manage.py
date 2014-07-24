# coding: utf-8
from argparse import ArgumentParser

from fabric.api import local

from admin.main import start_admin_application
from zerorpcserver.service import run_zerorpc
from models import Base
from utils.connection import db_connect
from zerorpcserver.service import ZeroRpcService
from functools import partial


def local_db_reset():
    '''Перезаписать локальную базу из репозитория
    '''
    local('''echo "DROP DATABASE IF EXISTS next_tv;" | sudo  sudo -u postgres psql''')
    local('''echo "CREATE USER pgadmin WITH PASSWORD 'qwerty'; CREATE DATABASE next_tv; GRANT ALL PRIVILEGES ON DATABASE next_tv to pgadmin;" | sudo  sudo -u postgres psql''')


def delete_tables(**options):
    Base.metadata.drop_all(bind=db_connect())


def create_tables(**options):
    Base.metadata.create_all(bind=db_connect())


def db_reset(**options):
    Base.metadata.drop_all(bind=db_connect())
    Base.metadata.create_all(bind=db_connect())


if __name__ == '__main__':
    parser = ArgumentParser(usage='manage.py subcommand [options] [args]')

    subparser = parser.add_subparsers(title='Commands')
    admin_c = subparser.add_parser('admin', help='Start sites admin')
    admin_c.add_argument('-p', '--port', metavar='PORT', type=int, help='Port to start admin', default=5000)
    admin_c.add_argument('-H', '--host', metavar='HOST', help='Host to start admin', default='127.0.0.1')
    admin_c.add_argument('--debug', dest='debug', action='store_true', help='Run admin in debug mode')
    admin_c.add_argument('--no-debug', dest='debug', action='store_false', help='Run admin without debug mode')
    admin_c.set_defaults(func=start_admin_application, debug=True)

    local_db_reset_c = subparser.add_parser('local_db_reset', help='Сносит БД, создает пользователя и новую БД, добавляет права пользователю на эту БД')
    local_db_reset_c.set_defaults(func=local_db_reset)

    syncdb_c = subparser.add_parser('syncdb', help='Create tabels')
    syncdb_c.set_defaults(func=create_tables)

    drop_all_c = subparser.add_parser('dropdb', help='Delete all tabels')
    drop_all_c.set_defaults(func=delete_tables)

    reset_c = subparser.add_parser('resetdb', help='Local database reset')
    reset_c.set_defaults(func=db_reset)

    zerorpc_server_c = subparser.add_parser('zerorpcserver', help='Start ZeroRpcServer')
    zerorpc_server_c.set_defaults(func=partial(run_zerorpc, ZeroRpcService))

    options = parser.parse_args()
    dict_opt = vars(options)
    func = dict_opt.pop('func')
    if func:
        func(**dict_opt)
