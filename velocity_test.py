#!/usr/bin/env python

import argparse
import rospy
import baxter_interface
import time
#from run_positions import move_list
from baxter_core_msgs.msg import JointCommand

from baxter_interface import CHECK_VERSION

def dictToList(dict):
    pos_new = [float]*7
    pos_new[0] = dict['left_w0']
    pos_new[1] = dict['left_w1']
    pos_new[2] = dict['left_w2']
    pos_new[3] = dict['left_e0']
    pos_new[4] = dict['left_e1']
    pos_new[5] = dict['left_s0']
    pos_new[6] = dict['left_s1']

    return pos_new


rospy.init_node("hand_wave")
left = baxter_interface.Limb('left')

which_pos = True

pos_00 = {'left_w0': -0.17602429520874024, 'left_w1': 0.8264321485290528, 'left_w2': 0.611674838470459, 'left_e0': 0.2320145939025879, 'left_e1': 0.9008302166564942, 'left_s0': -0.09357282795410157, 'left_s1': -0.22511168036499024}
pos_10 = {'left_w0': -0.5921165834472657, 'left_w1': 0.8302671004943848, 'left_w2': 0.6864564017944337, 'left_e0': 0.5372767703430176, 'left_e1': 1.03083508828125, 'left_s0': -0.36201946552734376, 'left_s1': -0.20133497817993165}
pos_20 = {'left_w0': -1.298898230657959, 'left_w1': 1.1255584018249511, 'left_w2': 0.8356360332458497, 'left_e0': 1.0526943144836427, 'left_e1': 1.0404224681945802, 'left_s0': -0.655009795678711, 'left_s1': 0.03911651004638672}
pos_1 = {'left_w0': 1.1662088926574707, 'left_w1': -0.2308641083129883, 'left_w2': -0.09625729432983399, 'left_e0': -1.2026409363281252, 'left_e1': -0.050237870745849615, 'left_s0': 0.3900146148742676, 'left_s1': 0.45559229348144537}
pos_2 = {'left_w0': 1.0956457764953613, 'left_w1': -1.4016749433288576, 'left_w2': -0.15569904979248048, 'left_e0': -1.2390729799987794, 'left_e1': -0.04947088035278321, 'left_s0': 0.390781605267334, 'left_s1': 0.12348545328369141}

pub_joints = rospy.Publisher('/robot/limb/left/joint_command', JointCommand, queue_size=1)
rospy.init_node("hand_wave")
rate = rospy.Rate(100)

cmd_msg = JointCommand()
cmd_msg.mode = JointCommand.POSITION_MODE
cmd_msg.names = ['left_w0', 'left_w1', 'left_w2', 'left_e0', 'left_e1', 'left_s0', 'left_s1']
left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
left.set_joint_position_speed(0.5)
print(left.joint_velocities())
print(right.joint_velocities())
#left.set_joint_velocities({'left_w1' : 50})
while not rospy.is_shutdown():

    if which_pos:
        position = dictToList(pos_1)
    else:
        position = dictToList(pos_2)
    cmd_msg.command = position
    pub_joints.publish(cmd_msg)
    print(cmd_msg)
    rospy.sleep(2)
    which_pos = not which_pos