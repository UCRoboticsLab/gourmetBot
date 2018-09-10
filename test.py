#!/usr/bin/env python

import time
import json

import rospy

# http://api.rethinkrobotics.com/baxter_interface/html/index.html
import baxter_interface

from baxter_core_msgs.msg import EndpointState

from std_msgs.msg import String

# https://github.com/ricardodeazambuja/BaxterRobotUtils/blob/master/ik_client.py
from ik_client import ik_service

# http://sdk.rethinkrobotics.com/wiki/IK_Service_Example

limb = 'right'

gripper_force_threshold = 30  # in percentage
gripper_vacuum_threshold = 18  # in percentage

# Receives a list of poses / gripper commands
ik = ik_service(limb, speed=0.3)

gripper = baxter_interface.Gripper(limb)

print
"Using the " + gripper.type() + " gripper."

if gripper.type() == 'electric':
    print
    "Calibrating the electric gripper"
    gripper.calibrate()
    gripper.set_holding_force(gripper_force_threshold)
else:
    gripper.set_vacuum_threshold(gripper_vacuum_threshold)

print
"Gripper parameters: ", gripper.parameters()

# Callback function for the coord_sub subscriber
coord_data = [None]


def coord_sub_cb(data):
    coord_data[0] = json.loads(data.data)


# Subscribes to the topic where we can find the coordinates
coord_sub = rospy.Subscriber('/coordinates_from_opencv_' + limb, String, coord_sub_cb)

# Test our subscriber
coord_data

# Callback function for the endpoint_state_sub subscriber
endpoint_state_data = [None]


def endpoint_state_sub_cb(data):
    endpoint_state_data[0] = data

endpoint_state_topic = '/robot/limb/' + limb + '/endpoint_state'
endpoint_state_sub = rospy.Subscriber(endpoint_state_topic, EndpointState, endpoint_state_sub_cb, queue_size=1)

# Test our subscriber
endpoint_state_data[0].pose

rate = rospy.Rate(10)

while True:
    if coord_data[0] != None and endpoint_state_data[0] != None:
        # Keep the same original pose
        quat = [endpoint_state_data[0].pose.orientation.x,
                endpoint_state_data[0].pose.orientation.y,
                endpoint_state_data[0].pose.orientation.z,
                endpoint_state_data[0].pose.orientation.w]

        pos = [endpoint_state_data[0].pose.position.x,
               endpoint_state_data[0].pose.position.y,
               endpoint_state_data[0].pose.position.z]
        #
        # Now you need to do the magic to keep the gripper aligned...
        #

        if not ik.ik_call(pos, quat):
            ik.ik_move_to(timeout=15)
            if g_i:
                gripper.close()
            else:
                gripper.open()
        else:
            print
            "IK returned an error..."

    # Makes sure the while loop will not go crazy eating all your cpu resources...
    rate.sleep()

