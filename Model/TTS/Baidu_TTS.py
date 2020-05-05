# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   Baidu_TTS.py
 
@Time    :   2020/5/1 10:44 下午
 
@Desc    :   语音合成
 
"""

import logging
import os

from Model.TTS.api.Speech import AipSpeech

# 语音合成百度文档地址：http://yuyin.baidu.com/docs/tts/196
# 参数	类型	描述	是否必须
# tex	String	合成的文本，使用UTF-8编码，请注意文本长度必须小于1024字节	是
# lang	String	语言选择,填写zh	是
# ctp	String	客户端类型选择，web端填写1	是
# cuid	String	用户唯一标识，用来区分用户，填写机器 MAC 地址或 IMEI 码，长度为60以内	否
# spd	String	语速，取值0-9，默认为5中语速	否
# pit	String	音调，取值0-9，默认为5中语调	否
# vol	String	语速，取值0-15，默认为5中语速	否
# per	String	发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女

logger = logging.getLogger(__name__)


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
        aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        result = aipSpeech.synthesis(text, 'zh', 1, {
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