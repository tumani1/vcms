# coding: utf-8
from argparse import ArgumentParser

from admin.main import start_admin_application
from zerorpcserver.server import start_zerorpc_services
from models import Base
from connectors import db_connect


def start_syncdb(**options):
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

    syncdb_c = subparser.add_parser('syncdb', help='Create database')
    syncdb_c.set_defaults(func=start_syncdb)

    zerorpc_server_c = subparser.add_parser('zerorpcserver', help='Start ZeroRpcServer')
    zerorpc_server_c.set_defaults(func=start_zerorpc_services)

    options = parser.parse_args()
    dict_opt = vars(options)
    func = dict_opt.pop('func')
    if func:
        func(**dict_opt)