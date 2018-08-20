#!/usr/bin/env python

import argparse
import rospy
import baxter_interface
from run_positions import move_list

from baxter_interface import CHECK_VERSION


def main():

    rospy.init_node("hand_wave")
    left = baxter_interface.Limb('left')

    position_1 = ({'left_w1': 1.0})
    position_2 = ({'left_w1': -1.0})

    print(left.joint_velocity('left_w1'))
    left.move_to_joint_positions(position_1)
    print(left.joint_velocity('left_w1'))
    left.move_to_joint_positions(position_2)
    print(left.joint_velocity('left_w1'))

main()
