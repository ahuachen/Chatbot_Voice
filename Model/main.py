# -*- coding: utf-8 -*-

"""
@Author  :   Xu

@Software:   PyCharm

@File    :   main.py

@Time    :   2020/5/2 12:10 下午

@Desc    :   语音助手主函数

"""

import os
import sys
import random
import string
import traceback
import logging
import pathlib
import time
from playsound import playsound

from Model.Record import input_record
from Model.TTS.Baidu_TTS import text2voice
from Model.ASR.Baidu_ASR import voice2text

from Model.Record.compound_speech import *
from Model.Record.output_radio import *

from Model.Server.Rasa_server import get_bot_response
from Model.Server.Tuling_server import get_tuling_answer
from Model.config import RobotConfig

logger = logging.getLogger(__name__)

basedir = str(pathlib.Path(os.path.abspath(__file__)).parent.parent)

cf = RobotConfig()


class RobotsConfig():
    # 临时文件的目录与名称
    temp_folder = 'tmp'

    temp_folder = os.path.join(basedir + "/Resource", temp_folder)

    # temp_folder = '/Users/charlesxu/PycharmProjects/Chatbot_Voice/test/tmp'

    # 录音文件名
    wavfile_path = os.path.join(temp_folder, 'record-audio.wav')

    # 回答语音文件名
    tuling_answer_file = os.path.join(temp_folder, 'tuling-answer.mp3')

    # 问候语
    Voice_Dailog0 = os.path.join(temp_folder, 'dailog0.mp3')


class VoiceRobot():

    def __init__(self, config):
        self.config = config

        if not os.path.exists(config.temp_folder):
            os.makedirs(self.config.temp_folder)

        # 生成
        if not os.path.exists(self.config.Voice_Dailog0):
            text2voice(cf.APP_ID, cf.API_KEY, cf.SECRET_KEY, "亲，我在呢！有啥事？", self.config.Voice_Dailog0)

        self.answer = self._fun_echo

        print("正在删除临时文件...")
        os.system("rm -rf %s" % os.path.join(self.config.temp_folder, "tuling-answer_*.mp3"))

    # 默认回复方法：原样返回
    def _fun_echo(self, x):
        return x

    # 指定回答的方法
    def answer(self, answer_fun):
        self.answer = answer_fun
        return 1

    def run(self):
        pass

        while True:

            # 先调用录音，录10秒
            # speak(Voice_Dailog0)
            print('准备录音...')
            # playsound(basedir + '/Resource/wakeup/ding.wav')
            input_record.record(self.config.wavfile_path)  # 成功
            # playsound(basedir + '/Resource/wakeup/dong.wav')

            time.sleep(3)
            # 语音转成文字的内容
            print('声音转文字...')
            input_message = voice2text(self.config.wavfile_path)

            print('你说:', input_message)

            if not input_message:  # 没有识别到则继续
                continue

            # 获取回答信息
            if '小笨' in input_message:
                answer = '主人，我在呢，有啥事？'
            elif '爸爸' in input_message:
                answer = '爸爸'
            elif '爷爷' in input_message:
                answer = '爷爷'
            elif '哥哥' in input_message:
                answer = '哥哥'
            else:
                # answer = get_bot_response(input_message)
                answer = get_tuling_answer(input_message)
            print("[答]:%s" % answer)

            # 随机生成语音文件
            tuling_answer_file = os.path.join(self.config.temp_folder, 'robot-answer_' + get_randstr() + '.mp3')
            print('机器人语音文件: %s ' % tuling_answer_file)

            print('文字转声音...')
            text2voice(cf.APP_ID, cf.API_KEY, cf.SECRET_KEY, answer, tuling_answer_file)

            # 播放图灵回答的内容
            print('播放声音...')
            playMp3(tuling_answer_file)

            if input_message[0] == '再见':
                break

        # 退出后删除临时文件
        os.system("rm -rf %s" % basedir + '/Resource/tmp/robot-answer_*.wav')


# def myanswer(x):
#     print("调用对话系统接口")
#     answer = get_bot_response()    # 这里调用外部接口
#     return answer

if __name__ == '__main__':
    robot = VoiceRobot(RobotsConfig())

    # 指定回答接口
    print('指定接口...')
    # robot.answer = myanswer

    # 运行机器人
    robot.run()
