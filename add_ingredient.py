#!/usr/bin/env python

import rospy
import baxter_interface
import time
from run_positions import move_list

from baxter_interface import CHECK_VERSION

print("Test")

rospy.init_node("add_ingredient")
left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
grip_right = baxter_interface.Gripper('right', CHECK_VERSION)


positions_1 = (
	{'right_w2': -2.6921,
	'right_e1': 0.0422,
	'right_w0': 2.6058,
	'right_w1': 0.4249,
	'right_s0': 0.8295,
	'right_s1': 0.4533,
	'right_e0': 0.0610}
	)

positions_2 = (
	{'right_s1': 0.15,
	'right_s0': 1.1136,
	'right_w0': -0.0912}
	)

positions_3 = (
	{'right_s1': 0.3,
	'right_s1': 0.3}
	)


print("Program started")

right.set_joint_position_speed(0.8)
move_list(neutral=False, arm='right', p_list=[positions_1])
grip_right.close()
time.sleep(0.5)
move_list(neutral=False, arm='right', p_list=[positions_2])
time.sleep(0.5)
move_list(neutral=False, arm='right', p_list=[positions_1])
grip_right.open()
time.sleep(0.5)
move_list(neutral=False, arm='right', p_list=[positions_3])
right.move_to_neutral(10)

print("Program executed")