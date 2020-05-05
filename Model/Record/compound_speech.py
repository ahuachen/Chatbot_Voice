# -*- coding: utf-8 -*-

"""
@Author  :   Xu

@Software:   PyCharm

@File    :   compound_speech.py

@Time    :   2020/5/2 12:10 下午

@Desc    :   语音合成

"""

from Model.TTS.api import AipSpeech
import os
import random
import traceback
import logging
import string


# 生成随机的字符串，可用于文件名等
# 参数：
#    strlen  字符串长度，默认为10

# 返回：
#    成功返回 生成的字符串
#    失败返回 None
def get_randstr(strlen=10):
    try:
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(strlen, strlen)))
        return ran_str
    except Exception as e:
        logging.error('Error in get_randstr: ' + traceback.format_exc())
        return None


def text2voice(APP_ID, API_KEY, SECRET_KEY, text, file_path):
    '''
    百度文本转语音
    :param APP_ID:
    :param API_KEY:
    :param SECRET_KEY:
    :param text:
    :param file_path:
    :return:
    '''
    try:
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

        result = client.synthesis(text, 'zh', 1, {
            'vol': 5,
            'per': 4,
        })

        if not isinstance(result, dict):
            if os.path.exists(file_path):
                os.remove(file_path)
            with open(file_path, 'wb') as f:
                f.write(result)
    except Exception as e:
        print(e)
        return None
