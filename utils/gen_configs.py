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


def main(h, worker_pool, rest_ws_pool, render_pool, python, project, dest, without_node):
    try:
        # генерация группы для zerorpc служб

        worker_pool = range(worker_pool[0], worker_pool[1])
        wp_p1, wp_p2 = worker_pool[:len(worker_pool)/2], worker_pool[len(worker_pool)/2:]
        rest_ws_pool = range(rest_ws_pool[0], rest_ws_pool[1])
        render_pool = range(render_pool[0], render_pool[1])
        if len(wp_p1) != len(rest_ws_pool) or len(wp_p2) != len(render_pool):
            raise ValueError("Размеры пулов должны быть равны")

        with open(join(dest, 'vcms.conf'), 'w') as config:

            programs = []
            for N, p in enumerate(worker_pool, start=1):
                config_name = 'w{N}'.format(N=N)
                section = 'program:{name}'.format(name=config_name)
                command = '{python} -m zerorpcservices.rest_service --host={} --port={}'.format(h, p, python=python)
                cp = CP()
                cp.add_section(section)
                cp.set(section, 'command', command)
                cp.set(section, 'directory', project)
                cp.write(config)
                programs.append(config_name)

            cp = CP()
            section = 'group:workers'
            cp.add_section(section)
            cp.set(section, 'programs', ', '.join(programs))
            cp.write(config)

        # генерация группы rest_ws служб
            programs = []
            for N, ports in enumerate(zip(rest_ws_pool, wp_p1), start=1):
                config_name = 'rws{N}'.format(N=N)
                section = 'program:{name}'.format(name=config_name)
                command = 'nodejs app.js --host={} --port={} --backend_host={} --backend_port={}'.format(h, ports[0], h, ports[1])
                cp = CP()
                cp.add_section(section)
                cp.set(section, 'command', command)
                cp.set(section, 'directory', join(project, 'nodeservices', 'rest_ws_service'))
                cp.write(config)
                programs.append(config_name)

            cp = CP()
            section = 'group:rest_ws_services'
            cp.add_section(section)
            cp.set(section, 'programs', ', '.join(programs))
            cp.write(config)

        # генерация группы render служб
            programs = []
            for N, ports in enumerate(zip(render_pool, wp_p2), start=1):
                config_name = 'rnd{N}'.format(N=N)
                section = 'program:{name}'.format(name=config_name)
                command = 'nodejs app.js --host={} --port={} --backend_host={} --backend_port={}'.format(h, ports[0], h, ports[1])
                cp = CP()
                cp.add_section(section)
                cp.set(section, 'command', command)
                cp.set(section, 'directory', join(project, 'nodeservices', 'render_service'))
                cp.write(config)
                programs.append(config_name)

            cp = CP()
            section = 'group:render_services'
            cp.add_section(section)
            cp.set(section, 'programs', ', '.join(programs))
            cp.write(config)

        print('vcms.conf is wrote')

        # генерация конфига для node служб
        if not without_node:
            conf = {'render_serv': {
                        'host': h,
                        'port': render_pool[0],
                        'template_dir': 'templates',
                        'backend': {'host': h, 'port': worker_pool[0]}},
                    'rest_ws_serv': {
                        'host': h,
                        'port': rest_ws_pool[0],
                        'backend': {'host': h, 'port': worker_pool[0]}}
                    }
            # если нужно повешать на прослушивание ip, а не localhost
            # conf['render_serv']['backend'] = {'host':get_lan_ip(), 'port':ha_port}
            # conf['rest_ws_serv']['backend'] = {'host':get_lan_ip(), 'port':ha_port}

            with open(join(dest, 'node_service.yaml'), 'w') as config:
                yaml.dump(conf, config)
            print('node_service.yaml is wrote')

    except Exception as e:
        raise e


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ГЕНЕРИРУЕТ КОНФИГИ ДЛЯ ENGINE WORKER, NODEJS_REST_WS, NODE_RENDER, SUPERVISOR.'
                                                 ' ВСЕ ПАРАМЕТРЫ ИМЕЮТ ЗНАЧЕНИЕ ПО УМОЛЧАНИЮ. ')
    parser.add_argument('--host', dest='h', default='127.0.0.1', metavar='<host>',
                        help='адрес, на котором будут запускаться большинство служб')
    parser.add_argument('--project', dest='project', type=path, default=curdir, metavar='<path>',
                        help='путь корня проекта')
    parser.add_argument('--worker_pool', dest='worker_pool', nargs=2, type=int, default=[6600, 6608], metavar='<port> <port>',
                        help='два значения - начало и конец промежутка портов, напр. --port_pool 6600 6608. '
                             'По ним генерируется количество ZeroRPC служб')
    parser.add_argument('--rest_ws_pool', dest='rest_ws_pool', nargs=2, type=int, default=[5500, 5504], metavar='<port> <port>',
                        help='два значения - начало и конец промежутка портов, напр. --port_pool 5500 5504. '
                             'По ним генерируется количество NODEJS_REST_WS служб')
    parser.add_argument('--render_pool', dest='render_pool', nargs=2, type=int, default=[5400, 5404], metavar='<port> <port>',
                        help='два значения - начало и конец промежутка портов, напр. --port_pool 5400 5404. '
                             'По ним генерируется количество NODEJS_RENDER служб')
    parser.add_argument('--python', dest='python', type=path, default=executable, metavar='<path>',
                        help='путь и имя исполняемого файла питона из виртуального окружения')
    parser.add_argument('--destination', dest='dest', type=path, default='generated_configs', metavar='<path>',
                        help='путь выгрузки сгенерированных конфигов')
    parser.add_argument('--without_node', action='store_true', dest='without_node',
                        help='необходимо ли генерировать конфиг для node сервисов')
    namespace = parser.parse_args()
    main(**vars(namespace))