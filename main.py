import os
import socket
import sqlite3
from slacker import IncomingWebhook


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
    (ip, port) = list(map(str.strip, parse_host(host)))

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


conn = sqlite3.connect('hosts.sqlite3')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS dead_hosts (host TEXT PRIMARY KEY)''')
conn.commit()
hosts = get_hosts()
slack = IncomingWebhook(url=os.environ['webhook_url'])
for host in hosts:
    cursor.execute("SELECT host FROM dead_hosts WHERE host='{}'".format(host))

    if tcp_open(host):
        if cursor.fetchone() is not None:
            cursor.execute("DELETE FROM dead_hosts WHERE host='{}'".format(host))
            conn.commit()
            slack.post({
                "attachments": [{
                    "author_name": host,
                    "title": ":relieved: 서비스 정상화",
                }]
            })
    elif cursor.fetchone() is None :
        cursor.execute("INSERT INTO dead_hosts (host) VALUES ('{}')".format(host))
        conn.commit()
        slack.post({
            "attachments": [{
                "author_name": host,
                "title": ":fearful: 서비스 접속 불가",
            }]
        })

cursor.close()
conn.close()
