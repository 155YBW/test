# --- coding:utf-8 ---
"""
---------------------------------------------
__author__: 15500
___date___: 2021/11/27 19:06
---------------------------------------------
"""
import socket
import numpy as np
import open3d as o3d
import time
from lib.PointOperation import create_point_pic_head, create_point_pic_windows, update_point_pic, update_point_file


def point_show(client_s, pic_t1, fps_speed):
    """
        点云连续显示函数
        input:client_s:服务器分配参数；pic_t1：计时参数，后期可舍弃；fps_speed：显示速度参数
        output：无
    """
    # 创建点云pcd文件函数
    create_point_pic_head()

    # 统计点云点的数量
    point_num = 0

    # 创建open3d窗口变量
    create = False

    while True:
        # t2 = time.time()
        recv_data = client_s.recv(1024 * 1024)  # recv只接收数据,recv解堵塞有两种情况：1.有数据发送。2.用户端断开链接

        # to_reset = True

        # 点云窗口应在点云文件中存在部分点后再创建，才能正常的刷新数据
        if point_num == 1 and not create:
            vis, pointcloud, to_reset = create_point_pic_windows()
            create = True  # 避免重复创建窗口导致报错

        # 一张完整的点云图数据读取完毕，刷新pcd文件，显示下一张
        if recv_data.decode('gbk') == 'end' or recv_data.decode('gbk') == 'end\n':
            print('end')

            # 创建点云pcd文件函数，相当于刷新
            create_point_pic_head()

            # 统计点云数量归零
            point_num = 0

            # 结束标志反馈
            client_s.send("end".encode("gbk"))

            # 统计耗时
            pic_t2 = time.time()
            print(f"一张图片耗时：{pic_t2 - pic_t1}s")
            pic_t1 = time.time()

        # 未显示完则继续接收点云数据
        else:
            # 设置刷新条件，控制刷新速度
            if point_num % fps_speed == 0 and point_num != 0:
                update_point_file(point_num, recv_data)
                point_num = point_num + 1

                # 设置刷新条件，防止读取空文件
                if point_num >= 2:
                    # to_reset = True
                    to_reset = update_point_pic(pointcloud, vis, to_reset)
                    print(f'第{point_num}点数据已接收')
                    client_s.send("get".encode("gbk"))

            # 未到刷新条件则不断接收点云数据
            else:
                # 非空判断
                if recv_data:
                    # 文件数据刷新
                    with open('../test/get.pcd', "a+", encoding='gbk') as f:
                        f.writelines(recv_data.decode('gbk'))
                    point_num = point_num + 1
                    print(f'第{point_num}点数据已接收')
                    client_s.send("get".encode("gbk"))  # 接收反馈
                    # t3 = time.time()
                    # print('第%d次接收点数据耗时：%.4f s' % (point_num, (t3 - t2)))

    # vis.destroy_window()  # 接收完毕，关闭窗口
    #
    # client_s.send("success".encode("gbk"))
    #
    # client_s.close()
    #
    # print(f'总共耗时：{str(time.time() - t1)}s')
    #
    # print(f"客户端{client_addr}已断开\n")
