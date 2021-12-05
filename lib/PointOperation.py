# --- coding:utf-8 ---
"""
---------------------------------------------
__author__: 15500
___date___: 2021/11/27 19:08
---------------------------------------------
"""
import socket
import numpy as np
import open3d as o3d
import time


def create_point_pic_head():
    """
        创建点云图文件，写入pcd文件头
        input:无
        output:无
    """
    with open('../test/get.pcd', "w+", encoding='gbk') as f:
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


def create_point_pic_windows():
    """
        创建点云显示窗口
        input:无
        output: vis：Visualizer对象实例；pointcloud：点云对象；to_reset：刷新方式参数；剩余暂时没用
    """
    to_reset = True
    # 初始化窗口
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='open3d', width=900, height=600)
    # 创建pcd类型数据
    pointcloud = o3d.geometry.PointCloud()  # 定义点云
    vis.add_geometry(pointcloud)  # 将点云对象添加给Visualizer
    # 可视化参数设置
    opt = vis.get_render_option()
    opt.background_color = np.asarray([255, 255, 255])  # 设置背景颜色
    opt.point_size = 1.5  # 设置点云大小
    opt.show_coordinate_frame = False  # 是否显示坐标轴
    opt.point_color_option = o3d.visualization.PointColorOption.YCoordinate

    # # 读取viewpoint参数
    # param = o3d.io.read_pinhole_camera_parameters('viewpoint.json')
    # ctr = vis.get_view_control()
    # # 转换视角
    # ctr.convert_from_pinhole_camera_parameters(param)

    return vis, pointcloud, to_reset


def update_point_file(point_num, recv_data):
    """
        点云数据更新
        input:point_num:点云数量；recv_data：客户端发送点云数据
        output：无
    """
    with open('../test/get.pcd', 'r+', encoding='gbk') as f:
        data = f.readlines()
        # print(len(data))
        point_num = point_num + 1
        # print(f'p : {point_num}')
        data[6] = f'WIDTH {point_num}\n'
        data[9] = f'POINTS {point_num}\n'
    with open('../test/get.pcd', "w+", encoding='gbk') as f:
        for i in data:
            f.write(i)
        f.writelines(recv_data.decode('gbk'))  # 解码成list类型


def update_point_pic(pointcloud, vis, to_reset):
    """
        点云显示更新
        input:pointcloud:点云对象；vis：窗口对象；to_reset：视角相关变量；其他暂时没用
        output：无
    """
    # 刷新点云显示
    pcd = o3d.io.read_point_cloud("../test/get.pcd")  # 此处读取的pcd文件,也可读取其他格式的
    pcd.paint_uniform_color([0, 0, 0])  # 设置点云颜色
    # 将open3d格式数据转换为numpy数组，后用reshape将数组转变为a*b/3行，3列（原数组为a行b列）
    pcd = np.asarray(pcd.points).reshape((-1, 3))
    pointcloud.points = o3d.utility.Vector3dVector(pcd)  # 定义点云坐标位置(如果使用numpy数组可省略上两行)
    vis.update_geometry(geometry=pointcloud)  # 更新点云坐标位置
    if to_reset:
        vis.reset_view_point(to_reset)  # 重置视点函数
        to_reset = False
    # ctr.convert_from_pinhole_camera_parameters(param)  # 暂时没有作用
    # vis.reset_view_point(True)
    # 渲染一帧新的点云图像
    vis.poll_events()
    vis.update_renderer()
    return to_reset
