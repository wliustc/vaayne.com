# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/06 17:14 

from pprint import PrettyPrinter
import json

pp = PrettyPrinter(indent=4)

with open('public.json') as f:
    con = f.readlines()
    for item in con:
        item = json.loads(item)
        if item.get('VerifyFlag') == 8:
            print '1.', item.get('Alias'), '2.', item.get('NickName'), '3.', item.get('RemarkName')




