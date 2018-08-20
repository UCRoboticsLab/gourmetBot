#!/usr/bin/env python

import argparse
import rospy
import baxter_interface
from run_positions import move_list

from baxter_interface import CHECK_VERSION


def main():

    rospy.init_node("neutral")
    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')

    left.move_to_neutral(15.0)
    right.move_to_neutral(15.0)

print("Moving to neutral...")
main()
print("Program executed.")
