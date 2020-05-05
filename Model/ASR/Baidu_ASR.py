# -*- coding: utf-8 -*-

"""
@Author  :   Xu

@Software:   PyCharm

@File    :   Baidu_ASR.py

@Time    :   2020/5/1 10:43 下午

@Desc    :

"""

import json
import base64
import time
import ffmpeg
import ast
import os
import pathlib
import logging

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

from Model.config import RobotConfig

basedir = str(pathlib.Path(os.path.abspath(__file__)).parent.parent.parent)

cf = RobotConfig()  # 机器人全局配置文件


class DemoError(Exception):
    pass


def fetch_token():
    '''
    获取调用百度接口的token
    :return:
    '''
    params = {'grant_type': 'client_credentials',
              'client_id': cf.API_KEY,
              'client_secret': cf.SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(cf.TOKEN_URL, post_data)
    f = urlopen(req)
    result_str = f.read()
    result_str = result_str.decode()

    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if cf.SCOPE and (not cf.SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        # print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


def voice2text(file):
    '''
    语音转文字
    :param file:
    :return:
    '''
    token = fetch_token()

    if os.path.exists(basedir + '/Resource/tmp/record-audio2.wav'):
        os.system("rm -rf %s" % basedir + '/Resource/tmp/record-audio2.wav')

    # 需要转换采样率
    ffmpeg.input(file).output(basedir + '/Resource/tmp/record-audio2.wav',
                              ar=16000).run()

    wav_file2 = basedir + '/Resource/tmp/record-audio2.wav'
    with open(wav_file2, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % file)
    speech = base64.b64encode(speech_data)
    speech = str(speech, 'utf-8')
    params = {'dev_pid': cf.DEV_PID,
              # "lm_id" : LM_ID,    #测试自训练平台开启此项
              'format': cf.FORMAT,
              'rate': cf.RATE,
              'token': token,
              'cuid': cf.CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    req = Request(cf.ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        result_str = err.read()
    result_str = str(result_str, 'utf-8')
    result = ast.literal_eval(result_str)

    user_talk = result['result'][0]

    return user_talk
