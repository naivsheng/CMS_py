from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room
import pymysql.cursors
import hashlib

# 创建Flask应用程序和SocketIO实例
app = Flask(__name__)
app.secret_key = 'secret_key'
socketio = SocketIO(app)

# 连接数据库
db = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    db='chatroom',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = db.cursor()

# 创建users表
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

# 创建communications表
cursor.execute("CREATE TABLE IF NOT EXISTS communications (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), message TEXT)")

# 定义处理客户端连接的事件处理函数
@socketio.on('connect')
def handle_connect():
    if 'username' in session:
        join_room(session['username'])
        emit('message', 'You are connected.')
    else:
        return False

# 定义处理客户端发送消息的事件处理函数
@app.route('/chat')
def chat():
    if 'username' in session:
        # 从数据库中获取聊天记录
        select_query = "SELECT * FROM messages ORDER BY id DESC LIMIT 10"
        cursor.execute(select_query)
        messages = cursor.fetchall()
        return render_template('chat.html', username=session['username'], messages=messages)
    return redirect(url_for('login'))

@socketio.on('connect')
def handle_connect():
    join_room('chat_room')
    emit('message', 'You have joined the chat room.', room='chat_room')

@socketio.on('send_message')
def handle_send_message(message):
    # 将消息存储到数据库中
    insert_query = "INSERT INTO messages (username, message) VALUES (%s, %s)"
    values = (session['username'], message)
    cursor.execute(insert_query, values)
    db.commit()
    emit('message', message, room='chat_room')

# 定义处理主页的函数
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 将密码使用md5加密后存储到数据库中
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        # 在数据库中创建新用户
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (username, password_hash)
        cursor.execute(insert_query, values)
        db.commit()
        session['username'] = username
        return redirect(url_for('chat'))
    return render_template('register.html')

# 定义处理登录页面的函数
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 将密码使用md5加密后与数据库中存储的密码进行比较
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password_hash)
        cursor.execute(select_query, values)
        user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

if __name__ == '__main__':
    socketio.run(app)