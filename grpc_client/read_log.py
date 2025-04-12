import sqlite3
from datetime import datetime, timedelta

# 打印带有时间的信息
def msg_with_time(type : str, msg : str):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')#获取当前时间
    print(f'{current_time} {type} : {msg}')

# 读取已解码的日志内容，将日期和访问次数存入数据库
def count(log_content : str):
    msg_with_time('INFO', 'start counting visit data')    # 指示正在进行统计

    date_counts = {}    # 用于存储日期和访问次数的字典
    tag_counts = {}     # 用于存储标签和出现次数的字典

    lines = log_content.splitlines()    # 按行分割日志内容
    for line in lines:
        # 日志格式：
        # xxxx-xx-xx xx:xx:xx INFO event:visit
        # xxxx-xx-xx xx:xx:xx INFO event:purchase tag:xx&xx&...
        words = line.split(' ')    # 按空格分割行内容

        if len(words) < 4:  # 如果行内容不足4个单词，则警告并跳过
            msg_with_time('WARNING', 'a format error detected in the log: shorter than 4 words')
            continue

        if words[3] == 'event:visit':   # 如果是访问事件，则将日期和访问次数存入列表
            date_counts[words[0]] = date_counts.setdefault(words[0], 0) + 1  # 统计日期出现次数

        elif words[3] == 'event:purchase':  # 如果是购买事件，则将标签和出现次数存入字典
            tags = (words[4][4::]).split('&')    # 按&分割标签
            for tag in tags:  # 统计标签出现次数
                tag_counts[tag] = tag_counts.setdefault(tag, 0) + 1
        else:   # 如果不是访问事件也不是购买事件，则警告并跳过
            msg_with_time('WARNING', 'an error detected in the log: undefined event')
            continue

    msg_with_time('INFO', 'log content processed')  # 指示统计成功

#----上传数据到到history数据库
    conn = sqlite3.connect('database/history.db')    # 连接到history数据库
    c = conn.cursor()    # 创建游标

    # 将日期和访问次数插入数据库
    keys = list(date_counts.keys())   # 获取日期列表
    values = list(date_counts.values())   # 获取访问次数列表
    for i in range(len(date_counts)):
        c.execute("SELECT visit_num FROM visit WHERE date = ?", (keys[i],))  # 查询数据库中是否存在该日期
        result = c.fetchone()   # 获取查询结果
        if result is not None:  # 如果存在该日期，则更新访问次数
            c.execute("UPDATE visit SET visit_num = ? WHERE date = ?", (result[0] + values[i], keys[i]))
        else:   # 如果不存在该日期，则插入该日期
            c.execute("INSERT INTO visit (date, visit_num) VALUES (?, ?)", (keys[i], values[i]))
    conn.commit()   # 提交更改
    msg_with_time('INFO', 'successfully upload visit data to history.db')  # 指示上传成功

#----上传热度数据到history数据库
    for tag, count in tag_counts.items():  # 遍历标签和出现次数
        c.execute("SELECT purchase_num FROM hot WHERE tag =?", (tag,))  # 查询数据库中是否存在该标签
        result = c.fetchone()   # 获取查询结果
        if result is not None:  # 如果存在该tag，则更新出现次数
            c.execute("UPDATE hot SET purchase_num =? WHERE tag =?", (result[0] + count, tag))
        else:   # 如果不存在该tag，则插入新tag
            c.execute("INSERT INTO hot (tag, purchase_num) VALUES (?,?)", (tag, count))

    conn.commit()   # 提交更改
    msg_with_time('INFO', 'successfully upload hot data to history.db')  # 指示上传成功
    
    # 获取history.db中热度数据的前10名
    c.execute("SELECT tag, purchase_num FROM hot ORDER BY purchase_num DESC LIMIT 10")
    rows = c.fetchall()     # 获取查询结果
    tag_counts = {}         # 清空原先的tag_counts字典
    sum_of_top_10 = 0
    for row in rows:
        tag_counts[row[0]] = row[1]     # 将标签和出现次数存入字典中
        sum_of_top_10 += row[1]         # 计算前10名的出现次数总和
    
    # 如果history.db的hot表中一共有超过10个标签，则将剩余的tag的出现次数合并为"其他"
    c.execute("SELECT COUNT(*) FROM hot")  # 查询数据库中标签的数量
    result = c.fetchone()   # 获取查询结果
    if result[0] > 10:
        c.execute("SELECT SUM(purchase_num) FROM hot")
        sum_of_all = c.fetchone()    # 获取查询结果
        sum = sum_of_all[0] - sum_of_top_10   # 计算剩余标签的出现次数
        if sum is None or sum <= 0:  # 如果查询结果为空，则警告
            msg_with_time('WARNING', 'sum of \'others\' is None or <= 0')
            tag_counts['others'] = 0
        else:
            tag_counts['others'] = sum  # 将剩余标签的出现次数存入字典中
    
    conn.close()    # 关闭连接

#----上传访问量数据到current_show数据库
    conn = sqlite3.connect('database/current_show.db')    # 连接到current_show数据库
    c = conn.cursor()    # 创建游标
    # 获取数据库中各日期的访问次数，存入date_counts字典中
    c.execute("SELECT date, visit_num FROM visit")  # 查询数据库中所有日期和访问次数
    rows = c.fetchall()   # 获取查询结果
    for row in rows:  # 遍历查询结果
        date_counts[row[0]] = date_counts.setdefault(row[0], 0) + row[1]   # 将日期和访问次数存入字典中

    # 检查date_counts是否为空，若为空则警告
    if not date_counts:
        msg_with_time('WARNING', 'date_counts is empty')

    # 找到最远日期
    max_date = datetime.strptime(max(date_counts.keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d')), '%Y-%m-%d')
    
    # 计算起始日期（最远日期前推29天）
    start_date = max_date - timedelta(days=29)
    
    # 生成连续30天的日期列表（升序排列）
    current_date = start_date
    date_list = []
    while current_date <= max_date:
        date_list.append(current_date.strftime('%Y-%m-%d')) # 将日期格式化为字符串，插入date_list
        current_date += timedelta(days=1)
    
    # 生成次数列表
    count_list = []
    for i in date_list:
        count_list.append(date_counts.get(i, 0))    # 如果日期在date_counts中，则将访问次数存入count_list，否则存入0
    
    # 重写current_show数据库的visit表
    c.execute("DELETE FROM visit")  # 删除表中所有数据
    for i in range(len(date_list)):  # 遍历日期列表和次数列表
        c.execute("INSERT INTO visit (date, visit_num) VALUES (?,?)", (date_list[i], count_list[i]))  # 插入数据

    conn.commit()   # 提交更改
    msg_with_time('INFO','successfully upload visit data to current_show.db')  # 指示上传成功

#----上传前10名(若包含others则为11项)热度数据到current_show数据库
    c.execute("DELETE FROM hot")  # 删除表中原先数据
    for tag, count in tag_counts.items():  # 遍历标签和出现次数
        c.execute("INSERT INTO hot (tag, purchase_num) VALUES (?,?)", (tag, count))

    conn.commit()   # 提交更改
    msg_with_time('INFO', 'successfully upload hot data to current_show.db')  # 指示上传成功
    
    conn.close()    # 关闭连接
    msg_with_time('INFO', 'upload visit data success')  # 指示上传成功

if __name__ == '__main__':
    # 读取日志文件内容
    f = open('grpc_client/test.log', 'r', encoding='utf-8')  # 打开日志文件，读取内容
    log_content = f.read()  # 读取日志内容
    f.close()   # 关闭文件
    count(log_content)  # 调用count方法，将日志内容解析并注入到数据库