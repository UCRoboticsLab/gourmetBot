#!/usr/bin/env python

import argparse
import rospy
import time
import threading
import baxter_interface
from run_positions import move_list

from baxter_interface import CHECK_VERSION

rospy.init_node("cartesian_move")
left = baxter_interface.Limb('left')

pos_init = {'left_w0': left.joint_angles()['left_w0'],
            'left_w1': left.joint_angles()['left_w1'],
            'left_w2': left.joint_angles()['left_w2'],
            'left_e0': left.joint_angles()['left_e0'],
            'left_e1': left.joint_angles()['left_e1'],
            'left_s0': left.joint_angles()['left_s0'],
            'left_s1': left.joint_angles()['left_s1']}

pos_curr = {'left_w0': None,
            'left_w1': None,
            'left_w2': None,
            'left_e0': None,
            'left_e1': None,
            'left_s0': None,
            'left_s1': None}

def move_z(int):
    pos_curr = pos_init
    pos_curr['left_s1'] = pos_curr['left_s1'] + int
    move_list(arm='left', p_list=[pos_curr])


def main():
    move_z(0.1)
    move_z(0.1)
    move_z(0.1)


print("Executing cartesian_move...")
main()
print("Program executed.")
