'''
Author: naivsheng naivsheng@outlook.com
Date: 2023-04-12 17:27:28
LastEditors: naivsheng naivsheng@outlook.com
LastEditTime: 2023-04-17 17:22:59
FilePath: \CMS_py\server.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from flask import Flask, request, url_for, redirect
from werkzeug.utils import secure_filename
import os
from werkzeug.routing import BaseConverter
 
class MyIntConverter(BaseConverter):
 
    def __init__(self, url_map):
        super(MyIntConverter, self).__init__(url_map)
 
    def to_python(self, value):
        return int(value)
 
    def to_url(self, value):
        return value * 2

    
app = Flask(__name__)
app.url_map.converters['my_int'] = MyIntConverter

# 文件上传目录
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
# 支持的文件格式
app.config['ALLOWED_EXTENSIONS'] = {'png','jpg','jpeg','git'}
# 判断文件名是否是支持的格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files['image']
    if upload_file and allowed_file(upload_file.filename): # 上传前文件在客户端的文件名
        filename = secure_filename(upload_file.filename)
        # 将文件保存到 static/uploads目录，文件名同上传时使用的文件名
        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'],filename))
        return 'info is '+ request.form.get('info', '')+'. success'
    else:
        return 'failed'

@app.route('/')
def hello_world():
    pass

@app.route('/user/<name>')
def user(name):
    pass

@app.route('/test')
def test():
    # 工具函数url_for可以让你以软编码的形式生成url，提供开发效率。
    print(url_for('test'))
    print(url_for('user', name='loen'))
    print(url_for('page', num=1, q='welcome to w3c 15%2'))
    print(url_for('static', filename='uploads/flask.jpg'))
    return 'Hello'

# redirect函数用于重定向
@app.route('/old')
def old():
    print('this is old')
    return redirect(url_for('new'))
 
@app.route('/new')
def new():
    print('this is new')
    return 'this is new'

# num变量自动转化为int、float、path
@app.route('/page/<int:num>')
def page(num):
    print(num)
    print(type(num))
    pass
    return 'hello world'
 

if __name__ == '__main__':
    app.run(port=5000,debug=True)