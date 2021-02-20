#!/usr/bin/env python
# license removed for brevity
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import paho.mqtt.client as mqtt
import math
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker  

port = 1883
return_msg=""
MQTT_TOPIC='/ccu'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    msg_str=msg.payload.decode("utf8")
    print('1')
    point()
    print('2')
    movebase_client()

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

def movebase_client():
    #rospy.loginfo('go to init point!')
    #move(1, 0, 2, 0)
    rospy.loginfo('go to target!')
    move(2,2, 2, 1)
    rospy.sleep(5)
    rospy.loginfo("back to home!")
    move(1, 0, 2, 0)
    
    # If the result doesn't arrive, assume the Server is not available
    # if not wait:
    #     rospy.logerr("Action server not available!")
    #     rospy.signal_shutdown("Action server not available!")
    # else:
    # # Result of executing the action
    #     return client.get_result()

def point():
    PCT = rospy.Publisher('point_cloud', Marker, queue_size=10)
    marker = Marker()
    t = rospy.Duration()
    
    marker.lifetime = t
    marker.header.frame_id = "/map"
    marker.ns = "my_namespace"
    marker.id = 10
    marker.type = marker.POINTS
    marker.action = marker.ADD
    marker.pose.orientation.w = 1
    marker.pose.position.x = 1.5679 #-3.4565
    marker.pose.position.y = -2.0503
    marker.pose.position.z = 0
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 1
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 0.0
    
    apoint = Point()
    apoint.x = (407.73981154498244)*0.005
    apoint.y = -((68.3835996914338)*0.05)
    apoint.z = 0
    print('3')
    triplePoints.append(apoint)
    marker.points = triplePoints
    
    PCT.publish(marker)
   


if __name__ == '__main__':
    clientc = mqtt.Client()
    clientc.on_connect = on_connect
    clientc.on_message = on_message

    # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')
        clientc.connect('10.10.11.190', port)
        # movebase_client()        
        clientc.loop_forever()
    #     if result:
    #         rospy.loginfo("Goal execution done!")
    # except rospy.ROSInterruptException:
    #     rospy.loginfo("Navigation test finished.")
    except KeyboardInterrupt:
        clientc.disconnect()
