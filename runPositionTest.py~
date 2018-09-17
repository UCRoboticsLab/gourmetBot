#!/usr/bin/env python

import argparse
import rospy
import time
import threading
import baxter_interface
from run_positions import move_list_smooth

from baxter_interface import CHECK_VERSION

pos_1 = {'left_w0': 1.170427339819336, 'left_w1': -0.04947088035278321, 'left_w2': 0.04256796681518555, 'left_e0': -1.196888508380127, 'left_e1': 0.08091748646850587, 'left_s0': 0.5403447319152832, 'left_s1': 0.1710388576538086}
pos_2 = {'left_w0': 1.185383652484131, 'left_w1': 0.011504855895996095, 'left_w2': -0.14726215546875002, 'left_e0': -1.2030244315246583, 'left_e1': -0.050237870745849615, 'left_s0': 0.485121423614502, 'left_s1': -0.09357282795410157}


rospy.init_node("hand_wave")
left = baxter_interface.Limb('left')

for i in range(3):
    move_list_smooth(arm='left', p_list=[pos_1, pos_2], speed=0.5, threshold=0.05)
