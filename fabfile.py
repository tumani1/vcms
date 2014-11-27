# coding: utf-8

import os
import fabtools

from time import time
from fabric.api import env, roles, run, settings, sudo, cd, local, require, get, put

common_packages = [
    'git', 'python', 'build-essential', 'python-dev',
    'python-setuptools', 'python-pip', 'python-virtualenv',
    'add-apt-repository'
]

env.git_clone = 'git@git.aaysm.com:developers/next_tv.git'

####################################################################
# Environments
def localhost_env():
    "Use the local virtual server"
    env.hosts = ['localhost']
    env.user = 'tumani1'
    env.project_name = 'next_tv'
    env.path = '/home/%(user)s/workspace/%(project_name)s' % env
    env.env = '/home/%(user)s/venv' % env
    env.current_path = '%(path)s/current' % env
    env.releases_path = '%(path)s/releases' % env
    env.req_dir = 'deploy'
    env.pip = '%(env)s/bin/pip' % env
    env.python = '%(env)s/bin/python' % env
    env.shell = '/bin/bash -c'


def production_env():
    pass

####################################################################
def install_common_packages():
    """
    Установка основных общих системных пакетов
    """

    fabtools.deb.install(globals()['common_packages'])


def install_all_repo(**kwargs):
    """
    Установка репозитариев
    """

    run('cat %(repo_file)s | xargs sudo add-apt-repository' % {
        'repo_file': os.path.join(env.current_release, env.req_dir, 'reposytary.txt')
    })

    fabtools.deb.update_index(False)


def install_all_sys_packages(**kwargs):
    """
    Установка системных пакетов
    """

    run('cat %(sys_file)s | xargs sudo apt-get install -y ' % {
        'sys_file': os.path.join(env.current_release, env.req_dir, 'system.txt')
    })


def install_repo_and_packages(install_repo=True, **kwargs):
    """
    Установка системных пакетов с репозитариями
    """

    if install_repo:
        install_all_repo()

    install_all_sys_packages()


def install_packages_to_env(**kwargs):
    """
    Установка python пакетов в окружение
    """

    # Проверка папки окружения
    if not fabtools.python.virtualenv_exists(env.env):
        fabtools.python.create_virtualenv(env.env)

    with cd(env.current_release):
        # Установка python пакетов
        with fabtools.python.virtualenv(env.env):
            run('%(pip)s install -r %(path)s' % {
                'pip': env.pip,
                'path': os.path.join(env.current_release, env.req_dir, 'requirements.txt'),
            })


def deploy(**kwargs):
    require('hosts', provided_by=[localhost_env, production_env])
    require('path')

    install_repo_and_packages(**kwargs)
    install_packages_to_env(**kwargs)
