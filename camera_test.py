#!/usr/bin/env python
import os
import sys
import argparse
import rospy
import cv2
import cv_bridge
import numpy
import baxter_interface
from sensor_msgs.msg import Image

rospy.init_node("my_cam")
display_pub= rospy.Publisher('/robot/xdisplay',Image)
def republish(msg):
    print("test")
    """
        Sends the camera image to baxter's display
    """
    display_pub.publish(msg)

left_camera = baxter_interface.CameraController("left_hand_camera")

left_camera.resolution =(960, 600)
left_camera.open()
camera_name = "left_hand_camera"
sub = rospy.Subscriber('/cameras/' + camera_name + "/image", Image,republish,None,1)
rospy.spin()