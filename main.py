import os
import socket
from datetime import datetime


def get_hosts():
    return os.environ['hosts'].split(',')


def parse_host(host):
    split_port = host.split(':')

    if len(split_port) > 2 or len(split_port) < 1:
        raise ValueError('Invalid host')

    elif len(split_port) == 1:
        split_port.append('80')

    return tuple(split_port)


def tcp_open(host):
    (ip, port) = parse_host(host)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()


hosts = get_hosts()

for host in hosts:
    time = datetime.now()

    if tcp_open(host):
        print('{}: {} is open'.format(time, host))
    else:
        print('{}: {} is not open'.format(time, host))
