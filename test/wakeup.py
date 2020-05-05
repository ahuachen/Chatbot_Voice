# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   wakeup.py
 
@Time    :   2020/5/4 12:05 下午
 
@Desc    :   语音唤醒测试
 
"""


from Model.WakeUP import snowboydecoder
import signal

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

# if len(sys.argv) == 1:
#     print("Error: need to specify model name")
#     print("Usage: python demo.py your.model")
#     sys.exit(-1)
#
# model = sys.argv[1]

model = '/Users/charlesxu/PycharmProjects/Chatbot_Voice/Resource/wakeup/xiaoqi.pmdl'

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=snowboydecoder.play_audio_file,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()