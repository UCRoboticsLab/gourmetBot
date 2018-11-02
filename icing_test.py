#!/usr/bin/env python

import rospy
import baxter_interface
import time
from run_positions import move_list
from run_positions import cartesian_move_rel
from run_positions import cartesian_move_abs
from get_cartesian import get_cartesian_positions

from baxter_interface import CHECK_VERSION

rospy.init_node("whisk")
left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
grip_right = baxter_interface.Gripper('right', CHECK_VERSION)
start_Y_pos = 0

start_pos = {'left_w0': 0.23968449783325196, 'left_w1': 0.7754272873901368, 'left_w2': 0.5391942463256836, 'left_e0': -2.1445051390136722, 'left_e1': 0.4594272454467774, 'left_s0': 0.4509903511230469, 'left_s1': 0.5276893904296875}

def shake():
    cartesian_move_rel(limb="left", x=-0.01)
    cartesian_move_rel(limb="left", x=0.02)
    cartesian_move_rel(limb="left", x=-0.01)

def pump_and_up(x_diff=0.0, z_diff=0.0):
    global start_Y_pos

    grip_left.set_moving_force(90)
    grip_left.set_velocity(10)

    cartesian_move_rel(limb="left", y=-0.03, smooth=False)

    grip_left.open(block=True, timeout=15.0)
    time.sleep(8.0)

    cartesian_move_rel(limb="left", y=-0.01, smooth=False)

    grip_left.close(block=True, timeout=15.0)
    time.sleep(1.0)
    cartesian_move_rel(limb="left", y=0.04, smooth=False)

    #shake()
    time.sleep(1.0)
    print(abs(start_Y_pos - get_cartesian_positions('left')['position y:']))
    cartesian_move_rel(limb="left",x=x_diff,y=0.05,z=z_diff, smooth=False)
    time.sleep(1.0)

def lower_hand():

    cartesian_move_rel(limb="left", y=-0.05, threshold=0.005, smooth=False)



move_list(arm='left', p_list=[start_pos])
time.sleep(1.0)

start_Y_pos = get_cartesian_positions('left')['position y:']

pump_and_up(x_diff=0.1)
lower_hand()
#cartesian_move_rel(limb="left", x=0.1)

pump_and_up(z_diff=-0.1)
lower_hand()
#cartesian_move_rel(limb="left", z=-0.1)

pump_and_up(x_diff=-0.1)
lower_hand()
#cartesian_move_rel(limb="left", x=-0.1)

pump_and_up(z_diff=0.1)
#cartesian_move_rel(limb="left", z=0.1)

move_list(arm='left', p_list=[start_pos])