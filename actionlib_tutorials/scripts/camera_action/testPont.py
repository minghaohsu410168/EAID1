from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler  
import math

q = quaternion_from_euler(0.0, 0.0, 0.25*math.pi,) #axes='sxyz'
print(q)