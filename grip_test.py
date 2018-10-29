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

#left.set_joint_position_speed(0.5)
grip_left.set_moving_force(90)
grip_left.set_velocity(90)

#grip_left.calibrate()
grip_left.open(block=True, timeout=15.0)

#if not grip_0left.calibrated():
time.sleep(3.0)
grip_left.close(block=True, timeout=15.0)

#grip_left.open(block=True, timeout=15.0)
'''
for i in range(10):
    time.sleep(1.0)
    grip_left.command_position(10 * i, timeout=15.00)
'''


