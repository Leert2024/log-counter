#coding:utf-8
#author:leert

import sys
from flask import *
from provide_data import *

app = Flask(__name__)

app.secret_key = 'whatcanisay'#session密钥

# 欢迎界面
@app.route('/')
def hello():
    return render_template('welcome.html')

# 登录界面
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    #获取表单提交的数据
    name = request.form['name']
    password = request.form['password']
    
    #检查用户名与密码是否正确
    if check_account_password(name,password):
        session['name'] = name
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')

# 用户面板
@app.route('/dashboard')
def dashboard():
    #如果用户已登录，显示用户界面
    if 'name' in session:
        return render_template('dashboard.html')
    #用户未登录，让用户先登录
    return redirect(url_for('login'))

# 获取访问量(json格式)并返回给前端
@app.route('/dashboard/api/get_line_chart')
def get_line_chart():
    return get_visit()

@app.route('/dashboard/api/get_pie_chart')
def get_pie_chart():
    return get_hot()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'images/favicon.ico')

@app.route('/apple-touch-icon.png')
def apple_touch_icon():
    return send_from_directory('static', 'images/apple-touch-icon.png')

@app.route('/apple-touch-icon-precomposed.png')
def apple_touch_icon_precomposed():
    return send_from_directory('static', 'images/apple-touch-icon-precomposed.png')

def run_flask():
    app.run(host = '0.0.0.0', port = 80)

if __name__ == '__main__':
    run_flask()