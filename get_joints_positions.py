#!/usr/bin/env python

import rospy
import baxter_interface
import argparse

from baxter_interface import CHECK_VERSION


def main():
    rospy.init_node("get_joints_position")

    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')

    parser = argparse.ArgumentParser(description='Prints out joint positions.')
    parser.add_argument('arm', metavar='C', type=str, nargs='?',
                        help='Left(l) or Right(r) arm', choices=['l','r'])
    args = parser.parse_args()

    if args.arm == None:
        print(left.joint_angles())
        print(right.joint_angles())
    else:
        arm = args.arm[0]
        if arm == 'l':
            print(left.joint_angles())
        elif arm == 'r':
            print(right.joint_angles())

main()
