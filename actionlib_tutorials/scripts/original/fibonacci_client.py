#! /usr/bin/env python

import roslib; roslib.load_manifest('actionlib_tutorials')
import rospy

# Brings in the SimpleActionClient
import actionlib

# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.
import actionlib_tutorials.msg
import paho.mqtt.client as mqtt
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseFeedback

port=1883
return_msg=""
MQTT_TOPIC='location'
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)
def on_message(client, userdata, msg):
    msg_str=msg.payload.decode("utf8")
    print(msg_str)
    sent(msg_str)

def sent(text):
    client = actionlib.SimpleActionClient(self._prefix + 'move_base', MoveBaseAction)
    #go_goal()
    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = actionlib_tutorials.msg.FibonacciGoal(order=text)
    
    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    client.wait_for_result()
    print "result=",client.get_result()
    go_goal()

    # Prints out the result of executing the action
    #return client.get_result()  # A FibonacciResult
def go_goal():
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id="odom" #/odom
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = -10
    goal.target_pose.pose.position.y = -10
    goal.target_pose.pose.orientation.w = 1.0
    self._client.send_goal(goal)#, feedback_cb=self.feedbackCb



if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('fibonacci_client_py')
        #result = on_message
        print "result=",return_msg
        client.connect('10.10.11.190', port)
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
    #except rospy.ROSInterruptException:
    #    print "program interrupted before completion"
