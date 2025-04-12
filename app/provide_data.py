#coding:utf-8
#author:leert

import os
import sqlite3
from flask import jsonify
from datetime import datetime, timedelta

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SHOW_DB_PATH = os.path.join(CURRENT_DIR, '../database/current_show.db')
ACCOUNT_DB_PATH = os.path.join(CURRENT_DIR, '../database/account.db')

# 打印带有时间的信息
def msg_with_time(type : str, msg : str):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')#获取当前时间
    print(f'{current_time} {type} : {msg}')

# 检查账号密码是否正确
def check_account_password(username, password):
    conn = sqlite3.connect(ACCOUNT_DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM account WHERE username = ?", (username,))
    data = c.fetchone()
    conn.close()

    if data:
        if data[2] == password:
            msg_with_time('INFO', f'account {data[0]} : {username} login success')
            return True
        else:
            msg_with_time('WARNING', f'account {data[0]} : {username} entered wrong password')
            return False
    else:
        msg_with_time('WARNING',f'nonexistent user {username} attempt to login')
        return False

# 获取访问量，返回30天内的数据(json对象)
def get_visit():
    date = []
    visit = []

    conn = sqlite3.connect(SHOW_DB_PATH)
    c = conn.cursor()

    # 查询数据库中所有日期和访问次数，按日期由远到近排序
    try:
        c.execute("SELECT * FROM visit ORDER BY date DESC")
    except sqlite3.OperationalError:
        msg_with_time('ERROR', f'visit table not found in database/current_show.db')

        for i in range(30):
            start = datetime.now() - timedelta(days=29)
            date.append((start + timedelta(days=i)).strftime('%Y-%m-%d'))
            visit.append(0)
        
        return jsonify(dict(zip(date, visit)))
    
    rows = c.fetchall()   # 获取查询结果
    conn.close()

    for row in rows:
        date.append(row[0])
        visit.append(row[1])

    # 如果数据超过30天，则只返回最近30天的数据
    if(len(rows) > 30):
        msg_with_time('WARNING', 'visit data of more than 30 days in current_show.db')
        return jsonify(dict(zip(date[-30:], visit[-30:])))

    # 如果数据不足30天，则用0补齐
    elif(len(rows) < 30):
        msg_with_time('WARNING', 'visit data in current_show.db is less than 30 days')
        # 在前面前插若干个访问量都为0的日期，使其长度为30
        first_date = datetime.strptime(date[0], '%Y-%m-%d')
        for i in range(30 - len(rows)):
            date.insert(0, (first_date - timedelta(days=i+1)).strftime('%Y-%m-%d'))
            visit.insert(0, 0)

    return jsonify(dict(zip(date, visit)))

# 获取热度，返回所有tag和出现次数(json对象)
def get_hot():
    conn = sqlite3.connect(SHOW_DB_PATH)
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM hot")   # 查询hot表中所有tag和出现次数
    except sqlite3.OperationalError:
        msg_with_time('ERROR', f'hot table not found in database/current_show.db')
        return jsonify({'foo': 1, 'bar': 2, 'baz': 3})# 获取数据失败，返回无意义数据，避免前端报错
    rows = c.fetchall()   # 获取查询结果

    if(not rows):   # 处理查询结果为空的情况
        msg_with_time('WARNING', 'hot data in current_show.db is empty')
        return jsonify({'foo': 1, 'bar': 2, 'baz': 3})
    
    hot = {}    # 将查询结果转换为字典，键为tag，值为出现次数
    for row in rows:
        hot[row[0]] = row[1]
    conn.close()    # 关闭连接

    return jsonify(hot) # 返回json对象给前端

if __name__ == '__main__':
    print('This is a module, not a script.')