#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler  
import numpy as np
import math
import paho.mqtt.client as mqtt
from actionlib_tutorials.msg import my_msg

bdistence = 0.01

social_ID = []


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


    client.subscribe("human_data")

def on_message(client, userdata, msg):
    Mqtt_msg = msg.payload.decode('utf-8')
    #print(Mqtt_msg)
    s_msg = Mqtt_msg.split(',')
    m_data=[]
    
    for i in range(len(s_msg)-1):
        
        cost = []
        if s_msg[i] == 'id':
            cost.append(int(s_msg[i+1]))
            cost.append(float(s_msg[i+2])*bdistence)
            cost.append(float(s_msg[i+3])*bdistence)
            m_data.append(cost)
            #print(i)
            

    #print(m_data)
    point(m_data)

def get_radian(position1, position2):
    x1 = position1[0]
    y1 = position1[1]
    x2 = position2[0]
    y2 = position2[1]
    radian = math.atan2(y2-y1, x2-x1)
    return radian


def point(m_data):
    PCT = rospy.Publisher('point_cloud', Marker, queue_size=10)
    Car = rospy.Publisher('car', my_msg, queue_size=10)
    rospy.init_node('point', anonymous=True)
    cp = my_msg()
    
    #fake_x = (407.73981154498244)*0.01
    #fake_y = -(68.3835996914338)*0.01 
    camera_x = 1.82
    camera_y = -2.2
    radian = get_radian([1.82, -2.2], [3.09, 4.1]) # angle from (0, 0) to camera point
    t = rospy.Duration()

    dis_hu = dis(m_data)

    dis_back = dis_count(dis_hu)
    #print(dis_back)
    #print(social_ID)
    original = Marker()
    original.lifetime = t
    original.header.frame_id = "/map"
    original.ns = "my_namespace"
    original.id = 10
    original.type = original.POINTS
    original.action = original.ADD
    original.pose.orientation.w = 1
    original.pose.position.x = 0
    original.pose.position.y = 0
    original.pose.position.z = 0
    original.pose.orientation.x = 0.0
    original.pose.orientation.y = 0.0
    original.pose.orientation.z = 0.0
    original.pose.orientation.w = 1.0
    original.scale.x = 0.1
    original.scale.y = 0.1
    original.color.a = 1.0
    original.color.r = 1.0
    original.color.g = 0.0
    original.color.b = 0.0



    lines = Marker()
    lines.lifetime = t
    lines.header.frame_id = "/map"
    lines.ns = "my_namespace"
    lines.id = 3
    lines.type = original.LINE_STRIP
    lines.action = original.ADD
    lines.pose.position.x = 0
    lines.pose.position.y = 0
    lines.pose.position.z = 0
    lines.scale.x = 0.05
    lines.color.a = 1.0
    lines.color.r = 0.0
    lines.color.g = 1.0
    lines.color.b = 0.0

    social = Marker()
    social.lifetime = t
    social.header.frame_id = "/map"
    social.ns = "my_namespace"
    social.id = 4
    social.type = original.LINE_STRIP
    social.action = original.ADD
    social.pose.position.x = 0
    social.pose.position.y = 0
    social.pose.position.z = 0
    social.scale.x = 0.05
    social.color.a = 1.0
    social.color.r = 0.0
    social.color.g = 0.0
    social.color.b = 1.0




    #trans_pos = trans_coordinate(radian, camera_x, camera_y, fake_x, fake_y)
    triplePoints2 = []
    triplePoints3 = []
    carPoint = []
    '''triplePoints2 = []
    apoint2 = Point()
    apoint2.x = trans_pos[0]
    apoint2.y = trans_pos[1]'''
    
    for i in range(len(m_data)):
        
        trans_pos = trans_coordinate(radian, camera_x, camera_y, m_data[i][1], -m_data[i][2])
        apoint2 = Point()
        apoint2.x = trans_pos[0]
        apoint2.y = trans_pos[1]
        apoint2.z = 0
        triplePoints2.append(apoint2)


    for i in range(len(dis_hu)):

        
        #print(dis_hu[i])
        trans_pos = trans_coordinate(radian, camera_x, camera_y, dis_hu[i][0][1], -dis_hu[i][0][2])
        apoint = Point()
        apoint.x = trans_pos[0]
        apoint.y = trans_pos[1]
        apoint.z = 0
        
        trans_pos2 = trans_coordinate(radian, camera_x, camera_y, dis_hu[i][1][1], -dis_hu[i][1][2])
        apoint2 = Point()
        apoint2.x = trans_pos2[0]
        apoint2.y = trans_pos2[1]
        apoint2.z = 0
        

        if social_ID[i][2] > 100:
            social_x = ((trans_pos[0]+trans_pos2[0])/2.0)+0.2
            social_y = ((trans_pos[1]+trans_pos2[1])/2.0)+0.2
            carPoint.append(apoint)
            carPoint.append(apoint2)
            cp.id = 1
            cp.x = social_x
            cp.y = social_y
        else:
            triplePoints3.append(apoint)
            triplePoints3.append(apoint2)
            cp.id = 0
            cp.x = 0
            cp.y = 0
    
    #print(apoint2)
    #triplePoints2.append(apoint2)
    original.points = triplePoints2
    lines.points = triplePoints3
    social.points = carPoint
    #print(triplePoints2)
    #print(triplePoints3)
    PCT.publish(original)
    PCT.publish(lines)
    PCT.publish(social)
    Car.publish(cp)



def trans_coordinate(radian, xc1, yc1, xh2, yh2):
    vi_vc, vi = vector(0,0,xc1, yc1)
    vc_vh, vc = vector(0,0,xh2, yh2)

    trans_vh = rotation(radian, vc)

    vi_vh = [vi[0]+trans_vh[0, 0], vi[1]+trans_vh[0, 1]]
    #vi_vh = [trans_vh[0, 0], trans_vh[0, 1]]
    return vi_vh


def vector(x1, y1, x2, y2): # find vector from two point
    return math.sqrt(math.pow(x2-x1, 2)+math.pow(y2-y1, 2)), [x2-x1, y2-y1]

def rotation(the, vector): # find rotated vector


    cos = math.cos(the)
    sin = math.sin(the)
    matrix = np.array([[cos, sin], 
			[-sin, cos]])
    v = np.array([[vector[0], vector[1]]])
    trans_v = v.dot(matrix)
    
    return trans_v

def dis(perlist):
    dis_hu = []
    for i in range(len(perlist)-1):
        for j in range(i+1, len(perlist)):

            #print(perlist[i][1])
            x = perlist[i][1]-perlist[j][1]

            y = perlist[i][2]-perlist[j][2]

            c = math.sqrt((x*x)+(y*y))

            if c < (160*0.005):
                dis_hu.append([perlist[i],perlist[j]])

    return dis_hu

def dis_count(dis_hu):
    global social_ID
    #print(dis_hu)
    #print(social_ID)
    #print(3)
    if dis_hu:
        if social_ID:
            local_ID = []
            for i in range(len(dis_hu)):
                count = 0
                for j in range(len(social_ID)):
                    if dis_hu[i][0][0] == social_ID[j][0] and dis_hu[i][1][0] == social_ID[j][1]:
                        social_ID[j][2]+=1
                        local_ID.append(social_ID[j])
                        break
                    else:
                        count+=1
                if count == len(social_ID):
                    #social_ID.append([dis_hu[i][0][0], dis_hu[i][1][0], 0]) 
                    local_ID.append([dis_hu[i][0][0], dis_hu[i][1][0], 0]) 
            social_ID = local_ID
            #print(1)
        else:
            for i in range(len(dis_hu)):
                social_ID.append([dis_hu[i][0][0], dis_hu[i][1][0], 0])
            #print(2)
    else:
        social_ID = []
        #print(4)
    
    return dis_hu

if __name__ == '__main__':
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        #client.connect("10.10.11.190", 1883, 60)
        client.connect("10.10.11.144", 1883, 60)
        client.loop_forever()
        #point()
    except rospy.ROSInterruptException:
        pass
