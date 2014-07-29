# coding=utf-8
import argparse
import yaml
import socket
import fcntl
import struct
from ConfigParser import ConfigParser as CP
from os import curdir, makedirs
from os.path import exists, abspath, join
from sys import executable


def get_lan_ip():
    """возвращает строку с IP адресом, используя низкоуровневую магию"""
    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127."):
        interfaces = ["eth0", "eth1", "eth2", "wlan0", "wlan1", "wifi0","ath0", "ath1", "ppp0"]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


def path(string):
    """Удобный пользовательский тип для значений аргументов, которые обозначают директорию."""
    r_string = abspath(string)
    if not exists(string):
        makedirs(r_string)
        print('directory created - ' + str(r_string))

    return abspath(string)


def main(h, ha_port, ha_stat_port, pool, python, project, dest):
    try:
        # генерация группы для zerorpc служб
        pool = range(pool[0], pool[1])
        with open(join(dest, 'zerorpc_services.conf'), 'w') as config:

            programs = []
            for N, p in enumerate(pool, start=1):
                config_name = 'zerorpc_service_{N}'.format(N=N)
                section = 'program:{name}'.format(name=config_name)
                command = '{python} -m zerorpcservices.rest_service --host={host} --port={port}'.format(python=python, host=h, port=p)
                cp = CP()
                cp.add_section(section)
                cp.set(section, 'command', command)
                cp.set(section, 'directory', project)
                cp.write(config)
                programs.append(config_name)

            cp= CP()
            section = 'group:zerorpc_services'
            cp.add_section(section)
            cp.set(section, 'programs', ', '.join(programs))
            cp.write(config)

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

listen haproxy {host}:{ha_port}
    mode tcp
    option tcplog
    balance roundrobin
    retries 3
    maxconn 20000
    default_backend zeronodes

listen stats {host}:{ha_stat_port}
    mode http
    balance
    timeout client 5000
    timeout connect 4000
    timeout server 30000

    stats uri /haproxy_stats
    stats realm HAProxy\ Statistics
    stats admin if TRUE

backend zeronodes\n""".format(host=get_lan_ip(), ha_port=ha_port, ha_stat_port=ha_stat_port)

        for p in pool:
            template += '\tserver backend_{N} {host}:{port}\n'.format(N=p, host=h, port=p)

        with open(join(dest, 'haproxy.conf'), 'w') as config:
            config.write(template)

        # генерация группы haproxy
        section = 'program:haproxy'
        cp = CP()
        cp.add_section(section)
        cp.set(section, 'command', 'haproxy -f /etc/haproxy/haproxy.conf')

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
        conf['render_serv']['backend'] = {'host':get_lan_ip(), 'port':ha_port}
        conf['rest_ws_serv']['backend'] = {'host':get_lan_ip(), 'port':ha_port}

        with open(join(dest, 'node_service.yaml'), 'w') as config:
            yaml.dump(conf, config)

        #геренерация главного конфига супервизора
        template = """[unix_http_server]
file=/var/run/supervisor.sock
chmod=0700

[inet_http_server]
port={host}:9001

[supervisord]
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid
childlogdir=/var/log/supervisor

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///var/run/supervisor.sock

[include]
files = /etc/supervisor/conf.d/*.conf

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface""".format(host=get_lan_ip())
        with open(join(dest, 'supervisord.conf'), 'w') as config:
            config.write(template)

    except Exception as e:
        raise e


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ГЕНЕРИРУЕТ КОНФИГИ ДЛЯ ZERORPC СЛУЖБ, NODEJS_REST_WS, HAPROXY, SUPERVISOR.'
                                                 ' ВСЕ ПАРАМЕТРЫ ИМЕЮТ ЗНАЧЕНИЕ ПО УМОЛЧАНИЮ. ')
    parser.add_argument('--host', dest='h', default='127.0.0.1', metavar='<host>',
                        help='адрес, на котором будут запускаться большинство служб')
    parser.add_argument('--ha_port', dest='ha_port', type=int, default=6700, metavar='<port>',
                        help='порт для балансировщика')
    parser.add_argument('--ha_stat_port', dest='ha_stat_port', type=int, default=6710, metavar='<port>',
                        help='порт, на котором будет запущен веб-интерфейс балансировщика')
    parser.add_argument('--project', dest='project', type=path, default=curdir, metavar='<path>',
                        help='путь корня проекта')
    parser.add_argument('--port_pool', dest='pool', nargs=2, type=int, default=[6600, 6608], metavar='<port>',
                        help='два значения - начало и конец промежутка портов, напр. --port_pool 6000 6008. '
                             'По ним генерируется количество ZeroRPC служб')
    parser.add_argument('--python', dest='python', type=path, default=executable, metavar='<path>',
                        help='путь и имя исполняемого файла питона из виртуального окружения')
    parser.add_argument('--destination', dest='dest', type=path, default='generated_configs', metavar='<path>',
                        help='путь выгрузки сгенерированных конфигов')
    namespace = parser.parse_args()
    main(**vars(namespace))