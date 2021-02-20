#!/usr/bin/env python

import rospy
import cv2
import urllib2
import yaml
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CameraInfo




def camera():
    pub = rospy.Publisher('camera1_topic', Image, queue_size = 2)
    #caminfo = rospy.Publisher('camera_info', CameraInfo, queue_size=10)
    rospy.init_node('camera1', anonymous=True)
    bridge = CvBridge()
    #camera_info_msg = camera_info('ost.yaml')
    stream = urllib2.urlopen(urllib2.Request('http://10.10.10.123:5000/video_feed'))
    bytes= b''
    
    while not rospy.is_shutdown():
        bytes += stream.read(1024)

        a = bytes.find(b'\xff\xd8')  # JPEG start

        b = bytes.find(b'\xff\xd9')  # JPEG end

        if a!=-1 and b!=-1:

            jpg = bytes[a:b+2] # actual image

            bytes= bytes[b+2:] # other informations


            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            #caminfo.publish(camera_info_msg)
            
            pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
            


def camera_info(yaml_faname):

    with open(yaml_faname, 'r') as file_handle:
        calib_data = yaml.load(file_handle)
    # Parse
    camera_info_msg = CameraInfo()
    camera_info_msg.width = calib_data["image_width"]
    camera_info_msg.height = calib_data["image_height"]
    camera_info_msg.K = calib_data["camera_matrix"]["data"]
    camera_info_msg.D = calib_data["distortion_coefficients"]["data"]
    camera_info_msg.R = calib_data["rectification_matrix"]["data"]
    camera_info_msg.P = calib_data["projection_matrix"]["data"]
    camera_info_msg.distortion_model = calib_data["distortion_model"]
    return camera_info_msg


if __name__ == '__main__':


    try:
        camera()
    except rospy.ROSInterruptException:
        pass
    cv2.destroyAllWindows()


