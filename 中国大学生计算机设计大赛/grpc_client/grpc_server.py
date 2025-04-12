#coding: utf-8

from time import sleep
import grpc
import statistics_pb2 as pb2
import statistics_pb2_grpc as pb2_grpc
from concurrent import futures

ADDRESS = '127.0.0.1'
PORT = '9090'

class Statistics(pb2_grpc.StatisticsServicer):
    def get_log(self, request, context):
        print('INFO Statistics_request received')    # 指示已收到请求

        if request.req != "get_log":   # 检查请求是否合法
            print('WARNING recv an invalid request')
            return pb2.Statistics_response(log = None)

        with open('test.log', 'rb') as f:   # 读取日志文件
            log_content = f.read()
        print('INFO log file read')
        return pb2.Statistics_response(log = log_content)
    
def run_grpc():
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))    # 创建gRPC服务器，指定线程池大小为4
    pb2_grpc.add_StatisticsServicer_to_server(Statistics(), grpc_server)    # 将服务实现注册到服务器上
    grpc_server.add_insecure_port(f'{ADDRESS}:{PORT}')  # 添加监听端口
    print(f'INFO grpc_server started at {ADDRESS}:{PORT}')   # 打印服务器启动信息
    grpc_server.start() # 启动服务器
    try:
        while(1):
            sleep(3600)
    except KeyboardInterrupt:
        grpc_server.stop(0)

if __name__ == '__main__':
    run_grpc()
