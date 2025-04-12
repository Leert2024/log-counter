# coding : utf-8
# author : leert

import sqlite3
from server_message import *

#新建数据库
def init_db():
    conn = sqlite3.connect('database/history.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS visit(date TEXT, visit_num INTEGER)') # 访问量表
    c.execute('CREATE TABLE IF NOT EXISTS hot(tag TEXT, purchase_num INTEGER)') # 热度表
    conn.commit()
    conn.close()
    msg_with_time('INFO','table visit in history.db created')
    msg_with_time('INFO','table hot in history.db created')

    conn = sqlite3.connect('database/current_show.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS visit(date TEXT, visit_num INTEGER)') # 访问量表
    c.execute('CREATE TABLE IF NOT EXISTS hot(tag TEXT, purchase_num INTEGER)') # 热度表
    conn.commit()
    conn.close()
    msg_with_time('INFO','table visit in current_show.db created')
    msg_with_time('INFO','table hot in current_show.db created')

#写入测试数据(仅在测试时使用)
def write_test_data():
    conn = sqlite3.connect('database/history.db')
    c = conn.cursor()
    c.execute('INSERT INTO visit VALUES("2025-03-16", 100)')
    c.execute('INSERT INTO visit VALUES("2018-03-17", 200)')
    c.execute('INSERT INTO visit VALUES("2018-03-18", 300)')
    c.execute('INSERT INTO visit VALUES("2018-03-19", 400)')
    conn.commit()   # 提交更改
    conn.close()    # 关闭连接
    msg_with_time('INFO','test data written to table visit in history.db')

    conn = sqlite3.connect('database/current_show.db')
    c = conn.cursor()

    # 插入访问量数据
    c.execute('INSERT INTO visit VALUES("2025-03-16", 100)')
    c.execute('INSERT INTO visit VALUES("2018-03-17", 200)')
    c.execute('INSERT INTO visit VALUES("2018-03-18", 300)')
    c.execute('INSERT INTO visit VALUES("2018-03-19", 400)')

    # 插入热度数据
    c.execute('INSERT INTO hot VALUES("sports", 20)')
    c.execute('INSERT INTO hot VALUES("textbook", 30)')
    c.execute('INSERT INTO hot VALUES("anime", 50)')

    conn.commit()   # 提交更改
    conn.close()    # 关闭连接
    msg_with_time('INFO','test data written table visit in current_show.db')
    msg_with_time('INFO','test data written table hot in current_show.db')

# 显示数据库中的所有数据
def show():
    conn = sqlite3.connect('database/history.db')
    c = conn.cursor()

    print('__________________________________')
    print('    visit table in history.db     ')
    print('----------------------------------')
    try:
        c.execute("SELECT date, visit_num FROM visit")
    except sqlite3.OperationalError:
        msg_with_time('ERROR', 'visit table not found in history.db')
    rows = c.fetchall()
    for row in rows:
        print(row)
    print('__________________________________')

    print('__________________________________')
    print('     hot table in history.db      ')
    print('----------------------------------')
    try:
        c.execute("SELECT tag, purchase_num FROM hot")
    except sqlite3.OperationalError:
        msg_with_time('ERROR', 'hot table not found in history.db')
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close( )

    print('__________________________________')

    print('__________________________________')
    print('  visit table in current_show.db  ')
    print('----------------------------------')
    conn = sqlite3.connect('database/current_show.db')
    c = conn.cursor()
    try:
        c.execute("SELECT date, visit_num FROM visit")
    except sqlite3.OperationalError:
        msg_with_time('ERROR', 'visit table not found in current_show.db')
    rows = c.fetchall()
    for row in rows:
        print(row)
    print('__________________________________')

    print('__________________________________')
    print('   hot table in current_show.db   ')
    print('----------------------------------')
    try:
        c.execute("SELECT tag, purchase_num FROM hot")
    except sqlite3.OperationalError:
        msg_with_time('ERROR', 'hot table not found in current_show.db')
    rows = c.fetchall()
    for row in rows:
        print(row)
    print('__________________________________')

    conn.close()

def delete_info(db_name, table_name):
    conn = sqlite3.connect(f'database/{db_name}')
    c = conn.cursor()
    c.execute(f'DELETE FROM {table_name}')#删除visit表中所有数据
    conn.commit()
    conn.close()

    msg_with_time('INFO','info in history.db cleared')

# 删除所有当前显示数据
def delete_all_current_show_info(table_name):
    conn = sqlite3.connect('database/current_show.db')
    c = conn.cursor()
    c.execute(f'DELETE FROM {table_name}')#删除visit表中所有数据
    conn.commit()
    conn.close()

    msg_with_time('INFO',f'info in table {table_name} in current_show.db cleared')

# 删除history.db中的表
def delete_table(db_name, table_name):
    connection = sqlite3.connect(db_name)  # 连接到 SQLite 数据库（如果数据库不存在，将会自动创建）
    cursor = connection.cursor()    # 创建一个游标对象
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")    # 删除表
        msg_with_time('INFO',f"table '{table_name}' in {db_name} deleted successfully.")
    except sqlite3.Error as e:
        msg_with_time('ERROR',f"fail to delete table '{table_name}' in {db_name} : {e}")

    connection.commit() # 提交更改
    connection.close()  # 关闭连接

if __name__ == '__main__':
    print("""
1. 初始化数据库
2. 写入测试数据
3. 显示数据库中的所有数据          
4. 删除数据
5. 删除表                        
6. 退出
""")
    option1 = int(input('请输入选项：'))
    level = 1
    while(1):
        if level == 1:  # 一级菜单
            if option1 == 1:
                init_db()
            elif option1 == 2:
                write_test_data()
            elif option1 == 3:
                show()
            elif option1 == 4:
                print('1. 历史访问量数据')
                print('2. 所有的商品热度数据')
                print('3. 当前显示的访问量数据')
                print('4. 当前显示的商品热度数据(不推荐删除，可能会影响前端显示)')
                print('5. 所有数据')
                print('请选择需要删除的数据：')
                option2 = input()
                level = 2
                continue
            elif option1 == 5:
                print('1. 历史访问量表(history.db中的visit表)')
                print('2. 所有商品热度表(history.db中的hot表)')
                print('3. 当前显示的访问量表(current_show.db中的visit表)')
                print('4. 当前显示的商品热度表(current_show.db中的hot表)(不建议删除)')
                print('5. 所有表')

                print('请选择需要删除的表：')
                option2 = input()
                level = 2
                continue
            elif option1 == 6:
                break
            else:
                print('输入错误，请重新输入：')

        elif level == 2:  # 二级菜单
            if(option1 == 4):
                if option2 == '1':
                    delete_info('history.db', 'visit')
                elif option2 == '2':
                    delete_info('history.db', 'hot')
                elif option2 == '3':
                    delete_info('current_show.db', 'visit')
                elif option2 == '4':
                    delete_info('current_show.db', 'hot')
                elif option2 == '5':  # 删除所有当前显示数据
                    delete_info('history.db', 'visit')
                    delete_info('history.db', 'hot')
                    delete_info('current_show.db', 'visit')
                    delete_info('current_show.db', 'hot')

            elif(option1 == 5):
                if option2 == '1':
                    delete_table('database/history.db', 'visit')
                elif option2 == '2':
                    delete_table('database/history.db', 'hot')
                elif option2 == '3':
                    delete_table('database/current_show.db', 'visit')
                elif option2 == '4':
                    delete_table('database/current_show.db', 'hot')
                elif option2 == '5':    # 删除所有表
                    delete_table('database/history.db', 'visit')
                    delete_table('database/history.db', 'hot')
                    delete_table('database/current_show.db', 'visit')
                    delete_table('database/current_show.db', 'hot')
            level = 1
        
        option1 = int(input('请输入选项：'))