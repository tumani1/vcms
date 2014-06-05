# coding: utf-8
from fabric.api import local

def local_db_reset():
    '''
    Перезаписать локальную базу из репозитория
    '''
    local('''echo "DROP DATABASE next_tv;" |  sudo  sudo -u postgres psql''')
    local('''echo "CREATE USER pgadmin WITH PASSWORD 'qwerty'; CREATE DATABASE next_tv; GRANT ALL PRIVILEGES ON DATABASE next_tv to pgadmin;" | sudo  sudo -u postgres psql''')

