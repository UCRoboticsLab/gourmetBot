#!/usr/bin/env python

import rospy
import baxter_interface
import time
from fluid_movement import fluid_move
from joint_position_keyboard_test import set_position_order

from baxter_interface import CHECK_VERSION

rospy.init_node("whisk")
left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
grip_right = baxter_interface.Gripper('right', CHECK_VERSION)


pos_in = dict(
    {
     'left_w0': -0.01,
     'left_w1': 1.22,
     'left_w2': -3.06,
     'left_e0': -0.29,
     'left_e1': 0.30,
     'left_s0': -0.44,
     'left_s1': -0.12
    }
)

pos_up = dict(
    {
     'left_w0': -0.26,
     #'left_w1': 1.22,
     #'left_w2': -3.06,
     'left_e0': -0.35,
     'left_e1': 0.39,
     #'left_s0': -0.44,
     #'left_s1': -0.12
    }
)

pos_out = dict(
    {
     'left_w0': -0.15,
     'left_w1': 1.72,
     #'left_w2': -3.06,
     'left_e0': -0.29,
     'left_e1': -0.05,
     #'left_s0': -0.44,
     #'left_s1': -0.12
    }

)

#left.set_joint_position_speed(1.0)
print(left.joint_velocities())
velocities = dict(
    {
    'left_w0': 0.0026215491950511934,
    'left_w1': -0.0026215491950511934,
    'left_w2': 0.013482253003120424,
    'left_e0': 0.010111689752340317,
    'left_e1': 0.00786464758515358,
    'left_s0': 0.019099858421087267,
    'left_s1': -0.014980281114578248
    }
)

left.set_joint_velocities()

'''
print("Moving to neutral")
left.move_to_neutral(10)
'''
'''
for i in range(3) :
    left.move_to_joint_positions(pos_in, 1.0, threshold=0.05)
    left.move_to_joint_positions(pos_up, 0.5, threshold=0.05)
    left.move_to_joint_positions(pos_out, 1.0, threshold=0.05)
'''