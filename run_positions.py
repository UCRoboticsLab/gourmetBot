#!/usr/bin/env python

import rospy
import baxter_interface

from baxter_interface import CHECK_VERSION

def move_list(neutral=False, arm=None, p_list=0, timeout=15.0, threshold=0.008726646):
	arm = arm.lower()

	if arm == 'l':
		arm = 'left'
	elif arm == 'r':
		arm = 'right'

	if arm == 'left' or arm == 'right':

		limb = baxter_interface.Limb(arm)

		if neutral:
			limb.move_to_neutral()

		for positions in p_list:
			limb.move_to_joint_positions(positions=positions, timeout=timeout, threshold=threshold)

		if neutral:
			limb.move_to_neutral()

		print("move_list executed")

	else:
		print("Error: {} is not a valid limb".format(arm))
