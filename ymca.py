#!/usr/bin/env python

import argparse
import rospy
import time
import threading
import baxter_interface
from run_positions import move_list_smooth

from baxter_interface import CHECK_VERSION


def main():

    rospy.init_node("ymca")

    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')

    left_thread = MoveLeft(arm=left)
    right_thread = MoveRight(arm=right)

    left_thread.start()
    right_thread.start()


class MoveLeft(threading.Thread):

    def __init__(self, arm):
        super(MoveLeft, self).__init__()
        self.arm = arm

    def run(self):

        pos_y_left = {'left_w0                                                                                                                                                                      ': 0.030296120526123047, 'left_w1': 0.03758252926025391, 'left_w2': -2.852820767010498,
                      'left_e0': -3.0349809853637697, 'left_e1': -0.01457281746826172, 'left_s0': 0.49739326990356447,
                      'left_s1': -1.087208882171631}

        pos_m_left = {'left_w0': 0.683388440222168, 'left_w1': 1.7817186830932619, 'left_w2': -0.6055389153259277, 'left_e0': -3.0250101102539064, 'left_e1': 1.2601652158081056, 'left_s0': 0.15148060263061525, 'left_s1': -0.5890486218750001}

        pos_c_left = {'left_w0': -0.23661653626098633, 'left_w1': 0.3271214026428223, 'left_w2': -3.0587576875488285, 'left_e0': -3.040733413311768, 'left_e1': 1.0829904350097657, 'left_s0': 0.645422415765381, 'left_s1': 0.43334957208251956}

        pos_a_left = {'left_w0': 0.27534955111083986, 'left_w1': 0.1326893380004883, 'left_w2': 0.12156797730102539, 'left_e0': -2.780340174865723, 'left_e1': 1.2011069555419922, 'left_s0': -0.011888351092529297, 'left_s1': -0.7712088402282715}

        self.arm.set_joint_position_speed(0.8)

        move_list_smooth(neutral=False, arm='left', p_list=[pos_y_left, pos_m_left, pos_c_left, pos_a_left], threshold=0.2, speed=0.8)

        time.sleep(1.0)

        self.arm.move_to_neutral(15.0)

class MoveRight(threading.Thread):

    def __init__(self, arm):
        super(MoveRight, self).__init__()
        self.arm = arm

    def run(self):

        pos_y_right = {'right_s0': -0.4755340437011719, 'right_s1': -1.0722525695068361, 'right_w0': 0.13690778516235352,
         'right_w1': 0.1334563283935547, 'right_w2': 2.6476508368652345, 'right_e0': 3.050704288421631,
         'right_e1': -0.013422331878662111}

        pos_m_right = {'right_s0': -0.08436894323730469, 'right_s1': -0.4878058899902344, 'right_w0': -0.3413107249145508, 'right_w1': 1.7521895529602052, 'right_w2': 0.20171847337646487, 'right_e0': 2.9437091285888672, 'right_e1': 1.2471263791259766}

        pos_c_right = {'right_s0': -0.679553488256836, 'right_s1': -1.1017816996398926, 'right_w0': 0.37927674937133793, 'right_w1': 0.9223059476623536, 'right_w2': -0.22549517556152346, 'right_e0': 2.8574227093688966, 'right_e1': 0.900446721459961}

        pos_a_right = {'right_s0': 0.03719903406372071, 'right_s1': -0.7248059214477539, 'right_w0': -0.2067039109313965, 'right_w1': 0.18983012228393556, 'right_w2': -0.1457281746826172, 'right_e0': 2.7358547320678714, 'right_e1': 1.200723460345459}

        self.arm.set_joint_position_speed(0.8)

        move_list_smooth(neutral=False, arm='right', p_list=[pos_y_right, pos_m_right, pos_c_right], threshold=0.2, speed=0.8)

        time.sleep(0.8)

        move_list_smooth(neutral=False, arm='right', p_list=[pos_a_right], threshold=0.1)

        time.sleep(1.0)

        self.arm.move_to_neutral(15.0)


print("Doing the YMCA...")
main()
print("Program executed.")
