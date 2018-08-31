#!/usr/bin/env python

import argparse
import rospy
import time
import baxter_interface
from run_positions import move_list

from baxter_interface import CHECK_VERSION


def main():

    def b0_pressed(v):
        print ("Button 0: %s" % (v,))

    def b1_pressed(v):
        grip_left.open(block=True, timeout=2.0)

    def b2_pressed(v):
        grip_left.close(block=True, timeout=2.0)

    def wheel_moved(v):
        print ("Wheel Increment: %d, New Value: %s" % (v, nav.wheel))
        angles = left.joint_angles()

        if v == 1:
            temp = angles['left_w2'] - 0.5
        elif v == -1:
            temp = angles['left_w2'] + 0.5

        pos = {'left_w2': temp}

        move_list(arm='left', p_list=[pos], timeout=0.05)

    rospy.init_node("navigator_test")
    left = baxter_interface.Limb('left')
    left.set_joint_position_speed(1.0)
    grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
    nav = baxter_interface.Navigator('left')

    nav.button0_changed.connect(b0_pressed)
    nav.button1_changed.connect(b1_pressed)
    nav.button2_changed.connect(b2_pressed)
    nav.wheel_changed.connect(wheel_moved)

    while not rospy.is_shutdown():
        rate = rospy.Rate(1)
        rate.sleep()


print("Navigator running...")
main()
print("Program executed.")
