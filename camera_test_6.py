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
import threading
from run_positions import cartesian_move_rel
from run_positions import move_list_smooth
import time
import baxter_interface
from baxter_interface import CHECK_VERSION


# Instantiate CvBridge
bridge = CvBridge()

i1,i2,i3,i4 = 0,0,0,0
button_increment = 5
template_repeat_threshold = 60
show_colour = 'blue'
object_loc_arr = []
object_count = 0
str_img_1 = 'Cake.png'
img_w, img_h, obj_w, obj_h = 0,0,0,0
boRun = True
startPos = {'left_w0': 0.29950974849243167, 'left_w1': 1.3993739721496583, 'left_w2': 0.18714565590820315, 'left_e0': -0.2803349886657715, 'left_e1': 0.5357427895568848, 'left_s0': -0.3880971388916016, 'left_s1': -0.3915485956604004}

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

def align_camera():
    global img_w, obj_w, img_h, obj_h
    global boRun
    speed = 0.0005

    while boRun:
        x_move = 0.0
        z_move = 0.0
        if abs((img_w * 0.5) - obj_w) > 20:
            if (img_w * 0.5) < obj_w:
                x_move = speed
                #cartesian_move_rel(limb="left", x=0.001*abs((img_w * 0.5) - obj_w), y=0.0, z=0.0)
            elif (img_w * 0.5) > obj_w:
                x_move = -speed
                #cartesian_move_rel(limb="left", x=-0.001*abs((img_w * 0.5) - obj_w), y=0.0, z=0.0)

        if abs((img_h * 0.5) - obj_h) > 20:
            if abs((img_h * 0.5) - obj_h) > 20:
                if (img_h * 0.5) < obj_h:
                    z_move = -speed
                    # cartesian_move_rel(limb="left", x=0.001*abs((img_w * 0.5) - obj_w), y=0.0, z=0.0)
                # cartesian_move_rel(limb="left", x=0.0, y=0.0, z=0.0)
                elif (img_h * 0.5) > obj_h:
                    z_move = speed
                    # cartesian_move_rel(limb="left", x=-0.001*abs((img_w * 0.5) - obj_w), y=0.0, z=0.0)
                # cartesian_move_rel(limb="left", x=0.0, y=0.0, z=0.0)
        print(abs((img_w * 0.5) - obj_w))
        if x_move == 0.0 and z_move == 0.0:
            print("centered")
        else:
            #cartesian_move_rel(limb="left", x=x_move, y=0.0, z=z_move, threshold=0.1)
            cartesian_move_rel(limb="left", x=x_move * abs((img_w * 0.5) - obj_w), y=0.0, z=z_move * abs((img_h * 0.5) - obj_h), threshold=0.1)

        obj_w = img_w * 0.5
        obj_h = img_h * 0.5
        time.sleep(0.19)

def detect_objects(img_rgb, pt, w, h):
    global object_loc_arr, object_count
    global str_img_1, template_repeat_threshold
    global img_h, img_w, obj_h, obj_w

    cv2.circle(img_rgb, (int(img_w * 0.5), int(img_h * 0.5)), 1, (0, 0, 255), 2)

    if len(object_loc_arr) == 0:
        object_loc = ({'x': None, 'y': None})
        object_loc['x'] = pt[0]
        object_loc['y'] = pt[1]
        object_loc_arr.append(object_loc)
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        center = pt[0] + (w * 0.5), pt[1] + (h * 0.5)
        cv2.circle(img_rgb, (int(center[0]), int(center[1])), 1, (0, 255, 0), 2)
        cv2.putText(img=img_rgb, text=str_img_1, org=(pt[0], pt[1] - int(0.1 * h)),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, thickness=2, color=(0, 0, 0))
        img_h, img_w, img_channel = img_rgb.shape
        obj_h, obj_w = center[1], center[0]

        object_count += 1

    else:
        for i in range(len(object_loc_arr)):
            if abs(pt[0] - object_loc_arr[i]['x']) < template_repeat_threshold and abs(pt[1] - object_loc_arr[i]['y']) < template_repeat_threshold:
                break
            elif i == len(object_loc_arr) - 1:
                new_object_loc = ({'x': None, 'y': None})
                new_object_loc['x'] = pt[0]
                new_object_loc['y'] = pt[1]
                object_loc_arr.append(new_object_loc)
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                cv2.putText(img=img_rgb, text=str_img_1, org=(pt[0], pt[1] - int(0.1 * h)),
                            fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, thickness=2, color=(0, 0, 0))
                object_count += 1



def image_callback(msg):
    global i1,i2,i3,i4,button_increment
    global colour
    global object_loc_arr, object_count
    global str_img_1
    global boRun

    camera_x_gap = 625
    camera_y_gap = 450

    try:
        # Convert your ROS Image message to OpenCV2
        img_rgb = bridge.imgmsg_to_cv2(msg, "bgr8")
    except:
        print("Error")
    else:
        # Save your OpenCV2 image as a jpeg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(str_img_1, 0)
        template2 = cv2.imread('Cross.jpg', 0)
        w, h = template.shape[::-1]
        w2, h2 = template2.shape[::-1]

        threshold = 0.7

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            detect_objects(img_rgb, pt, w, h)
        object_loc_arr = []
        object_count = 0

        res2 = cv2.matchTemplate(img_gray, template2, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res2 >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)

        cv2.imshow('res.png', img_rgb)
        if cv2.waitKey(5) & 0xff == 27:
            boRun = False
            rospy.signal_shutdown("user exit")
            cv2.destroyAllWindows()

def get_image():
    # Define your image topic
    image_topic = "/cameras/left_hand_camera/image"
    # Set up your subscriber and define its callback
    rospy.Subscriber(image_topic, Image, image_callback)
    # Spin until ctrl + c
    while not rospy.is_shutdown():
        rospy.spin()

def main():
    rospy.init_node('image_listener')
    thread_get_image = threading.Thread(name='get_image', target=get_image)
    thread_align_camera = threading.Thread(name='align_camera', target=align_camera)
    thread_get_image.start()
    thread_align_camera.start()

if __name__ == '__main__':
    main()
