#!/usr/bin/env python

import rospy
import baxter_interface
import time
from run_positions import move_list

from baxter_interface import CHECK_VERSION

rospy.init_node("whisk")
left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
grip_right = baxter_interface.Gripper('right', CHECK_VERSION)


if not grip_left.calibrated():
    grip_left.calibrate()
grip_left.open()
