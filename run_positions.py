#!/usr/bin/env python

import rospy
import baxter_interface
import time
import math
from baxter_core_msgs.msg import JointCommand
from baxter_interface import CHECK_VERSION

import sys

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)

default_speed = 0.3
default_timeout = 15.0
default_threshold = 0.008726646

def dictToList(limb, dict):
    pos_new = [float] * 7
    joints = limb.joint_names()
    current = limb.joint_angles()

    for k in dict.keys():
        current[k] = dict[k]

    pos_new[0] = current[joints[4]]
    pos_new[1] = current[joints[5]]
    pos_new[2] = current[joints[6]]
    pos_new[3] = current[joints[2]]
    pos_new[4] = current[joints[3]]
    pos_new[5] = current[joints[0]]
    pos_new[6] = current[joints[1]]

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
    joints = limb.joint_names()
    current = [float] * 7
    current[0] = limb.joint_angles()[joints[4]]
    current[1] = limb.joint_angles()[joints[5]]
    current[2] = limb.joint_angles()[joints[6]]
    current[3] = limb.joint_angles()[joints[2]]
    current[4] = limb.joint_angles()[joints[3]]
    current[5] = limb.joint_angles()[joints[0]]
    current[6] = limb.joint_angles()[joints[1]]

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
        limb.set_joint_position_speed(speed)

        if neutral:
            limb.move_to_neutral()

        for positions in p_list:
            position = dictToList(limb, positions)

            pub_joints = rospy.Publisher('/robot/limb/' + arm + '/joint_command', JointCommand, queue_size=5)

            cmd_msg = JointCommand()
            cmd_msg.mode = JointCommand.POSITION_MODE
            cmd_msg.names = [arm + '_w0', arm + '_w1', arm + '_w2', arm + '_e0', arm + '_e1', arm + '_s0', arm + '_s1']
            cmd_msg.names = [arm + '_w0', arm + '_w1', arm + '_w2', arm + '_e0', arm + '_e1', arm + '_s0', arm + '_s1']

            bo_finish = False

            while not bo_finish and not rospy.is_shutdown():
                cmd_msg.command = position
                pub_joints.publish(cmd_msg)
                time.sleep(0.19)
                bo_finish = not checkThreshold(limb, position, threshold)

        if neutral:
            limb.move_to_neutral()

        limb.set_joint_position_speed(default_speed)

    else:
        print("Error: {} is not a valid limb".format(arm))


def move_list_smooth_wobble(neutral=False, arm=None, p_list=0, timeout=default_timeout, threshold=default_threshold,
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
            position = dictToList(limb, positions)

            pub_joints = rospy.Publisher('/robot/limb/' + arm + '/joint_command', JointCommand, queue_size=5)

            cmd_msg = JointCommand()
            cmd_msg.mode = JointCommand.POSITION_MODE
            cmd_msg.names = [arm + '_w0', arm + '_w1', arm + '_w2', arm + '_e0', arm + '_e1', arm + '_s0', arm + '_s1']
            cmd_msg.names = [arm + '_w0', arm + '_w1', arm + '_w2', arm + '_e0', arm + '_e1', arm + '_s0', arm + '_s1']

            bo_finish = False

            while not bo_finish and not rospy.is_shutdown():
                cmd_msg.command = position
                pub_joints.publish(cmd_msg)
                time.sleep(0.19)
                bo_finish = not checkThreshold(limb, position, threshold)

        if neutral:
            limb.move_to_neutral()

        limb.set_joint_position_speed(default_speed)

    else:
        print("Error: {} is not a valid limb".format(arm))



def cartesian_move_abs(limb, x=None, y=None, z=None, smooth=True):
    def set_x(value):
        poses.pose.position.y = 1 - value

    def set_y(value):
        poses.pose.position.z = value

    def set_z(value):
        poses.pose.position.x = value

    def get_x():
        return 1 - poses.pose.position.y

    def get_y():
        return poses.pose.position.z

    def get_z():
        return poses.pose.position.x

    #rospy.init_node("rsdk_ik_service_client")
    ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
    iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
    ikreq = SolvePositionIKRequest()
    hdr = Header(stamp=rospy.Time.now(), frame_id='base')
    limb_interface = baxter_interface.Limb('right')
    current_pose = limb_interface.endpoint_pose()

    poses = PoseStamped()
    poses.pose.position.x = current_pose['position'].x
    poses.pose.position.y = current_pose['position'].y
    poses.pose.position.z = current_pose['position'].z
    poses.pose.orientation.x = current_pose['orientation'].x
    poses.pose.orientation.y = current_pose['orientation'].y
    poses.pose.orientation.z = current_pose['orientation'].z
    poses.pose.orientation.w = current_pose['orientation'].w
    poses.header = hdr

    ikreq.pose_stamp.append(poses)
    if x == None:
        x = get_x()

    if y == None:
        y = get_y()

    if z == None:
        z = get_z()
    set_x(x)
    set_y(y)
    set_z(z)

    try:
        rospy.wait_for_service(ns, 5.0)
        resp = iksvc(ikreq)
    except Exception as e:
        rospy.logerr("Service call failed: %s" % (e,))
        return 1
    if (resp.isValid[0]):
        print("SUCCESS - Valid Joint Solution Found:")
        # Format solution into Limb API-compatible dictionary
        limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
        if smooth:
            move_list_smooth(arm=limb, p_list=[limb_joints])
        else:
            move_list(arm=limb, p_list=[limb_joints])

    else:
        print("INVALID POSE - No Valid Joint Solution Found.")

    return 0

def cartesian_move_rel(limb, x=0.0, y=0.0, z=0.0, threshold=default_threshold, smooth=True):
    def set_x(value):
        poses.pose.position.y = 1 - value

    def set_y(value):
        poses.pose.position.z = value

    def set_z(value):
        poses.pose.position.x = value

    def get_x():
        return 1 - poses.pose.position.y

    def get_y():
        return poses.pose.position.z

    def get_z():
        return poses.pose.position.x

    try:
        #rospy.init_node("rsdk_ik_service_client")
        ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
        iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
        ikreq = SolvePositionIKRequest()
        hdr = Header(stamp=rospy.Time.now(), frame_id='base')
        limb_interface = baxter_interface.Limb(limb)
        current_pose = limb_interface.endpoint_pose()

        poses = PoseStamped()
        poses.pose.position.x = current_pose['position'].x
        poses.pose.position.y = current_pose['position'].y
        poses.pose.position.z = current_pose['position'].z
        poses.pose.orientation.x = current_pose['orientation'].x
        poses.pose.orientation.y = current_pose['orientation'].y
        poses.pose.orientation.z = current_pose['orientation'].z
        poses.pose.orientation.w = current_pose['orientation'].w
        poses.header = hdr

        ikreq.pose_stamp.append(poses)
        set_x(get_x() + x)
        set_y(get_y() + y)
        set_z(get_z() + z)

        try:
            rospy.wait_for_service(ns, 5.0)
            resp = iksvc(ikreq)
        except Exception as e:
            rospy.logerr("Service call failed: %s" % (e,))
            return 1
        if (resp.isValid[0]):
            print("SUCCESS - Valid Joint Solution Found:")
            # Format solution into Limb API-compatible dictionary
            limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
            if smooth:
                move_list_smooth(arm=limb, p_list=[limb_joints], threshold=threshold)
            else:
                move_list(arm=limb, p_list=[limb_joints], threshold=threshold)

        else:
            print("INVALID POSE - No Valid Joint Solution Found.")

        return 0

    except KeyError:
        return 1