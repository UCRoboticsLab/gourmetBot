#!/usr/bin/env python

import rospy
import baxter_interface
import time
from fluid_movement import fluid_move
from joint_position_keyboard_test import set_position_order

from baxter_interface import CHECK_VERSION

rospy.init_node("Test")
left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
grip_right = baxter_interface.Gripper('right', CHECK_VERSION)

'''
def fluid_move(limb, timeout=15.0, positions=[0.0, -0.55, 0.0, 0.75, 0.0, 0.0, 1.0]):
	print("Running fluid move")
	angles = dict(zip(limb.joint_names(), positions))
	return limb.move_to_joint_positions(angles, timeout)
'''

positions_1 = (
	{'right_w2': -2.6921},
	{'right_e1': 0.0422},
	{'right_w0': 2.6058},
	{'right_w1': 0.4249},
	{'right_s0': 0.8295},
	{'right_s1': 0.4533},
	{'right_e0': 0.0610}
	)

positions_test = [0.8295, 0.4533, 0.0610, 0.0422, 2.6058, 0.4249, -2.6921]

positions_2 = (
	{'right_s1': 0.15},
	{'right_s0': 1.1136},
	{'right_w0': -0.0912}
	)
'''
positions_3 = (
	{'right_w0': 2.6058},
	{'right_w0': 2.6058}
	)
'''

positions_3 = (
	{'left_w1': 0},
	{'left_w2': 1}
	)

positions_4 = (
	{'right_s1': 0.3},
	{'right_s1': 0.3}
	)

print("Moving to neutral")
#right.move_to_neutral(10)

fluid_move(right, 15, positions_test)

print("Program executed")
'''
for pos in positions_1:
	print(pos)
	right.move_to_joint_positions(pos)

grip_right.calibrate()
grip_right.close()

time.sleep(1)

for pos in positions_2:
	print(pos)
	right.move_to_joint_positions(pos)

time.sleep(1)

for pos in positions_1:
	print(pos)
	right.move_to_joint_positions(pos)

grip_right.calibrate()
grip_right.open()

time.sleep(1)

for pos in positions_4:
	print(pos)
	right.move_to_joint_positions(pos)


right.move_to_neutral(10)
'''
