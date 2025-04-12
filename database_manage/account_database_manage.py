#coding: utf-8
#author:leert

import sqlite3
from server_message import *

DB_PATH = 'database/account.db'

#初始化账号数据库
def init_account_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS account
                (id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

#添加账号
def add_account(id, username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO account VALUES (?, ?, ?)", (id, username, password))
    msg_with_time('INFO', f'account {id} : {username} created')
    conn.commit()
    conn.close()

#删除账号
def delete_account(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM account WHERE id =?", (id,))
    conn.commit()
    conn.close()
    
#检查账号密码是否正确，正确返回True，错误或账号不存在返回False
def check_account_password(username, password):
    conn = sqlite3.connect(DB_PATH)
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

# 打印所有账号信息
def show_account():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM account")
    data = c.fetchall()
    for row in data:
        print(row)
    conn.close()

if __name__ == '__main__':
    print('1. 添加账号')
    print('2. 删除账号')
    print('3. 检查账号密码')
    print('4. 显示所有账号信息')
    print('5. 退出')

    init_account_database()

    while 1:
        a = input('请输入操作:')

        if a == '1':
            id = input('请输入账号id:')
            username = input('请输入账号名:')
            password = input('请输入密码:')
            add_account(id, username, password)
        elif a == '2':
            id = input('请输入账号id:')
            delete_account(id)
        elif a == '3':
            username = input('请输入账号名:')
            password = input('请输入密码:')
            print(check_account_password(username, password))
        elif a == '4':
            show_account()
        elif a == '5':
            break
        else:
            pass