#!/usr/bin/env python

import rospy
import baxter_interface
import time
from run_positions import move_list
from joint_position_keyboard_test import set_position_order

from baxter_interface import CHECK_VERSION

rospy.init_node("whisk")
left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
grip_right = baxter_interface.Gripper('right', CHECK_VERSION)


pos_in = dict(
    {'left_w0': -0.01,
     'left_w1': 1.22,
     'left_w2': -3.06,
     'left_e0': -0.29,
     'left_e1': 0.30,
     'left_s0': -0.44,
     'left_s1': -0.12}
    )

pos_up = dict(
    {'left_w0': -0.26,
     'left_e0': -0.35,
     'left_e1': 0.39}
    )

pos_out = dict(
    {'left_w0': -0.15,
     'left_w1': 1.72,
     'left_e0': -0.29,
     'left_e1': -0.05,}
    )

pos_2 = ({'left_w0': -0.02,
          'left_w1': 0.81,
          'left_w2': -3.05,
          'left_e0': -0.28,
          'left_e1': 0.20,
          'left_s0': -0.55,
          'left_s1': -0.05})

pos_3 = ({'left_w0': -0.17,
          'left_w1': 1.64,
          'left_w2': -3.05,
          'left_e0': -0.29,
          'left_e1': -0.03,
          'left_s0': -0.65,
          'left_s1': -0.02})

pos_2_2 = ({'left_w0': -0.02,
            'left_w1': 0.4,
            'left_w2': -3.05,
            'left_e0': -0.28,
            'left_e1': 0.10,
            'left_s0': -0.65,
            'left_s1': -0.00})

pos_3_2 = ({'left_w0': -0.30,
            'left_w1': 2.40,
            'left_w2': -3.05,
            'left_e0': -0.29,
            'left_e1': -0.60,
            'left_s0': -0.75,
            'left_s1': -0.00})

pos_a = ()

pos_b = ()

pos_c = ()

pos_d = ()


left.set_joint_position_speed(1.0)

move_list(arm='left', p_list=[pos_in])

for i in range(5):
    left.set_joint_position_speed(1.0)
    move_list(arm='left', p_list=[pos_in, pos_2_2, pos_3_2], timeout=0.3)

left.move_to_neutral(15.0)
