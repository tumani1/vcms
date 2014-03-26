# coding: utf-8
from fabric.api import env,roles, run, settings, sudo, cd,local, task
import fabric
from fabtools import require
import fabtools
from  fabtools.postgres import user_exists
from next_tv import settings as app_settings
env.hosts = ['123.123.1.1'] # Some remote hosts ip
env.hosts = ['188.226.191.166',]


@task
def setup_db_locally():
    database_vars = app_settings.DATABASES['default']
    local('''createdb --owner %(USER)s \
                      -U %(USER)s \
                      -W %(NAME)s''' % database_vars)
