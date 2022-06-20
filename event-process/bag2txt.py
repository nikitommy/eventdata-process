#!/usr/bin/env python
#coding:utf-8
import sys
import argparse
from fnmatch import fnmatchcase
from rosbag import Bag
import rosbag

bag_file = 'bike_bay_hdr.bag'
bag = rosbag.Bag(bag_file, "r")
bag_data = bag.read_messages('/dvs/events')
save_path = "/data1/HQF/bike_bay_hdr_events/"

j = 0
for topic, msg, t in bag_data:
    timestr = "%.6f" %  msg.header.stamp.to_sec()
    #print(timestr)
    #%.6f表示小数点后带有6位，可根据精确度需要修改；
    
    cloud_name = save_path + timestr+ ".txt" #点云命名：时间戳.txt
    with open(cloud_name,"w") as f:
		#其中i为索引值，如下直接通过索引取得接收到的数据对象
        for i in range(len(msg.points)):
            msg.points[i].x;
            msg.points[i].y;
            msg.points[i].z;
            f.writelines([str(msg.points[i].x), ' ', str(msg.points[i].y), ' ', str(msg.points[i].z), '\n'])  # 自带文件关闭功能，不需要再写f.close()
    if j % 10 == 0:
    	print('di ', j, ' zhen')
    j += 1
    #o3d.io.write_point_cloud(pcd_name, pcd)
    #o3d.io.write_point_cloud("../../TestData/sync.ply", pcd)
