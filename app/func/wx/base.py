# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/05 21:00
from lib.weixin import WebWeixin
import logging
import json


class MyBot(WebWeixin):
    log = logging.getLogger(__name__)
    import coloredlogs
    coloredlogs.install(level='DEBUG')

    def _init(self):
        self._echo('[*] 微信网页版 ... 开动')
        print
        logging.debug('[*] 微信网页版 ... 开动')
        while True:
            self._run('[*] 正在获取 uuid ... ', self.getUUID)
            self._echo('[*] 正在获取二维码 ... 成功')
            print
            logging.debug('[*] 微信网页版 ... 开动')
            self.genQRCode()
            print '[*] 请使用微信扫描二维码以登录 ... '
            if not self.waitForLogin():
                continue
                print '[*] 请在手机上点击确认以登录 ... '
            if not self.waitForLogin(0):
                continue
            break

        self._run('[*] 正在登录 ... ', self.login)
        self._run('[*] 微信初始化 ... ', self.webwxinit)
        self._run('[*] 开启状态通知 ... ', self.webwxstatusnotify)
        self._run('[*] 获取联系人 ... ', self.webwxgetcontact)
        self._echo('[*] 应有 %s 个联系人，读取到联系人 %d 个' %
                   (self.MemberCount, len(self.MemberList)))
        self._echo('[*] 共有 %d 个群 | %d 个直接联系人 | %d 个特殊账号 ｜ %d 公众号或服务号' % (len(self.GroupList),
                                                                         len(self.ContactList),
                                                                         len(self.SpecialUsersList),
                                                                         len(self.PublicUsersList)))
        self._run('[*] 获取群 ... ', self.webwxbatchgetcontact)
        logging.debug('[*] 微信网页版 ... 开动')

    def write_info(self, infos, filename):
        self.log.info('Start write %s ...' % filename)
        with open(filename + '.json', 'w+') as f:
            for item in infos:
                print item
                f.write(json.dumps(item, ensure_ascii=False))
                f.write('\n')

    def get_contact(self):
        self._init()
        self.write_info(self.GroupList, 'group')
        self.write_info(self.ContactList, 'contract')
        self.write_info(self.PublicUsersList, 'public')
        self.write_info(self.SpecialUsersList, 'special')


my = MyBot()
my.get_contact()



    # def test(self):
    #     if self.DEBUG:
    #         print self
    #     logging.debug(self)
    #
    #     if self.interactive and raw_input('[*] 是否开启自动回复模式(y/n): ') == 'y':
    #         self.autoReplyMode = True
    #         print '[*] 自动回复模式 ... 开启'
    #         logging.debug('[*] 自动回复模式 ... 开启')
    #     else:
    #         print '[*] 自动回复模式 ... 关闭'
    #         logging.debug('[*] 自动回复模式 ... 关闭')
    #
    #     listenProcess = multiprocessing.Process(target=self.listenMsgMode)
    #     listenProcess.start()
    #
    #     while True:
    #         text = raw_input('')
    #         if text == 'quit':
    #             listenProcess.terminate()
    #             print('[*] 退出微信')
    #             logging.debug('[*] 退出微信')
    #             exit()
    #         elif text[:2] == '->':
    #             [name, word] = text[2:].split(':')
    #             if name == 'all':
    #                 self.sendMsgToAll(word)
    #             else:
    #                 self.sendMsg(name, word)
    #         elif text[:3] == 'm->':
    #             [name, file] = text[3:].split(':')
    #             self.sendMsg(name, file, True)
    #         elif text[:3] == 'f->':
    #             print '发送文件'
    #             logging.debug('发送文件')
    #         elif text[:3] == 'i->':
    #             print '发送图片'
    #             [name, file_name] = text[3:].split(':')
    #             self.sendImg(name, file_name)
    #             logging.debug('发送图片')
    #         elif text[:3] == 'e->':
    #             print '发送表情'
    #             [name, file_name] = text[3:].split(':')
    #             self.sendEmotion(name, file_name)
    #             logging.debug('发送表情')


# def alias():
#     with open('content.txt') as f:
#         infos = f.readlines()
#         items = []
#         for info in infos:
#             print info.replace('\n', '')
#             item = json.loads(info)
#             items.append(item.get('Alias'))
#         with open('gzh.txt', 'w') as f:
#             for item in items:
#                 f.write(item)
#                 f.write('\n')
#
#
# def insert_db():
#     with open('gzh.txt', 'r') as f:
#         items = f.readlines()
#     for item in items:
#         item = item.replace('\n', '')
#         if item != '':
#             print item
#             db.wx_source.insert({'wx_id': item})
#
# insert_db()