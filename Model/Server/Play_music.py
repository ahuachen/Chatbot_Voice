# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   Play_music.py
 
@Time    :   2020/5/4 4:41 下午
 
@Desc    :
 
"""

import appscript

iTunes = appscript.app("网易云音乐")
browserWindows = iTunes.browser_windows()
browserWindow = browserWindows[0]
playList = browserWindow.view()
track = playList.tracks[2]

print('Track', track.name())