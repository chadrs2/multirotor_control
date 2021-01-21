import numpy as np
import rospy
import airsim
import cv2
from cv_bridge import CvBridge

import std_msgs.msg
import sensor_msgs.msg

rospy.init_node("camera_processing", anonymous=True)
camera_publisher = rospy.Publisher("camera_drone1", sensor_msgs.msg.Image, queue_size=10)
# bridge = CvBridge()

client = airsim.MultirotorClient()
client.confirmConnection()

camera_publishing_rate = rospy.Rate(30) # 30hz
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

def parse_camera(in_image):
    img1d = np.fromstring(in_image.image_data_uint8, dtype=np.uint8) # get numpy array
    image = img1d.reshape(in_image.height, in_image.width, 3) # reshape array to 3 channel image array H X W X 3
    print(img1d.shape, image.shape, end='\r')
    # camera_publisher.publish(bridge.cv2_to_imgmsg(image))
    print(cv2.__file__)
    cv2.imshow('image', image)
    cv2.waitKey(1)

while not rospy.is_shutdown():
    parse_camera(client.simGetImages([airsim.ImageRequest("front_center_custom", airsim.ImageType.Scene, False, False)])[0])
    camera_publishing_rate.sleep()

cv2.destroyAllWindows()