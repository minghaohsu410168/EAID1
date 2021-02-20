#!/usr/bin/env python
import rospy
import paho.mqtt.client as mqtt
from geometry_msgs.msg import Twist
import threading
import math

port = 1883
MQTT_TOPIC='agv/+'
msg_str = ""
linear = 0.0
linear_add = 0.03
angular = 0.0
angular_add = 0.1
max_linear = 0.3
max_angular = 1
msg_o = ''
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global msg_str
    global linear
    global angular
    global msg_o
    msg_o = msg.payload.decode("utf8")
    msg_str=msg.payload.decode("utf8").split(',')
    print(msg_str[0]+'  '+msg_str[1])
    # print(math.cos(float(msg_str[1])*math.pi/180))
    if math.cos(float(msg_str[1])*math.pi/180) >= 0:
        print('go')
        linear = float(msg_str[0])*0.2
    elif math.cos(float(msg_str[1])*math.pi/180)<0:
        print('back')
        linear = -float(msg_str[0])*0.2
    
    if float(msg_str[1])>90 and float(msg_str[1])<270:
        angular = math.sin(float(msg_str[1])*math.pi/180)
    else:
        angular = -math.sin(float(msg_str[1])*math.pi/180)

def move():
    global msg_str
    global linear
    global angular
    # global add
    
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10) #/turtle1/cmd_vel
    rate = rospy.Rate(10)
    try:
        while True:
            while not (msg_o=='auto' or msg_o=='placeA' or msg_o=='placeB' or msg_o=='placeO'): #rospy.is_shutdown():
                print(msg_o)
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
    
