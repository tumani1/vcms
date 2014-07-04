#coding: utf-8

import argparse

import settings
from utils.connection import db_connect, create_session


parser = argparse.ArgumentParser(description='Clear database for NextTV service')
parser.add_argument('-t', '--type', dest='type', action='store_true', default='postgresql',
                    help='Run server with test params')

args = parser.parse_args()


while True:
    result = raw_input("Вы уверенны, что хотите очистить базу данных?(Yes/No)")

    if result in ('y', 'Y', 'yes', 'Yes'):
        if not args.type in settings.DATABASE.keys():
            raise Exception('Необходим ключ из конфига базы данных')

        print "Идет очистка базы данных..."
        session = create_session(bind=db_connect(type=args.type))
        session.connection().connection.set_isolation_level(0)
        session.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        session.connection().connection.set_isolation_level(1)

        break

    elif result in ('n', 'N', 'no', 'No'):
        break
