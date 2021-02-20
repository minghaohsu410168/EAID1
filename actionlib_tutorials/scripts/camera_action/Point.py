#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler  
import numpy as np
import math


def get_radian(position1, position2):
    x1 = position1[0]
    y1 = position1[1]
    x2 = position2[0]
    y2 = position2[1]
    radian = math.atan2(y2-y1, x2-x1)
    return radian


def point():
    PCT = rospy.Publisher('point_cloud', Marker, queue_size=10)
    rospy.init_node('point', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        marker = Marker()
        t = rospy.Duration()
        marker.lifetime = t
        marker.header.frame_id = "/map"
        #marker.ns = "my_namespace"
        marker.id = 10
        marker.type = marker.POINTS
        marker.action = marker.ADD
        marker.pose.orientation.w = 1
        marker.pose.position.x = 1.82 #-3.4565 #3
        marker.pose.position.y = -2.2 #4
        marker.pose.position.z = 0
 	radian = get_radian([1.82, -2.2], [3.09, 4.1])
        q = quaternion_from_euler(0.0, 0.0, radian, axes='sxyz')
        print(q)
    	marker.pose.orientation = Quaternion(*q)
        #marker.pose.orientation.x = 0.0
        #marker.pose.orientation.y = 0.0
        #marker.pose.orientation.z = 0.38268343
        #marker.pose.orientation.w = 1
        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        triplePoints = []
        apoint = Point()
        apoint.x = (407.73981154498244)*0.01
        apoint.y = -(68.3835996914338)*0.01 

        triplePoints.append(apoint)
        marker.points = triplePoints
        PCT.publish(marker)
	rate.sleep()

def distance(x1, y1, x2, y2):
	pass
    

if __name__ == '__main__':
    try:
        point()
    except rospy.ROSInterruptException:
        pass
