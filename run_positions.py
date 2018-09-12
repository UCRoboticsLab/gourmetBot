#!/usr/bin/env python

import rospy
import baxter_interface
import time
import math
from baxter_core_msgs.msg import JointCommand
from baxter_interface import CHECK_VERSION

default_speed = 0.3
default_timeout = 15.0
default_threshold = 0.008726646


def dictToList(limb, dict):
    pos_new = [float] * 7

    current = limb.joint_angles()

    for k in dict.keys():
        current[k] = dict[k]

    pos_new[0] = current['left_w0']
    pos_new[1] = current['left_w1']
    pos_new[2] = current['left_w2']
    pos_new[3] = current['left_e0']
    pos_new[4] = current['left_e1']
    pos_new[5] = current['left_s0']
    pos_new[6] = current['left_s1']

    return pos_new


def move_list(neutral=False, arm=None, p_list=[], timeout=default_timeout, threshold=default_threshold,
              speed=default_speed):
    arm = arm.lower()

    if speed > 1.0:
        speed = 1.0
    elif speed <= 0.0:
        speed = 0.1

    if arm == 'l':
        arm = 'left'
    elif arm == 'r':
        arm = 'right'

    if arm == 'left' or arm == 'right':

        limb = baxter_interface.Limb(arm)
        limb.set_joint_position_speed(speed)

        if neutral:
            limb.move_to_neutral()

        for positions in p_list:
            limb.move_to_joint_positions(positions=positions, timeout=timeout, threshold=threshold)

        if neutral:
            limb.move_to_neutral()

        limb.set_joint_position_speed(default_speed)

    else:
        print("Error: {} is not a valid limb".format(arm))


def checkThreshold(limb, destination, threshold):
    current = [float] * 7
    current[0] = limb.joint_angles()['left_w0']
    current[1] = limb.joint_angles()['left_w1']
    current[2] = limb.joint_angles()['left_w2']
    current[3] = limb.joint_angles()['left_e0']
    current[4] = limb.joint_angles()['left_e1']
    current[5] = limb.joint_angles()['left_s0']
    current[6] = limb.joint_angles()['left_s1']

    for i in range(len(destination)):
        if math.fabs(current[i] - destination[i]) > threshold:
            return True
    return False


def move_list_smooth(neutral=False, arm=None, p_list=0, timeout=default_timeout, threshold=default_threshold,
                     speed=default_speed):
    arm = arm.lower()

    if speed > 1.0:
        speed = 1.0
    elif speed <= 0.0:
        speed = 0.1

    if arm == 'l':
        arm = 'left'
    elif arm == 'r':
        arm = 'right'

    if arm == 'left' or arm == 'right':

        limb = baxter_interface.Limb(arm)

        if neutral:
            limb.move_to_neutral()

        for positions in p_list:
            position = dictToList(limb, positions)

            pub_joints = rospy.Publisher('/robot/limb/left/joint_command', JointCommand, queue_size=5)

            cmd_msg = JointCommand()
            cmd_msg.mode = JointCommand.POSITION_MODE
            cmd_msg.names = ['left_w0', 'left_w1', 'left_w2', 'left_e0', 'left_e1', 'left_s0', 'left_s1']
            left = baxter_interface.Limb('left')
            left.set_joint_position_speed(speed)

            bo_finish = False

            while not bo_finish and not rospy.is_shutdown():
                cmd_msg.command = position
                pub_joints.publish(cmd_msg)
                time.sleep(0.19)
                bo_finish = not checkThreshold(left, position, threshold)

        if neutral:
            limb.move_to_neutral()

        limb.set_joint_position_speed(default_speed)

    else:
        print("Error: {} is not a valid limb".format(arm))
