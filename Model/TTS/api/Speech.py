# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   Speech.py
 
@Time    :   2020/5/1 11:41 下午
 
@Desc    :
 
"""

from Model.TTS.api.Base import AipBase
from Model.TTS.api.Base import base64
from Model.TTS.api.Base import hashlib
from Model.TTS.api.Base import json

class AipSpeech(AipBase):
    """
        Aip Speech
    """

    __asrUrl = 'http://vop.baidu.com/server_api'

    __ttsUrl = 'http://tsn.baidu.com/text2audio'

    def _isPermission(self, authObj):
        """
            check whether permission
        """

        return True

    def _proccessRequest(self, url, params, data, headers):
        """
            参数处理
        """

        token = params.get('access_token', '')
        data['cuid'] = hashlib.md5(token.encode()).hexdigest()

        if url == self.__asrUrl:
            data['token'] = token
            data = json.dumps(data)
        else:
            data['tok'] = token

        if 'access_token' in params:
            del params['access_token']

        return data

    def _proccessResult(self, content):
        """
            formate result
        """

        try:
            return super(AipSpeech, self)._proccessResult(content)
        except Exception as e:
            return {
                'content': content,
            }

    def asr(self, speech=None, format='pcm', rate=16000, options=None):
        """
            语音识别方法
            参数：{'dev_pid': DEV_PID,
                 #"lm_id" : LM_ID,    #测试自训练平台开启此项
                  'format': FORMAT,
                  'rate': RATE,
                  'token': token,
                  'cuid': CUID,
                  'channel': 1,
                  'speech': speech,
                  'len': length
                  }
        """

        data = {}

        if speech:
            data['speech'] = base64.b64encode(speech).decode()
            data['len'] = len(speech)

        data['channel'] = 1
        data['format'] = format
        data['rate'] = rate
        # data['token'] = AipBase.getParams()

        data = dict(data, **(options or {}))

        return self._request(self.__asrUrl, data)

    def synthesis(self, text, lang='zh', ctp=1, options=None):
        """
            语音合成
        """
        data ={}

        data['tex'] = text
        data['lan'] = lang
        data['ctp'] = ctp

        data = dict(data, **(options or {}))

        result = self._request(self.__ttsUrl, data)

        if 'err_no' in result:
            return result

        return result['content']