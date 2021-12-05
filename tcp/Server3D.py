# --- coding:utf-8 ---
"""
---------------------------------------------
__author__: 15500
___date___: 2021/11/9 13:51
---------------------------------------------
最新版本，更新时间：2021.11.22
"""

import socket
import numpy as np
import open3d as o3d
import time
from lib.PointShow import point_show


def server():
    # 初始化服务器
    tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_s.bind(("172.22.106.137", 7890))
    tcp_s.listen(128)  # 此时tcp_s为监听套接字,listen中的变量为最大排队个数，例如：多线程服务器可以同时处理n个客户，则最大请求量为n+128

    """ 关键变量 """
    fps_speed = 30  # 点云刷新速度，每fps_speed个点刷新一次
    pic_t1 = time.time()  # 计时变量，测试用

    # 循环等待客户端链接
    while True:
        print("等待数据链接...")
        client_s, client_addr = tcp_s.accept()  # s接收新的套接字对接客户端，addr接收链接服务器的客户端地址，此时由新的套接字对接客户端，接收套接字继续等待新的客户链接
        print(f"客户端{client_addr}已连接")

        point_show(client_s, pic_t1, fps_speed)  # 点云显示函数

    # 后期开发使用
    tcp_s.close()




