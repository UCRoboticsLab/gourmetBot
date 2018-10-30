#!/usr/bin/env python

import struct
import sys
import time
import rospy
import baxter_interface

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

def get_cartesian_positions(limb):
    retry = True

    while retry:
        try:
            pose_names = ['position x:',
                          'position y:',
                          'position z:',
                          'orientation x:',
                          'orientation y:',
                          'orientation z:',
                          'orientation w:']

            ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
            hdr = Header(stamp=rospy.Time.now(), frame_id='base')
            limb_interface = baxter_interface.Limb(limb)
            current_pose = limb_interface.endpoint_pose()

            ik_pose = PoseStamped()
            ik_pose.pose.position.x = current_pose['position'].x
            ik_pose.pose.position.y = current_pose['position'].y
            ik_pose.pose.position.z = current_pose['position'].z
            ik_pose.pose.orientation.x = current_pose['orientation'].x
            ik_pose.pose.orientation.y = current_pose['orientation'].y
            ik_pose.pose.orientation.z = current_pose['orientation'].z
            ik_pose.pose.orientation.w = current_pose['orientation'].w
            ik_pose.header = hdr

            pose_values = [ik_pose.pose.position.x,
                           ik_pose.pose.position.y,
                           ik_pose.pose.position.z,
                           ik_pose.pose.orientation.x,
                           ik_pose.pose.orientation.y,
                           ik_pose.pose.orientation.z,
                           ik_pose.pose.orientation.w]

            retry = False
            positions = {}
            for i in range(len(pose_names)):
                positions.update({pose_names[i]:pose_values[i]})
            return positions

        except KeyError:
            retry = True


def ik_test(limb):

    retry = True

    while retry:
        try:
            pose_names = ['position x:',
                          'position y:',
                          'position z:',
                          'orientation x:',
                          'orientation y:',
                          'orientation z:',
                          'orientation w:']

            rospy.init_node("rsdk_ik_service_client")
            ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
            hdr = Header(stamp=rospy.Time.now(), frame_id='base')
            limb_interface = baxter_interface.Limb(limb)
            current_pose = limb_interface.endpoint_pose()

            ik_pose = PoseStamped()
            ik_pose.pose.position.x = current_pose['position'].x
            ik_pose.pose.position.y = current_pose['position'].y
            ik_pose.pose.position.z = current_pose['position'].z
            ik_pose.pose.orientation.x = current_pose['orientation'].x
            ik_pose.pose.orientation.y = current_pose['orientation'].y
            ik_pose.pose.orientation.z = current_pose['orientation'].z
            ik_pose.pose.orientation.w = current_pose['orientation'].w
            ik_pose.header = hdr

            pose_values = [ik_pose.pose.position.x,
                           ik_pose.pose.position.y,
                           ik_pose.pose.position.z,
                           ik_pose.pose.orientation.x,
                           ik_pose.pose.orientation.y,
                           ik_pose.pose.orientation.z,
                           ik_pose.pose.orientation.w]

            print('\n' + limb + '\n')
            for i in range(len(pose_names)):
                if i == 3:
                    print
                print("{} {:.3f}".format(pose_names[i], pose_values[i]))
            print
            retry = False
        except KeyError:
            retry = True


def main():
    ik_test('left')
    ik_test('right')


if __name__ == '__main__':
    sys.exit(main())