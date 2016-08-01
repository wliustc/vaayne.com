# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/21 09:42 

import hashlib

diac = {
    'username': 'Vaayne',
    'email': 'lyishaou@gmail.com',
    'password': 'Passwd',
    'hash_passwd': '1a7dcac1e378896ddaefd39463c4f600'
}

hass = hashlib.md5('Passwd').hexdigest()

print diac
