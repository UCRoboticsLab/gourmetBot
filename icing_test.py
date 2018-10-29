#!/usr/bin/env python

import rospy
import baxter_interface
import time
from run_positions import move_list
from run_positions import cartesian_move_rel

from baxter_interface import CHECK_VERSION

rospy.init_node("whisk")
left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
grip_right = baxter_interface.Gripper('right', CHECK_VERSION)

def lower_and_pump():
    cartesian_move_rel(limb="left", y=-0.04)
    cartesian_move_rel(limb="left", y=-0.03, threshold=0.005)
    cartesian_move_rel(limb="left", y=-0.02, threshold=0.005)
    cartesian_move_rel(limb="left", y=-0.01, threshold=0.005)
    grip_left.open(block=True, timeout=15.0)
    time.sleep(4.0)
    grip_left.close(block=True, timeout=15.0)
    time.sleep(1.0)
    cartesian_move_rel(limb="left", y=0.03)
    time.sleep(1.0)
    cartesian_move_rel(limb="left", y=0.05)

grip_left.set_moving_force(90)
grip_left.set_velocity(90)

lower_and_pump()
time.sleep(1.0)
cartesian_move_rel(limb="left", x=0.1)

lower_and_pump()
time.sleep(1.0)
cartesian_move_rel(limb="left", z=-0.1)

lower_and_pump()
time.sleep(1.0)
cartesian_move_rel(limb="left", x=-0.1)

lower_and_pump()
time.sleep(1.0)
cartesian_move_rel(limb="left", z=0.1)
