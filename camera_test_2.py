#! /usr/bin/python
# Copyright (c) 2015, Rethink Robotics, Inc.

# Using this CvBridge Tutorial for converting
# ROS images to OpenCV2 images
# http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython

# Using this OpenCV2 tutorial for saving Images:
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html

# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image
import numpy as np
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2

# Instantiate CvBridge
bridge = CvBridge()

i1,i2,i3,i4 = 0,0,0,0

def image_callback(msg):
    global i1,i2,i3,i4
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except:
        print("Error")
    else:
        # Save your OpenCV2 image as a jpeg
        hsv = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2HSV)

        # Detect red
        lower_red = np.array([0, 30, 45])
        upper_red = np.array([5, 255, 255])

        # Test
        lower_test = np.array([i1, i2, i3])
        upper_test = np.array([i4, 255, 255])

        mask_test = cv2.inRange(hsv, lower_test, upper_test)
        test = cv2.bitwise_and(cv2_img, cv2_img, mask=mask_test)

        cv2.imshow('test', test)
        cv2.moveWindow('test', 800, 0)
        cv2.imshow('frame', cv2_img)
        cv2.moveWindow('frame', 0, 0)
        k = cv2.waitKey(5)
        if k == 27:
            rospy.signal_shutdown("shutdown")
        if k == 32:  # space
            print("i1: {}\ni2: {}\ni3: {}\ni4: {}\n".format(i1, i2, i3, i4))
        if k == 113:  # q
            i1 += 5
        if k == 97:  # a
            i1 -= 5
        if k == 119:  # w
            i2 += 5
        if k == 115:  # s
            i2 -= 5
        if k == 101:  # e
            i3 += 5
        if k == 100:  # d
            i3 -= 5
        if k == 114:  # r
            i4 += 5
        if k == 102:  # f
            i4 -= 5


def main():
    rospy.init_node('image_listener')
    # Define your image topic
    image_topic = "/cameras/left_hand_camera/image"
    # Set up your subscriber and define its callback
    rospy.Subscriber(image_topic, Image, image_callback)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()