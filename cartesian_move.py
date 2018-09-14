#!/usr/bin/env python

import argparse
import rospy
import time
import threading
import baxter_interface
from run_positions import cartesian_move_abs
from run_positions import cartesian_move_rel

from baxter_interface import CHECK_VERSION

rospy.init_node("cartesian_move")
left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')

def main():
    cartesian_move_rel('left', x=-0.1)


print("Executing cartesian_move...")
main()
print("Program executed.")
