#!/usr/bin/env python
import rospy
import paho.mqtt.client as mqtt
from geometry_msgs.msg import Twist
import threading

port = 1883
MQTT_TOPIC='agv/+'
msg_str = ""
linear = 0.0
linear_add = 0.03
angular = 0.0
angular_add = 0.1
max_linear = 0.27
max_angular = 1

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global msg_str
    global linear
    global angular
    # global add

    msg_str=msg.payload.decode("utf8")    
    if (msg.topic == 'agv/forward') and (linear < max_linear):
        linear = linear + linear_add
    elif (msg.topic == 'agv/backforward') and (linear > -max_linear):
        linear = linear - linear_add
    elif (msg.topic == 'agv/left') and (angular < max_angular):
        angular = angular + angular_add
    elif (msg.topic == 'agv/right') and (angular > -max_angular):
        angular = angular - angular_add
    elif msg.topic == 'agv/stop':
        linear = 0.0
        angular = 0.0
    # print(msg_str)
    # move(msg_str)

def move():
    global msg_str
    global linear
    global angular
    # global add
    
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) #/cmd_vel

    rate = rospy.Rate(10)#
    try:
        while True:
            while not (msg_str=='auto' or msg_str=='go to A' or msg_str=='go to B' or msg_str=='back to origin'): #rospy.is_shutdown():
                # if msg_str == 'go':
                #     linear = 0.1
                # elif msg_str == 'back':
                #     linear = -0.1
                if msg_str == 'stop':
                    linear = 0.0
                    angular = 0.0    

                print('move',msg_str,linear,angular)

                vel_msg = Twist()
                vel_msg.linear.x = linear
                vel_msg.angular.z = angular
                    # while not rospy.is_shutdown():
                velocity_publisher.publish(vel_msg)
                rate.sleep()
            linear = 0.0
            angular = 0.0

    except Exception as e:
        print(e)



if __name__ == '__main__':
    rospy.init_node('agv_control')
    command_thread = threading.Thread(target = move)
    command_thread.start()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect('10.87.1.110', port)
        # move()
        client.loop_forever()
    except rospy.ROSInterruptException: pass
    
