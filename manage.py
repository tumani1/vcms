# coding: utf-8
from argparse import ArgumentParser
from admin.main import start_application

from models import Base
from connectors import db_connect


def start_admin(options):
    start_application(host=options.host, port=options.port, debug=options.debug)


def start_syncdb(options):
    Base.metadata.create_all(bind=db_connect())

if __name__ == '__main__':
    parser = ArgumentParser(usage='manage.py subcommand [options] [args]')

    subparser = parser.add_subparsers(title='Commands')
    admin_c = subparser.add_parser('admin', help='Start sites admin')
    admin_c.add_argument('-p', '--port', metavar='PORT', type=int, help='Port to start admin', default=5000)
    admin_c.add_argument('-H', '--host', metavar='HOST', help='Host to start admin', default='127.0.0.1')
    admin_c.add_argument('--debug', dest='debug', action='store_true')
    admin_c.add_argument('--no-debug', dest='debug', action='store_false')
    admin_c.set_defaults(func=start_admin, debug=True)

    syncdb_c = subparser.add_parser('syncdb', help='Create database')
    syncdb_c.set_defaults(func=start_syncdb)

    options = parser.parse_args()
    options.func(options)