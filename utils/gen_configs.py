# coding=utf-8
from ConfigParser import ConfigParser as CP
from os import curdir, makedirs
from os.path import exists, abspath, join
from sys import executable
import argparse
import yaml


def path(string):
    r_string = abspath(string)
    if not exists(string):
        makedirs(r_string)
        print('directory created - ' + str(r_string))

    return abspath(string)


def main(h, ha_port, pool, python, project, dest):
    try:
        # генерация групп для zerorpc служб
        pool = range(pool[0], pool[1])
        for N, p in enumerate(pool, start=1):
            config_name = 'zerorpc_service_{N}'.format(N=N)
            sec = 'program:{name}'.format(name=config_name)
            command = '{python} -m zerorpcservice.service --host={host} --port={port}'.format(python=python, host=h, port=p)
            cp = CP()
            cp.add_section(sec)
            cp.set(sec, 'command', command)
            cp.set(sec, 'directory', project)

            with open(join(dest, config_name+'.conf'), 'w') as config:
                cp.write(config)

        # генерация основной части конфига группы listen

        # генерация части haproxy конфига для группы backend
        template = """global
    log /dev/log local0
    stats socket /var/run/haproxy.sock mode 600 level admin
    nbproc 1

defaults
    log  global
    mode tcp
    option tcplog
    option     dontlognull
    timeout connect 500
    timeout client 30000
    timeout server 30000

listen haproxy {host}:{port}
    mode tcp
    option tcplog
    balance roundrobin
    retries 3
    maxconn 20000
    default_backend zeronodes

backend zeronodes\n""".format(host=h, port=ha_port)
        for p in pool:
            template += '\tserver backend_{N} {host}:{port}\n'.format(N=p, host=h, port=p)

        with open(join(dest, 'haproxy.conf'), 'w') as config:
            config.write(template)

        # генерация группы haproxy
        sec = 'program:haproxy'
        cp = CP()
        cp.add_section(sec)
        cp.set(sec, 'command', 'haproxy -f {project}/configs/haproxy.conf'.format(project=project))

        with open(join(dest, 'pr_haproxy.conf'), 'w') as config:
                cp.write(config)

        # генерация конфига для node служб
        conf = {'render_serv': {
                    'host': '127.0.0.1',
                    'port': 9901,
                    'template_dir': 'templates'},
                'rest_ws_serv': {
                    'host': '127.0.0.1',
                    'port': 9902}}
        conf['render_serv']['haproxy'] = {'host':h, 'port':ha_port}
        conf['rest_ws_serv']['haproxy'] = {'host':h, 'port':ha_port}

        with open(join(dest, 'node_service.yaml'), 'w') as config:
            yaml.dump(conf, config)
    except Exception as e:
        raise e


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='генератор конфигов')
    parser.add_argument('--host', dest='h', default='127.0.0.1', metavar='<host>')
    parser.add_argument('--ha_port', dest='ha_port', type=int, default=6700, metavar='<port>')
    parser.add_argument('--project', dest='project', type=path, default=curdir, metavar='<path>',
                        help='путь корня проекта')
    parser.add_argument('--port_pool', dest='pool', nargs=2, type=int, default=[6600, 6608], metavar='<port>',
                        help='два значения - начало и конец промежутка портов, напр. --port_pool 6000 6008')
    parser.add_argument('--python', dest='python', type=path, default=executable, metavar='<path>',
                        help='путь и имя исполняемого файла питона из виртуального окружения')
    parser.add_argument('--destination', dest='dest', type=path, default='generated_configs', metavar='<path>',
                        help='путь выгрузки сгенерированных конфигов')
    namespace = parser.parse_args()
    main(**vars(namespace))