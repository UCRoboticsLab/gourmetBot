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
from matplotlib import pyplot as plt

# Instantiate CvBridge
bridge = CvBridge()

i1,i2,i3,i4 = 0,0,0,0
button_increment = 5
show_colour = 'blue'
object_loc_arr = []
object_count = 0
str_img_1 = 'face_small.png'

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

def detect_objects(img_rgb, pt, w, h):
    global object_loc_arr, object_count
    global str_img_1
    if len(object_loc_arr) == 0:
        object_loc = ({'x': None, 'y': None})
        object_loc['x'] = pt[0]
        object_loc['y'] = pt[1]
        object_loc_arr.append(object_loc)
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv2.putText(img=img_rgb, text=str_img_1, org=(pt[0], pt[1] - int(0.1 * h)),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, thickness=2, color=(0, 0, 0))
        object_count += 1

    else:
        for i in range(len(object_loc_arr)):
            if abs(pt[0] - object_loc_arr[i]['x']) < 10 and abs(pt[1] - object_loc_arr[i]['y']) < 10:
                break
            elif i == len(object_loc_arr) - 1:
                new_object_loc = ({'x': None, 'y': None})
                new_object_loc['x'] = pt[0]
                new_object_loc['y'] = pt[1]
                object_loc_arr.append(new_object_loc)
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                cv2.putText(img=img_rgb, text="Circle.jpg", org=(pt[0], pt[1] - int(0.1 * h)),
                            fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, thickness=2, color=(0, 0, 0))
                object_count += 1

def image_callback(msg):
    global i1,i2,i3,i4,button_increment
    global colour
    global object_loc_arr, object_count
    global str_img_1

    camera_x_gap = 625
    camera_y_gap = 450

    try:
        # Convert your ROS Image message to OpenCV2
        img_rgb = bridge.imgmsg_to_cv2(msg, "bgr8")
    except:
        print("Error")
    else:
        MIN_MATCH_COUNT = 5

        img1 = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        img2 = cv2.imread('warning.png', 0)  # trainImage

        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

            for pt in src_pts:
                cv2.circle(img_rgb, (pt[0][0], pt[0][1]), 2, (0, 0, 255), 2)


        else:
            print ("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
            matchesMask = None

        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)

        img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

        cv2.imshow('res.png', img_rgb)

        cv2.waitKey(1)

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
