#!/usr/bin/env python

import argparse
import rospy
import time
import baxter_interface
import threading
from sensor_msgs.msg import Range
from run_positions import move_list

from baxter_interface import CHECK_VERSION


def move_arm():

    pos_arm_down = {'left_w0': 0.04141748122558594, 'left_w1': -0.031446606115722656, 'left_w2': -0.04141748122558594, 'left_e0': -0.042951462011718754, 'left_e1': -0.034898062884521484, 'left_s0': -0.8206797205810548, 'left_s1': 0.39193209085693365}

    move_list(neutral=False, arm='left', p_list=[pos_arm_down])


def check_effort():

    left = baxter_interface.Limb('left')

    print (left.joint_efforts())

def main():

    rospy.init_node("height_check")
    left = baxter_interface.Limb('left')

    pos_arm_up = {'left_w0': 0.04180097642211914, 'left_w1': -0.042184471618652346, 'left_w2': -0.026461168560791018, 'left_e0': -0.042184471618652346, 'left_e1': -0.04985437554931641, 'left_s0': -0.8356360332458497, 'left_s1': -0.031063110919189455}

    left.set_joint_position_speed(0.1)

    move_list(neutral=False, arm='left', p_list=[pos_arm_up])

    thread_move_arm = threading.Thread(name='move_arm', target=move_arm)
    thread_check_effort = threading.Thread(name='check_effort', target=check_effort)
    thread_move_arm.start()
    thread_check_effort.start()

    left.set_joint_position_speed(0.1)

print("Checking height...")

print("Program executed.")
