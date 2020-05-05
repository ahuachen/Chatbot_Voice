# -*- coding: utf-8 -*-

"""
@Author  :   Xu

@Software:   PyCharm

@File    :   input_record.py

@Time    :   2020/5/2 12:10 下午

@Desc    :   实时录音实现，并且保存说话内容，用sounddevice实现

"""

import sounddevice as sd
from scipy.io.wavfile import write
import logging

logger = logging.getLogger(__name__)


def record(file_path):
    try:
        # 各路参数
        fs = 44100
        seconds = 3  # Duration of recording
        recording = sd.rec(frames=fs * seconds, samplerate=fs, blocking=True, channels=1)
        sd.wait()  # Wait until recording is finished
        write(file_path, fs, recording)
        logger.info('录音结束')
    except Exception as e:
        print("系统无法录音，请检查录音硬件设备情况...")
        return None