#coding: utf-8
#author:leert

from datetime import datetime

#打印带有时间的信息
def msg_with_time(type : str, msg : str):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')#获取当前时间
    print(f'{current_time} {type} : {msg}')

if __name__ == '__main__':
    msg_with_time('INFO', 'test')