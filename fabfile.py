# coding: utf-8
from fabric.api import env,roles, run, settings, sudo, cd,local, task
import fabric
from fabtools import require, deb, postgres, git
from fabtools.python import virtualenv
import fabtools
from next_tv import settings as app_settings

env.hosts = ['123.123.1.1'] # Some remote hosts ip
env.hosts = ['188.226.191.166',]
env.user = 'root'
env.shell= "/bin/bash -c"

env.project_name = 'next_tv'
env.project_path = '/var/www/next_tv'
env.project_current_path = '/var/www/next_tv/current'
env.server_user = 'www-data'
env.server_group = 'www-data'

repo = 'git@git.aaysm.com:developers/next_tv.git'
branch = 'master'
db_name = 'next_tv'
db_user = 'pgadmin'
db_password = 'qwerty'
virtualenv_path = '/home/virtualenv/next_tv'
def setup_db_locally():
    database_vars = app_settings.DATABASES['default']
    local('''createdb --owner %(USER)s \
                      -U %(USER)s \
                      -W %(NAME)s''' % database_vars)


def _setup_packages():

    # Require some Debian/Ubuntu packages
    require.deb.packages([
        'libxml2-dev',
        'mercurial',
        'memcached',
        'libmemcached-dev',
        'zlib1g-dev',
        'libssl-dev',
        'python-dev',
        'build-essential',
        'libjpeg-dev',
        'libfreetype6-dev',
        'zlib1g-dev',
        'libpng12-dev',
        'libpq-dev'
    ])
def _create_db():
    if not postgres.user_exists(db_user):
        require.postgres.user(db_user, db_password)

    if not postgres.database_exists(db_name):
        require.postgres.database(db_name, db_user)

def _init_directories():
    """Create initial directories."""
    print('\n\nCreating initial directories...')
    sudo('mkdir -p %(project_path)s/config' % env)
    sudo('chown -R %(server_user)s:%(server_group)s '
         '%(project_path)s' % env)

def setup():
    _setup_packages()
    _create_db()
    _init_directories()
    require.python.virtualenv(virtualenv_path)

def _deploy_code():
    current_path = '/var/www/%(project_name)s' % env
    with cd(current_path):
        fabtools.require.git.working_copy(repo,
                                          branch=branch,
                                          path='current',
                                          update=True,
                                          use_sudo=True,
                                          user='www-data')

def _create_symlink():
    config_files = []
    config_files.append({
        'source': '/var/www/%(project_name)s/config/db.ini' % env,
        'destination': '/var/www/%(project_name)s/current/configs/db.ini' % env
    })

    config_files.append({
        'source': '/var/www/%(project_name)s/config/uwsgi.ini' % env,
        'destination': '/var/www/%(project_name)s/current/configs/uwsgi.ini' % env
    })

    config_files.append({
        'source':  '/var/www/%(project_name)s/config/settings_local.py' % env,
        'destination':  '/var/www/%(project_name)s/current/%(project_name)s/settings_local.py' % env
    })

    for config_file in config_files:
        if not fabtools.files.is_link(config_file['destination']):
            fabtools.files.symlink(config_file['source'],
                                   config_file['destination'],
                                   use_sudo=False)

def _update_requirements():
    with virtualenv(virtualenv_path):
        fabtools.python.install_requirements('%(project_path)s/current/requirements/prod.txt' % env)

def _syncdb():
    with virtualenv(virtualenv_path):
        with cd(env.project_current_path):
            run('python manage.py syncdb  --noinput ')

def _migrate():
    with virtualenv(virtualenv_path):
        with cd(env.project_current_path):
            run('python manage.py migrate --noinput --no-initial-data')

def _collectstatic():
    with virtualenv(virtualenv_path):
        with cd(env.project_current_path):
            run('python manage.py collectstatic --dry-run --noinput')

def _restart_supervisor():
    pass

def deploy():
    _deploy_code()
    _update_requirements()
    _create_symlink()
    _syncdb()
    _migrate()
    _collectstatic()
