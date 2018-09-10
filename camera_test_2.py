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
button_increment = 5
show_colour = 'blue'

def min_max_numbers():
    global i1,i2,i3,i4
    if i1 > 180:
        i1 = 180
    if i1 < 0:
        i1 = 0
    if i2 > 255:
        i2 = 255
    if i2 < 0:
        i2 = 0
    if i3 > 255:
        i3 = 255
    if i3 < 0:
        i3 = 0
    if i4 > 180:
        i4 = 180
    if i4 < 0:
        i4 = 0


def show_img(colour):
    if colour == 'test':
        lower_test = np.array([i1, i2, i3])
        upper_test = np.array([i4, 255, 255])
        return lower_test, upper_test

    elif colour == 'orange':
        lower_orange = np.array([5, 130, 90])
        upper_orange = np.array([15, 255, 255])
        return lower_orange, upper_orange

    elif colour == 'blue':
        lower_blue = np.array([105,110,50])
        upper_blue = np.array([115, 255, 255])
        return lower_blue, upper_blue

    elif colour == 'green':
        lower_green = np.array([45, 70, 65])
        upper_green = np.array([90, 255, 255])
        return lower_green, upper_green

    elif colour == 'red':
        lower_red = np.array([1, 129, 41])
        upper_red = np.array([5, 255, 255])
        return lower_red, upper_red



def image_callback(msg):
    global i1,i2,i3,i4,button_increment
    global colour

    camera_x_gap = 625
    camera_y_gap = 450

    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except:
        print("Error")
    else:
        # Save your OpenCV2 image as a jpeg
        hsv = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2HSV)

        lower_colour, upper_colour = show_img(show_colour)
        mask_colour = cv2.inRange(hsv, lower_colour, upper_colour)
        colour = cv2.bitwise_and(cv2_img, cv2_img, mask=mask_colour)
        mask_colour_blur = cv2.GaussianBlur(mask_colour,(9,9),0)
        ret3,mask_colour_blur_otsu = cv2.threshold(mask_colour_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        mask_colour_blur_otsu_edge = cv2.Canny(mask_colour_blur_otsu, 0, 1000)

        cv2.imshow('frame', cv2_img)
        cv2.moveWindow('frame', 0, 0)
        cv2.imshow('colour', colour)
        cv2.moveWindow('colour', camera_x_gap, 0)
        cv2.imshow('mask_colour', mask_colour)
        cv2.moveWindow('mask_colour', 0, camera_y_gap)
        cv2.imshow('mask_colour_blur_otsu', mask_colour_blur_otsu)
        cv2.moveWindow('mask_colour_blur_otsu', camera_x_gap, camera_y_gap)
        cv2.imshow('mask_colour_blur_otsu_edge', mask_colour_blur_otsu_edge)
        cv2.moveWindow('mask_colour_blur_otsu_edge', camera_x_gap * 2, camera_y_gap)

        k = cv2.waitKey(5)
        if k == 27:
            rospy.signal_shutdown("shutdown")
        if k == 32:  # space
            print("i1: {}\ni2: {}\ni3: {}\ni4: {}\n".format(i1, i2, i3, i4))
        if k == 113:  # q
            i1 += button_increment
        if k == 97:  # a
            i1 -= button_increment
        if k == 119:  # w
            i2 += button_increment
        if k == 115:  # s
            i2 -= button_increment
        if k == 101:  # e
            i3 += button_increment
        if k == 100:  # d
            i3 -= button_increment
        if k == 114:  # r
            i4 += button_increment
        if k == 102:  # f
            i4 -= button_increment
        min_max_numbers()


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