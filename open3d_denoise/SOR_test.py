# --- coding:utf-8 ---
"""
---------------------------------------------
__author__: 15500
___date___: 2021/11/27 19:23
---------------------------------------------
"""
import open3d as o3d
from denoise import open_window, SOR_func


if __name__ == '__main__':
    pcd = o3d.io.read_point_cloud("test/gt_1.pcd")
    open_window(pcd, '降噪前')
    in_data, out_data = SOR_func(pcd)
    open_window(in_data, '降噪后')
    # open_window(out_data, '噪点')
