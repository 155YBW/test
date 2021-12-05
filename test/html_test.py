# --- coding:utf-8 ---
"""
---------------------------------------------
__author__: 15500
___date___: 2021/12/5 16:21
---------------------------------------------
"""
import open3d as o3d
import numpy as np

o3d.visualization.webrtc_server.enable_webrtc()
# vis = o3d.geometry.TriangleMesh.create_box(1,2,4)
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