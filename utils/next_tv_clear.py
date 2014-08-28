# coding: utf-8
import argparse

import settings
from utils.connection import db_connect, create_session


parser = argparse.ArgumentParser(description=u'Clear database for NextTV service')
parser.add_argument('-t', '--type', dest='type', action='store_true', default='postgresql',
                    help=u'Run server with test params')
parser.add_argument('-y', '--always-yes', dest='isyes', action='store_true', default=False)

args = parser.parse_args()

result = ''
if not args.isyes:
    result = raw_input(u'Вы уверенны, что хотите очистить базу данных?(Yes/No): '.encode('utf-8'))

if args.isyes or result.lower() in ('y', 'yes', 'Yes', 'Y'):
    if not args.type in settings.DATABASE.keys():
        raise Exception(u'Необходим ключ из конфига базы данных'.encode('utf-8'))

    print u'Начало создания сессии...'.encode('utf-8')
    session = create_session(bind=db_connect(type=args.type))

    print u'Очистка...'.encode('utf-8')
    session.connection().connection.set_isolation_level(0)
    session.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
    session.connection().connection.set_isolation_level(1)
