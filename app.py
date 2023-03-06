from flask import Flask, render_template, request, redirect, url_for, session
import datetime
import mysql.connector
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 连接 MySQL 数据库
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql",
  database="cms_db"
)

# 初始化 Flask-SocketIO
socketio = SocketIO(app)

# 创建游标
cursor = db.cursor()

# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # 向数据库中插入用户信息
        insert_query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        values = (username, password, email)
        cursor.execute(insert_query, values)
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

# 退出登录
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# 用户首页
@app.route('/')
def home():
    if 'user_id' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id=%s", (session['user_id'],))
        tasks = cursor.fetchall()
        cursor.execute("SELECT * FROM messages WHERE user_id=%s", (session['user_id'],))
        messages = cursor.fetchall()
        return render_template('home.html', tasks=tasks, messages=messages)
    else:
        return redirect(url_for('login'))

# 发布任务
@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = datetime.datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        cursor = db.cursor()
        cursor.execute("INSERT INTO tasks (user_id, title, description, due_date) VALUES (%s, %s, %s, %s)", (session['user_id'], title, description, due_date))
        db.commit()
        return redirect(url_for('home'))
    else:
        return render_template('create_task.html')

# 回馈任务
@app.route('/feedback_task/<int:task_id>', methods=['GET', 'POST'])
def feedback_task(task_id):
    if request.method == 'POST':
        feedback = request.form['feedback']
        cursor = db.cursor()
        cursor.execute("UPDATE tasks SET feedback=%s WHERE id=%s AND user_id=%s", (feedback, task_id, session['user_id']))
        db.commit()
        return redirect(url_for('home'))
    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id=%s AND user_id=%s", (task_id, session['user_id']))
        task = cursor.fetchone()
        if task:
            return render_template('feedback_task.html', task=task)
        else:
            return redirect(url_for('home'))

# 日程提醒
@app.route('/reminders')
def reminders():
    if 'username' in session:
        # 从数据库中获取用户的日程提醒
        select_query = "SELECT * FROM reminders WHERE username = %s"
        values = (session['username'],)
        cursor.execute(select_query, values)
        reminders = cursor.fetchall()
        return render_template('reminders.html', reminders=reminders)
    return redirect(url_for('login'))

# 用户沟通
@app.route('/communication')
def communication():
    if 'username' in session:
        # 从数据库中获取用户的沟通记录
        select_query = "SELECT * FROM communications WHERE username = %s"
        values = (session['username'],)
        cursor.execute(select_query, values)
        communications = cursor.fetchall()
        return render_template('communication.html', communications=communications)
    return redirect(url_for('login'))

@socketio.on('join')
def on_join(data):
    username = session['username']
    join_room(username)
    emit('user_joined', {
        'username': username
    }, broadcast=True)

@socketio.on('new_message')
def on_new_message(data):
    username = session['username']
    message = data['message']
    # 将新消息保存到数据库
    insert_query = "INSERT INTO communications (username, message) VALUES (%s, %s)"
    values = (username, message)
    cursor.execute(insert_query, values)
    db.commit()
    emit('new_message', {
        'username': username,
        'message': message
    }, broadcast=True)

if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app)