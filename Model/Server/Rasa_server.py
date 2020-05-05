# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   Rasa_server.py
 
@Time    :   2020/5/3 10:43 下午
 
@Desc    :
 
"""

import requests
import json
import random

def get_bot_response(query):

    url = "http://172.18.86.20:5005/webhooks/rest/webhook"
    data = {
                "sender": str(random.randint(1000, 10000)),
                "message": query
            }
    response = requests.post(url, data=json.dumps(data))
    # 获取请求状态码 200为正常
    if (response.status_code == 200):
        # 获取相应内容
        content = response.text
        json_dict = json.loads(content)

        robot_response = json_dict[0]['text']
        print(robot_response)

        return robot_response
    else:
        print('请求失败')

# if __name__ == '__main__':
#     query = '你好'
#     get_bot_response(query)