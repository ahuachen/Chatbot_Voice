# -*- coding: utf-8 -*-
# @Time     :2018/9/4
# @Author   :qpf
# update    : xmxoxo

"""
对本地语音文件解析成文字
"""
import ffmpeg


# from Model.TTS.api import AipSpeech
from aip import AipSpeech
from Model.ASR.Baidu_ASR import fetch_token


def voice2text(APP_ID, API_KEY, SECRET_KEY, file_path):
    '''
    asr转化
    1536：普通话
    状态码记录：
    3305： 次数超限，或者token不对
    3307
    :param APP_ID:
    :param API_KEY:
    :param SECRET_KEY:
    :param file_path:
    :return:
    '''
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    ret = client.asr(get_data(file_path), 'wav', 16000, {'dev_pid': 1536}, )
    if ret:
        if ret['err_msg'] == 'success.':
            return ret['result']
    return None


def voice2text2(APP_ID, API_KEY, SECRET_KEY, file_path):
    '''
    asr转化
    1536：普通话
    状态码记录：
    3305： 次数超限，或者token不对
    3307
    :param APP_ID:
    :param API_KEY:
    :param SECRET_KEY:
    :param file_path:
    :return:
    '''
    token = fetch_token()
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    params = {
        'dev_pid': 1537,
        'token': token
    }
    wav_file = '/Users/charlesxu/PycharmProjects/Chatbot_Voice/Resource/tmp/record-audio.wav'
    ffmpeg.input(wav_file).output('/Users/charlesxu/PycharmProjects/Chatbot_Voice/Resource/tmp/record-audio2.wav', ar=16000).run()

    wav_file2 = '/Users/charlesxu/PycharmProjects/Chatbot_Voice/Resource/tmp/record-audio2.wav'
    ret = client.asr(wav_file2, 'wav', 16000, params)
    if ret:
        if ret['err_msg'] == 'success.':
            return ret['result']
    return None


def get_data(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()
