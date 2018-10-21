#!/usr/bin/env python

import argparse
import rospy
import time
import baxter_interface
from run_positions import move_list_smooth

from baxter_interface import CHECK_VERSION


def main():

    rospy.init_node("salute")
    left = baxter_interface.Limb('left')

    position_1 = {'left_w0': 0.6128253240600586, 'left_w1': 1.361024452496338, 'left_w2': -1.6409759459655764, 'left_e0': 0.053689327514648444, 'left_e1': 0.9679418760498048, 'left_s0': 1.7023351774108888, 'left_s1': -0.14994662184448243}

    move_list_smooth(neutral=False, arm='left', p_list=[position_1], threshold=0.1)

    time.sleep(2.0)

    left.move_to_neutral(15.0)

print("Saluting...")
main()
print("Program executed.")
