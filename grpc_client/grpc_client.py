import threading
import time
import grpc
import statistics_pb2 as pb2
import statistics_pb2_grpc as pb2_grpc
from read_log import *

# 创建gRPC通道和服务存根（全局创建，所有线程共享）
server_address = 'localhost:9090'
channel = grpc.insecure_channel(server_address)
stub = pb2_grpc.StatisticsStub(channel)

# 通过gRPC发送get_log请求
def get_log(stub):
    try:
        request = pb2.Statistics_request(req="get_log")     # 发送一个字符串作为请求
        msg_with_time('INFO','get_log request will be sent...')
        response = stub.get_log(request)                    # 调用gRPC方法
        msg_with_time('INFO', 'log received')
        if response.log:
            log_content = response.log.decode('utf-8', errors='ignore')  # 解码日志内容
            count(log_content)  # 调用read_log.py的count方法，将日志内容解析并注入到数据库
        else:
            msg_with_time('ERROR', 'fail to receive log file')
    except Exception as e:
        msg_with_time('ERROR', f"error occurred: {str(e)}")

# 定时执行gRPC请求的线程函数(每小时执行一次)
def get_log_periodically(stop_event, stub):
    while not stop_event.is_set():
        get_log(stub)      # gRPC请求
        time.sleep(3600)        # 每小时执行一次

# 监听用户输入
def listen_for_input(stop_event, stub):
    while not stop_event.is_set():
        user_input = input("command:")
        if user_input == "1":
            get_log(stub)  # 输入1时发送gRPC请求
        elif user_input == "2":
            print("grpc_client will stop...")
            stop_event.set()

if __name__ == "__main__":
    stop_event = threading.Event()      # 创建一个事件对象，作为程序终止的标志

    # 创建定时调用get_log的线程
    periodic_thread = threading.Thread(
        target = get_log_periodically,  # 线程函数为get_log_periodically
        args = (stop_event, stub),      # 传递stop_event和stub作为参数
        daemon = True                   # 设置为守护线程，程序退出时自动停止
    )
    periodic_thread.start() # 启动线程

    msg_with_time('INFO', "grpc_client started")
    print('1 for get_log, 2 or Ctrl+C for stop')

    try:
        listen_for_input(stop_event, stub)  # 监听用户输入
    except KeyboardInterrupt:               # 捕获Ctrl+C
        print("grpc_client will stop...")
    finally:
        stop_event.set()                    # 设置终止标志，通知线程停止
        channel.close()                     # 关闭gRPC通道

    msg_with_time('INFO', "grpc_client terminated by user")
