#!/usr/bin/env python
# license removed for brevity
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatusArray
import paho.mqtt.client as mqtt
import math
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler  
import os

port = 1883
return_msg=""
MQTT_TOPIC='agv/+'

# def callback(data):
#     print(data.status_list[0].status)

# def listener():
#     # rospy.init_node('listener', anonymous=True)
#     rospy.Subscriber("/move_base/status", GoalStatusArray, callback)
#     rospy.spin()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    msg_str=msg.payload.decode("utf8")
    movebase_client(msg.topic)

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

def movebase_client(topic):
    # rate = rospy.Rate(1)
    if topic == 'agv/A':
        move(4, -0.5, 0, -0.5)
	# rate.sleep()
    elif topic == 'agv/B':
        move(4, 1.5, 0, 1.5)
    elif topic == 'agv/O':
        move(0, 0, 1, 0)
    # elif topic == 'agv/change1':
    #     os.system('rosrun airobot agv_control.py') 
    # elif topic == 'agv/change2':
    #     os.system('rosnode kill /agv_control ') 
    rospy.loginfo('go to target!')
    # If the result doesn't arrive, assume the Server is not available
    # if not wait:
    #     rospy.logerr("Action server not available!")
    #     rospy.signal_shutdown("Action server not available!")
    # else:
    # # Result of executing the action
    #     return client.get_result()   


if __name__ == '__main__':
    clientc = mqtt.Client()
    clientc.on_connect = on_connect
    clientc.on_message = on_message

    # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')
        clientc.connect('10.87.1.110', port)
        # movebase_client() 
        clientc.loop_forever()
    #     if result:
    #         rospy.loginfo("Goal execution done!")
    # except rospy.ROSInterruptException:
    #     rospy.loginfo("Navigation test finished.")
    except KeyboardInterrupt:
        clientc.disconnect()
