# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/10/09 17:04 

import logging
import coloredlogs
from flask import Blueprint

log = logging.getLogger(__name__)
coloredlogs.install('INFO')

ss = Blueprint('ss', __name__)
