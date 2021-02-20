#!/usr/bin/env python
import rospy
from beginner_tutorials.msg import my_msg
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import math



bdistence = 0.0050000 #((1.0154+4.2614)/960)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


    client.subscribe("MQTT")

def on_message(client, userdata, msg):
    Mqtt_msg = msg.payload.decode('utf-8')
    print(Mqtt_msg)
    s_msg = Mqtt_msg.split(',')
    #print(s_msg)
    m_data=[]
    
    for i in range(len(s_msg)-1):
        
        cost = []
        if s_msg[i] == 'id':
            if  int(s_msg[i+1]) == -1:
                cost.append(int(s_msg[i+1]))
                cost.append(float(s_msg[i+2]))
                cost.append(float(s_msg[i+3]))
                m_data.append(cost)
                print(i)




            else:
                cost.append(int(s_msg[i+1]))
                cost.append(float(s_msg[i+2])*bdistence)
                cost.append(float(s_msg[i+3])*bdistence)
                m_data.append(cost)
                print(i)
            

    #print(m_data)
    point(m_data)
    


def point(m_data):

    #print(m_data)

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
    triplePoints.append(apoint)
marker.points = triplePoints
PCT.publish(marker)



    lines = Marker()
    lines.lifetime = t
    lines.header.frame_id = "/map"
    lines.ns = "my_namespace"
    lines.id = 3
    lines.type = marker.LINE_STRIP
    lines.action = marker.ADD
    lines.pose.position.x = -4.0056 #-3.4565
    lines.pose.position.y = 0.48351
    lines.pose.position.z = 0
    lines.scale.x = 0.05
    lines.color.a = 1.0
    lines.color.r = 0.0
    lines.color.g = 1.0
    lines.color.b = 0.0

#-4.2982; 0.48611; -0.39669
#0.90577; 0.42169; -0.39149
#-3.9106; 0.25341; -0.0039073

#-4.0056; 0.48351; -0.0039984
#-4.2614; 0.84559; -0.42789

#1.0154; 0.51803; 0.0010225


    
    #rate = rospy.Rate(10) # 10hz
    triplePoints = []
    triplePoints2 = []
    
    for i in range(len(m_data)):
        
        if m_data[i][0] == 99:
            triplePoints2.append(apoint)

    #print(m_data)
    
    lines.points = triplePoints2
    print(triplePoints)
    print(triplePoints2)

    
    PCT.publish(lines)
    #rate.sleep()

def dis(perlist):
    for i in range(len(perlist)-1):
        for j in range(i+1, len(perlist)):
            #print(perlist[i][1])
            x = perlist[i][1]-perlist[j][1]

            y = perlist[i][2]-perlist[j][2]

            c = math.sqrt((x*x)+(y*y))

            if c < (150*0.005):

                perlist[i][0] = 99
                perlist[j][0] = 99

    return perlist

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
