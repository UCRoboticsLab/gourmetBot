#!/usr/bin/env python

import argparse
import rospy
import time
import baxter_interface
from run_positions import move_list

from baxter_interface import CHECK_VERSION

pressed = False

def main():
    def left_pressed(v):
        global pressed
        pressed = not pressed
        if pressed:
            print(left.joint_angles())
            print


    def left_wheel_moved(v):
        print(left.joint_angles())
        print

    def right_pressed(v):
        pressed = not pressed
        if pressed:
            print(right.joint_angles())
            print

    def right_wheel_moved(v):
        print(right.joint_angles())
        print

    rospy.init_node("navigator_test")
    left = baxter_interface.Limb('left')
    grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
    nav_left = baxter_interface.Navigator('left')
    nav_right = baxter_interface.Navigator('right')

    nav_left.button0_changed.connect(left_pressed)
    nav_left.button1_changed.connect(left_pressed)
    nav_left.button2_changed.connect(left_pressed)
    nav_left.wheel_changed.connect(left_wheel_moved)

    nav_right.button0_changed.connect(right_pressed)
    nav_right.button1_changed.connect(right_pressed)
    nav_right.button2_changed.connect(right_pressed)
    nav_right.wheel_changed.connect(right_wheel_moved)

    while not rospy.is_shutdown():
        rate = rospy.Rate(1)
        rate.sleep()


print("Navigator running...")
main()
print("Program executed.")
