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

pos_1 = {'left_w0': -2.792612021154785, 'left_w1': 0.49432530833129884, 'left_w2': -0.041033986029052734, 'left_e0': -0.39193209085693365, 'left_e1': -0.05138835633544922, 'left_s0': 0.707932132800293, 'left_s1': 0.5779272611755372}

pos_2 = {'left_w0': -3.0196411775024417, 'left_w1': 1.0484758673217773, 'left_w2': 0.16643691529541016, 'left_e0': -0.6392864926208497, 'left_e1': -0.04947088035278321, 'left_s0': -0.09050486638183594, 'left_s1': 0.9809807127319337}

pos_3 = {'left_w0': -0.9349612891479493, 'left_w1': 0.9027476926391602, 'left_w2': 0.9871166358764649, 'left_e0': -0.7673738882629395, 'left_e1': -0.05062136594238282, 'left_s0': 0.20133497817993165, 'left_s1': 0.6224127039733887}

pos_4 = {'left_w0': -2.822141151287842, 'left_w1': 0.556835025366211, 'left_w2': 0.14457768909301758, 'left_e0': -0.5832961939270019, 'left_e1': -0.050237870745849615, 'left_s0': 0.6527088244995117, 'left_s1': 0.5200194864990235}


left.set_joint_position_speed(0.5)

if not grip_left.calibrated():
    grip_left.calibrate()
grip_left.open(block=True, timeout=2.0)
move_list(arm='left', p_list=[pos_4, pos_1])

if not grip_left.calibrated():
    grip_left.calibrate()
time.sleep(2.0)
grip_left.close(block=True, timeout=2.0)
move_list(arm='left', p_list=[pos_2, pos_3], threshold=0.1)
time.sleep(0.5)
move_list(arm='left', p_list=[pos_4], threshold=0.1)
move_list(arm='left', p_list=[pos_1])

grip_left.open(block=True, timeout=2.0)



