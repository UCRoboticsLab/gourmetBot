#!/usr/bin/env python

import argparse
import rospy
import time
import baxter_interface
from run_positions import move_list
import simpleaudio as sa
from baxter_interface import CHECK_VERSION


def main():

    rospy.init_node("salute")
    left = baxter_interface.Limb('left')

    position_1 = {'left_w0': -2.1360682446899415, 'left_w1': -0.11888351092529298, 'left_w2': -0.2795679982727051, 'left_e0': -2.3301168141357422, 'left_e1': 2.4382624595581057, 'left_s0': 0.004601942358398438, 'left_s1': 0.3413107249145508}

    move_list(neutral=False, arm='left', p_list=[position_1], threshold=0.1, speed=0.8)

    time.sleep(2.0)

    left.move_to_neutral(15.0)

print("Saluting...")
fc.LeftRightCheck.run()
print("Program executed.")
