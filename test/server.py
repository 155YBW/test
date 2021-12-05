# --- coding:utf-8 ---
"""
---------------------------------------------
__author__: 15500
___date___: 2021/11/6 15:03
---------------------------------------------
"""
import socket
import numpy as np
import open3d as o3d
import time


def main():
    # 初始化服务器
    tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_s.bind(("172.22.106.137", 7890))
    tcp_s.listen(128)  # 此时tcp_s为监听套接字,listen中的变量为最大排队个数，例如：多线程服务器可以同时处理n个客户，则最大请求量为n+128
    t1 = time.time()
    while True:
        print("等待数据链接...")

        client_s, client_addr = tcp_s.accept()  # s接收新的套接字对接客户端，addr接收链接服务器的客户端地址，此时由新的套接字对接客户端，接收套接字继续等待新的客户链接

        print(f"客户端{client_addr}已连接")

        while True:
            # 创建点云图文件
            with open('get.pcd', "w+", encoding='gbk') as f:
                f.write('# .PCD v0.7 - Point Cloud Data file format\n')
                f.write('VERSION 0.7\n')
                f.write('FIELDS x y z intensity\n')
                f.write('SIZE 4 4 4 4\n')
                f.write('TYPE F F F F\n')
                f.write('COUNT 1 1 1 1\n')
                f.write(f'WIDTH 0\n')
                f.write('HEIGHT 1\n')
                f.write('VIEWPOINT 0 0 0 1 0 0 0\n')
                f.write(f'POINTS 0\n')
                f.write('DATA ascii\n')

            # 统计点的数量
            point_num = 0
            pd = True
            while True:
                print(point_num)
                recv_data = client_s.recv(1024*1024)  # recv只接收数据,recv解堵塞有两种情况：1.有数据发送。2.用户端断开链接
                print("after"+str(point_num))
                # print(recv_data)
                # print(time.time() - t1)
                # 点云窗口应在点云文件中存在部分点后再创建，才能正常的刷新数据
                if point_num == 1 and pd:
                    print('create')
                    # 创建点云显示窗口
                    to_reset = True
                    vis = o3d.visualization.Visualizer()
                    vis.create_window(window_name='open3d', width=900, height=600)
                    pointcloud = o3d.geometry.PointCloud()  # 定义点云
                    vis.add_geometry(pointcloud)  # 将点云对象添加给Visualizer
                    opt = vis.get_render_option()
                    opt.background_color = np.asarray([255, 255, 255])  # 设置背景颜色
                    opt.point_size = 1.5  # 设置点云大小
                    opt.show_coordinate_frame = False  # 是否显示坐标轴
                    opt.point_color_option = o3d.visualization.PointColorOption.YCoordinate
                    pd = False

                # 若recv解堵塞了且其值为空，则确定用户端断开了链接
                if recv_data.decode('gbk') == 'end':
                    print('end')
                    with open('get.pcd', "w+", encoding='gbk') as f:
                        f.write('# .PCD v0.7 - Point Cloud Data file format\n')
                        f.write('VERSION 0.7\n')
                        f.write('FIELDS x y z intensity\n')
                        f.write('SIZE 4 4 4 4\n')
                        f.write('TYPE F F F F\n')
                        f.write('COUNT 1 1 1 1\n')
                        f.write(f'WIDTH 0\n')
                        f.write('HEIGHT 1\n')
                        f.write('VIEWPOINT 0 0 0 1 0 0 0\n')
                        f.write(f'POINTS 0\n')
                        f.write('DATA ascii\n')
                    point_num = 0
                    client_s.send(f"end".encode("gbk"))
                else:
                    # 点云数据更新
                    with open('get.pcd', 'r+', encoding='gbk') as f:
                        data = f.readlines()
                        # print(len(data))
                        point_num = point_num + 1
                        data[7] = f'WIDTH {point_num}\n'
                        data[9] = f'POINTS {point_num}\n'
                    with open('get.pcd', "w+", encoding='gbk') as f:
                        for i in data:
                            f.write(i)
                        f.writelines(recv_data.decode('gbk'))  # 解码成list类型

                    if point_num >= 2:
                        # 刷新点云显示
                        pcd = o3d.io.read_point_cloud("get.pcd")  # 此处读取的pcd文件,也可读取其他格式的
                        pcd.paint_uniform_color([0, 0, 0])
                        # 将open3d格式数据转换为numpy数组，后用reshape将数组转变为a*b/3行，3列（原数组为a行b列）
                        pcd = np.asarray(pcd.points).reshape((-1, 3))
                        pointcloud.points = o3d.utility.Vector3dVector(pcd)  # 定义点云坐标位置(如果使用numpy数组可省略上两行)
                        vis.update_geometry(geometry=pointcloud)  # 更新点云坐标位置
                        if to_reset:
                            vis.reset_view_point(True)  # 重置视点函数
                            to_reset = False
                        # 渲染一帧新的点云图像
                        vis.poll_events()
                        vis.update_renderer()
                    client_s.send(f"get{point_num}".encode("gbk"))  # 接收反馈

            client_s.send("success".encode("gbk"))

        client_s.close()

        print(f"客户端{client_addr}已断开\n")

    # 后期开发使用
    tcp_s.close()


if __name__ == '__main__':
    main()