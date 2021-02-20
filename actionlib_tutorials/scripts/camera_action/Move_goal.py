#!/usr/bin/env python
# license removed for brevity
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

import math
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker 
import numpy as np 
from actionlib_tutorials.msg import my_msg

def get_radian(position1, position2):
    x1 = position1[0]
    y1 = position1[1]
    x2 = position2[0]
    y2 = position2[1]
    radian = math.atan2(y2-y1, x2-x1)
    return radian


def move(pose_x, pose_y, temp_pose_x, temp_pose_y):
    global client
    # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()
   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

   # Move 0.5 meters forward along the x axis of the "map" coordinate frame 
    goal.target_pose.pose.position.x = pose_x
    goal.target_pose.pose.position.y = pose_y

    #No rotation of the mobile base frame w.r.t. map frame
    radian = get_radian([goal.target_pose.pose.position.x, goal.target_pose.pose.position.y], [temp_pose_x, temp_pose_y]) 
    q = quaternion_from_euler(0.0, 0.0, radian, axes='sxyz')
    goal.target_pose.pose.orientation = Quaternion(*q)

   # Sends the goal to the action server.
    client.send_goal(goal)
    
    # Waits for the server to finish performing the action.
    wait = client.wait_for_result()

def movebase_client(social_x, social_y, trans_posx, trans_posy):
    #rospy.loginfo('go to init point!')
    #move(1, 0, 2, 0)
    #rospy.loginfo('go to target!')
    move(social_x, social_y, trans_posx, trans_posy)
    #rospy.sleep(5)
    #rospy.loginfo("back to home!")
    #move(1, 0, 2, 0)
    
    # If the result doesn't arrive, assume the Server is not available
    # if not wait:
    #     rospy.logerr("Action server not available!")
    #     rospy.signal_shutdown("Action server not available!")
    # else:
    # # Result of executing the action
    #     return client.get_result()

def callback(data):
    if data.id == 1:
        
        movebase_client(data.x, data.y, 1, -1)
        rospy.sleep(5)
        #rospy.loginfo("back to home!")
        movebase_client(4.43, 4.57, 0.03, 3.73)
        #sub.unregister()
        #sub = rospy.Subscriber("car", my_msg, callback)


def listener():
    rospy.init_node('listener', anonymous=True)
    #global sub
    #sub = rospy.Subscriber("car", my_msg, callback)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        msg = rospy.wait_for_message("car", my_msg, timeout = None)
        if msg.id == 1:
            movebase_client(msg.x, msg.y, 1, -1)
            rospy.sleep(5)
            movebase_client(4.43, 4.57, 0.03, 3.73)
        rate.sleep()
    #rospy.spin()


if __name__ == '__main__':
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    listener()
    

