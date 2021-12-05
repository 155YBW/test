# --- coding:utf-8 ---
"""
---------------------------------------------
__author__: 15500
___date___: 2021/11/21 15:43
---------------------------------------------
"""
import open3d as o3d
import numpy as np


def open_window(cloud_point, window_name):
    """
    窗口属性及显示函数
    :param cloud_point: 点云数据
    :param window_name: 创建窗口名称
    :return: NULL
    """
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name=window_name, width=900, height=600)
    vis.add_geometry(cloud_point)  # 加入点云
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])  # 设置背景颜色
    opt.point_size = 1.0  # 设置点云大小
    opt.show_coordinate_frame = False  # 是否显示坐标轴
    opt.point_color_option = o3d.visualization.PointColorOption.XCoordinate  # 设置点云颜色
    vis.run()


# 暂时不用
def display_inlier_outlier(cloud_point, ind):
    """
    降噪显示函数，根据降噪函数给出的噪点索引来区分
    :param cloud_point: 点云数据
    :param ind: 降噪函数生成索引文件
    :return: inlier_cloud：非噪声数据；outlier_cloud：噪声数据
    """
    inlier_cloud = cloud_point.select_by_index(ind)  # 索引筛选点云数据中的点
    outlier_cloud = cloud_point.select_by_index(ind, invert=True)
    # 上色区分
    outlier_cloud.paint_uniform_color([1, 0, 0])
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    return inlier_cloud, outlier_cloud


def SOR_func(cloud_point, nb_neighbors=20, std_ratio=2.0):
    """
    统计式离群点移除
    statistical_outlier_removal降噪函数
    statistical_outlier_removal函数删除与点云的距离比起其他邻域的平均距离远的点，他有两个输入参数：
    nb_neighbors：用于指定邻域点的数量，以便计算平均距离。
    std_ratio：基于点云的平均距离的标准差来设置阈值。阈值越小，滤波效果越明显。
    :param cloud_point: 点云数据
    :return: cl:降噪后剩余点云数量；ind：保留数据索引
    """
    cl, ind = cloud_point.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    inlier_cloud = cloud_point.select_by_index(ind)  # 索引筛选点云数据中的点
    outlier_cloud = cloud_point.select_by_index(ind, invert=True)
    # 上色区分
    # outlier_cloud.paint_uniform_color([1, 0, 0])
    # inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    return inlier_cloud, outlier_cloud


def RRO_func(cloud_point, nb_points=16, radius=0.05):
    """
    半径式离群点剔除
    radius_outlier_removal 会删除在给定半径的球体周围几乎没有邻域点的点。他也有两个输入参数：
    nb_points：选择球体中最少点的数量。
    radius：用来计算点的邻域点的数量的球的半径。
    :param cloud_point:点云数据
    :return:cl:降噪后剩余点云数量；ind：保留数据索引
    """
    cl, ind = cloud_point.remove_radius_outlier(nb_points=nb_points, radius=radius)
    inlier_cloud = cloud_point.select_by_index(ind)  # 索引筛选点云数据中的点
    outlier_cloud = cloud_point.select_by_index(ind, invert=True)
    # 上色区分
    # outlier_cloud.paint_uniform_color([1, 0, 0])
    # inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    return inlier_cloud, outlier_cloud


