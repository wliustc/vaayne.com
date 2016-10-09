import os
from flask import request, jsonify
from . import ss, manager, log


@ss.route('/add')
def add():
    orderId = request.get_data('orderId')
    try:
        db, cli = manager.conn()
        info = manager.add_port(db, cli, orderId)
        manager.update_config(db)
        manager.close(db, cli)
        return jsonify(info)
    except Exception as e:
        log.exception(e)
        return jsonify(
            state='error',
            msg=e
        )


@ss.route('/del')
def delete():
    try:
        port = request.get_data('port')
        db, cli = manager.conn()
        manager.remove_port(db, cli, port)
        manager.update_config(db)
        manager.close(db, cli)
        return jsonify(
            state=200,
            msg="Success delete port %s" % port
        )
    except Exception as e:
        log.exception(e)
        return jsonify(
            state='error',
            msg=e
        )


@ss.route('/restart')
def restart():
    db, cli = manager.conn()
    manager.update_config(db)
    manager.close(db, cli)
    os.system('ssserver --manager-address 127.0.0.1:6001 -c shadowsocks.json --user vaayne -d start')
    return os.system('sudo less /var/log/shadowsocks.log')

