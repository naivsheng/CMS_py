'''
Author: naivsheng naivsheng@outlook.com
Date: 2023-04-12 17:27:37
LastEditors: naivsheng naivsheng@outlook.com
LastEditTime: 2023-04-17 12:34:34
FilePath: \CMS_py\client.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import requests
 
file_data = {'image': open('flask.jpg', 'rb')}
 
user_info = {'info': 'flask'}
 
r = requests.post("http://127.0.0.1:5000/upload", data=user_info, files=file_data)
 
print(r.text)
