# --- coding:utf-8 ---
"""
---------------------------------------------
__author__: 15500
___date___: 2021/11/6 14:34
---------------------------------------------
"""
# --- coding:utf-8 ---
"""
---------------------------------------------
__author__: 15500
___date___: 2021/9/21 13:46
---------------------------------------------
"""
"""
    创建服务端流程：
        创建套件字 socket
        绑定本地信息 bind
        让默认套件字由主动变为被动 listen
        等待客户端的链接 accept
"""

import socket


def main():
    tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_s.bind(("172.22.106.137", 7890))

    tcp_s.listen(128)  # 此时tcp_s为监听套接字,listen中的变量为最大排队个数，例如：多线程服务器可以同时处理n个客户，则最大请求量为n+128

    while True:
        print("等待数据链接...")

        client_s, client_addr = tcp_s.accept()  # s接收新的套接字对接客户端，addr接收链接服务器的客户端地址，此时由新的套接字对接客户端，接收套接字继续等待新的客户链接

        print(f"客户端{client_addr}已连接")

        while True:
            recv_data = client_s.recv(1024)  # recv只接收数据,recv解堵塞有两种情况：1.有数据发送。2.用户端断开链接
            # print('')
            # 若recv解堵塞了且其值为空，则确定用户端断开了链接
            if recv_data:
                print(recv_data.decode("gbk"))
                if recv_data.decode('gbk') == "end":
                    print("end of it")
            else:
                break
            client_s.send("get".encode("gbk"))

        client_s.close()

        print(f"客户端{client_addr}已断开\n")

    tcp_s.close()

if __name__ == '__main__':
    main()
