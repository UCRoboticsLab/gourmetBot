#! /usr/bin/python

import argparse
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
import rospy

def show_image_callback(img_data):

    """The callback function to show image by using CvBridge and cv

    """

    bridge = CvBridge()

    try:

        cv_image = bridge.imgmsg_to_cv2(img_data, "bgr8")

    except:

        return

    '''
    if edge_detection == True:

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # customize the second and the third argument, minVal and maxVal

        # in function cv2.Canny if needed

        get_edge = cv2.Canny(blurred, 10, 100)

        cv_image = np.hstack([get_edge])
    '''

    edge_str = "(Edge Detection)" if edge_detection else ''

    cv_win_name = ' '.join([window_name, edge_str])

    cv2.namedWindow(cv_win_name, 0)

    # refresh the image on the screen

    cv2.imshow(cv_win_name, cv_image)

cv2.waitKey(3)

def main():

    """Camera Display Example

    """
    rospy.init_node('camera_display', anonymous=True)

    camera = intera_interface.Cameras()

    if not camera.verify_camera_exists(args.camera):
        rospy.logerr("Invalid camera name, exiting the example.")

        return

    camera.start_streaming(args.camera)

    rectify_image = not args.raw

    use_canny_edge = args.edge

    camera.set_callback(args.camera, show_image_callback,

                        rectify_image=rectify_image, callback_args=(use_canny_edge, args.camera))

    def clean_shutdown():

        print("Shutting down camera_display node.")

        cv2.destroyAllWindows()

    rospy.on_shutdown(clean_shutdown)

    rospy.loginfo("Camera_display node running. Ctrl-c to quit")

    rospy.spin()


if __name__ == '__main__':
    main()