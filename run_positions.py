#!/usr/bin/env python

import rospy
import baxter_interface
from baxter_core_msgs.msg import JointCommand
from baxter_interface import CHECK_VERSION

default_speed = 0.3
default_timeout = 15.0
default_threshold = 0.008726646

def move_list(neutral=False, arm=None, p_list=0, timeout=default_timeout, threshold=default_threshold, speed=default_speed):
	arm = arm.lower()

	if speed > 1.0:
		speed = 1.0
	elif speed <= 0.0:
		speed = 0.1

	if arm == 'l':
		arm = 'left'
	elif arm == 'r':
		arm = 'right'

	if arm == 'left' or arm == 'right':

		limb = baxter_interface.Limb(arm)

		limb.set_joint_position_speed(speed)

		if neutral:
			limb.move_to_neutral()

		for positions in p_list:
			limb.move_to_joint_positions(positions=positions, timeout=timeout, threshold=threshold)

		if neutral:
			limb.move_to_neutral()

		limb.set_joint_position_speed(default_speed)

	else:
		print("Error: {} is not a valid limb".format(arm))


def move_list_smooth(neutral=False, arm=None, p_list=0, timeout=default_timeout, threshold=default_threshold, speed=default_speed):
	arm = arm.lower()

	if speed > 1.0:
		speed = 1.0
	elif speed <= 0.0:
		speed = 0.1

	if arm == 'l':
		arm = 'left'
	elif arm == 'r':
		arm = 'right'

	if arm == 'left' or arm == 'right':

		limb = baxter_interface.Limb(arm)

		limb.set_joint_position_speed(speed)

		if neutral:
			limb.move_to_neutral()

		for positions in p_list:
			which_pos = True
			position_1 = []
			position_2 = [1.5, 0.5]

			pub_joints = rospy.Publisher('/robot/limb/left/joint_command', JointCommand, queue_size=2)
			rospy.init_node("hand_wave")
			rate = rospy.Rate(100)

			cmd_msg = JointCommand()
			cmd_msg.mode = JointCommand.POSITION_MODE
			cmd_msg.names = ['left_w1', 'left_w2']

		if neutral:
			limb.move_to_neutral()

		limb.set_joint_position_speed(default_speed)

	else:
		print("Error: {} is not a valid limb".format(arm))