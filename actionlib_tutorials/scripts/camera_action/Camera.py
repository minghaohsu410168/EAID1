#!/usr/bin/env python

import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import urllib2

#cam = cv2.VideoCapture('http://10.10.11.111:5000/video_feed?action=stream')
stream = urllib2.urlopen(urllib2.Request('http://10.10.11.111:5000/video_feed'))


def camera():
    pub = rospy.Publisher('camera1_topic', Image, queue_size = 2)
    rospy.init_node('camera1', anonymous=True)
    bridge = CvBridge()
    bytes= b''
    
    
    while not rospy.is_shutdown():
        bytes += stream.read(1024)

        a = bytes.find(b'\xff\xd8')  # JPEG start

        b = bytes.find(b'\xff\xd9')  # JPEG end


        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2] # actual image

            bytes= bytes[b+2:] # other informations
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            #ret, cimg = cam.read()
            #cv2.imshow('cframe', img)
            k = cv2.waitKey(1)
            pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
            



if __name__ == '__main__':


    try:
        camera()
    except rospy.ROSInterruptException:
        pass
    cv2.destroyAllWindows()


