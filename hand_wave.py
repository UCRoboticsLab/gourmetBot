#!/usr/bin/env python

import argparse
import rospy
import baxter_interface
from run_positions import move_list

from baxter_interface import CHECK_VERSION


def main():

    rospy.init_node("hand_wave")
    left = baxter_interface.Limb('left')

    position_init = left.joint_angles()
    position_1 = ({'left_w0': -3.0476363268493656, 'left_w1': -0.05867476506958008, 'left_w2': -3.0587576875488285, 'left_e0': -3.041500403704834, 'left_e1': 1.8821944245849611, 'left_s0': -0.7171360175170899, 'left_s1': 0.6043884297363281})
    position_2 = ({'left_e0': -2.5})


    move_list(arm='left', p_list=[position_1], threshold=0.05, speed=0.8)
    for i in range(2):
        move_list(arm='left', p_list=[position_2, position_1], threshold=0.05, speed=0.8)

    move_list(arm='left', p_list=[position_init], threshold=0.05, speed=0.5)

main()
