#!/usr/bin/env python

import argparse
import rospy
import baxter_interface
from run_positions import move_list

from baxter_interface import CHECK_VERSION


def main():

    rospy.init_node("hand_wave")
    left = baxter_interface.Limb('left')

    position_1 = ({'left_w2': 3.0})
    position_2 = ({'left_w2': -3.0})

    left.set_joint_position_speed(1.0)

    left.set_command_timeout(10.0)
    left.set_joint_velocities({'left_w1' : 0.2})
    print(left._pub_speed_ratio.name)

    for i in range(1):
        print('Velocity (left_w1):', left.joint_velocity('left_w1'))
        print('Effort (left_w1):', left.joint_effort('left_w1'))
        left.move_to_joint_positions(position_1)
        print('Velocity (left_w1):', left.joint_velocity('left_w1'))
        print('Effort (left_w1):', left.joint_effort('left_w1'))
        left.move_to_joint_positions(position_2, timeout=0.5)
        print('Velocity (left_w1):', left.joint_velocity('left_w1'))
        print('Effort (left_w1):', left.joint_effort('left_w1'))

main()
