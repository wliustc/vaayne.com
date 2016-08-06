# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/06 17:14 

from pprint import PrettyPrinter
import json

pp = PrettyPrinter(indent=4)

with open('group.json') as f:
    con = f.readlines()
    for item in con:
        item = json.loads(item)
        # pp.pprint(item)
        print '1.', item.get('Alias'), '2.', item.get('NickName'), '3.', item.get('RemarkName'), '4.', item.get('city')




