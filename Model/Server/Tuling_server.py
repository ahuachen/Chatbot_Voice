# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   Tuling_server.py
 
@Time    :   2020/5/3 11:30 下午
 
@Desc    :
 
"""

import requests
import json

from Model.config import RobotConfig

cf = RobotConfig()


def get_tuling_answer(message):
    url = 'http://www.tuling123.com/openapi/api?key=' + cf.TL_KEY + '&info=' + message
    res = requests.get(url)
    res.encoding = 'utf-8'
    response = json.loads(res.text)
    answer_message = response['text']
    return answer_message
