#!/usr/bin/env python

import argparse
import rospy
import time
import baxter_interface
from run_positions import move_list

from baxter_interface import CHECK_VERSION


def check_effort(limb):
    temp = {}
    current = {}
    diff_high = {'left_w0': 0.0, 'left_w1': 0.0, 'left_w2': 0.0, 'left_e0': 0.0, 'left_e1': 0.0, 'left_s0': 0.0, 'left_s1': 0.0}


    while not rospy.is_shutdown():
        if len(temp) == 0:
            temp = limb.joint_efforts()
        else:
            temp = current

        current = limb.joint_efforts()

        for i, j in current.items():
            if abs(j - temp[i]) > diff_high[i]:
                diff_high[i] = abs(j - temp[i])
                print("New Highest Difference ({}): {}".format(i, diff_high[i]))

        time.sleep(0.1)

    print()
    for i, j in diff_high.items():
        print('{}: {:.3f}'.format(i, j))


def main():

    rospy.init_node("effort_test")
    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')

    check_effort(left)


print("Printing effort...")
main()
print("Program executed.")
