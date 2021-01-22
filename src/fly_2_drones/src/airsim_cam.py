#!/usr/bin/python3

import numpy as np
import airsim
import cv2

client = airsim.MultirotorClient()
client.confirmConnection()

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
inkey = 'a'

while inkey != 27:
    in_image = client.simGetImages([airsim.ImageRequest("front_center_custom", airsim.ImageType.Scene, False, False)])[0]
    img1d = np.fromstring(in_image.image_data_uint8, dtype=np.uint8) # get numpy array
    image = img1d.reshape(in_image.height, in_image.width, 3) # reshape array to 3 channel image array H X W X 3
    # print(img1d.shape, image.shape, end='\r')
    cv2.imshow('image', image)
    inkey = cv2.waitKey(1)

cv2.destroyAllWindows()