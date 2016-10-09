import socket
import json
from pymongo import MongoClient, DESCENDING
from . import log


def conn():
    db = MongoClient().ss
    cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cli.connect(('127.0.0.1', 6001))
    return db, cli


def close(db, cli):
    db.close()
    cli.close()


def add_port(db, cli, orderId):
    res = db.ss.find().sort('port', DESCENDING)
    port = res[0]['port'] + 1
    passwd = orderId
    try:
        db.ss.insert_one({'orderId': orderId, 'port': port, 'password': passwd, 'used': 0})
    except Exception as e:
        log.exception(e)
        return
    cli.send(b'add: {"server_port":%s, "password":%s}' % (port, passwd))
    data, _ = cli.recvfrom(1506)
    if b'ok' in data:
        log.info("Success add port %s" % port)
        return dict(
            server='45.248.86.101',
            port=port,
            password=passwd,
            method='aes-128-cfb'
        )
    else:
        log.warn("Add port Error")


def remove_port(db, cli, port):
    cli.send(b'remove: {"server_port":%s}' % port)
    data, _ = cli.recvfrom(1506)
    if b'ok' in data:
        log.info("Success remove port %s" % port)
        try:
            db.ss.delete_one({'port': port})
        except Exception as e:
            log.exception(e)
    else:
        log.warn("Remove port Error")


def load_from_sql(db):
    datas = {}
    try:
        for info in db.ss.find():
            datas[int(info['port'])] = info['possword']
        log.info("Success get data from sql")
        return datas
    except Exception as e:
        log.exception(e)


def update_config(db):
    with open('shadowsocks.json', 'r') as f:
        js = json.load(f)
    datas = load_from_sql(db)
    if not datas:
        log.error("Load data from sql error")
        return
    js['port_password'] = datas
    with open('shadowsocks.json', 'w') as f:
        json.dump(js, f)
    log.info("success update shadowsocks.json")


