#!/usr/bin/env python

import argparse
import rospy
import baxter_interface
from run_positions import move_list

from baxter_interface import CHECK_VERSION


def main():

    rospy.init_node("hand_wave")
    left = baxter_interface.Limb('left')

    position_1 = ({'left_w0': -3.0476363268493656, 'left_w1': -0.05867476506958008, 'left_w2': -3.0587576875488285, 'left_e0': -3.041500403704834, 'left_e1': 1.8821944245849611, 'left_s0': -0.7171360175170899, 'left_s1': 0.6043884297363281})

    position_2 = ({'left_e0': -2.2})

    left.set_joint_position_speed(0.75)

    move_list(neutral=False, arm='left', p_list=[position_1], threshold=0.1)
    for i in range(2):
        move_list(neutral=False, arm='left', p_list=[position_2, position_1], timeout=0.8)

    left.move_to_neutral(15.0)


main()
