#!/usr/bin/env python

import argparse
import rospy
import baxter_interface
from run_positions import move_list

from baxter_interface import CHECK_VERSION


def main():

    rospy.init_node("Str")
    left = baxter_interface.Limb('left')

    position_1 = ({'left_w0': -0.054,
                   'left_w1': 1.370,
                   'left_w2': -1.926,
                   'left_e0': 0.244,
                   'left_e1': -0.027,
                   'left_s0': -0.633,
                   'left_s1': 0.007})

    position_2 = ({'left_w0': -0.054,
                   'left_w1': 1.104,
                   'left_w2': -2.095,
                   'left_e0': 0.243,
                   'left_e1': -0.049,
                   'left_s0': -0.668,
                   'left_s1': 0.018})

    position_3 = ({'left_w0': -0.054,
                   'left_w1': 0.904,
                   'left_w2': -2.200,
                   'left_e0': 0.243,
                   'left_e1': -0.069,
                   'left_s0': -0.698,
                   'left_s1': 0.018})

    position_4 = ({'left_w0': -0.054,
                   'left_w1': 1.104,
                   'left_w2': -2.095,
                   'left_e0': 0.243,
                   'left_e1': -0.049,
                   'left_s0': -0.668,
                   'left_s1': 0.018})


    position_5 = ({'left_w0': -0.054,
                   'left_w1': 1.370,
                   'left_w2': -1.926,
                   'left_e0': 0.244,
                   'left_e1': -0.027,
                   'left_s0': -0.633,
                   'left_s1': 0.007})

    left.set_joint_position_speed(0.75)

    move_list(neutral=False, arm='left', p_list=[position_1], threshold=1.0)
    """
    for i in range(1):
        move_list(neutral=False, arm='left', p_list=[position_2, position_3, position_4, position_5], timeout=10.0, threshold=1.0)

    left.move_to_neutral(15.0)
    """

print("String")

main()

print("String end")