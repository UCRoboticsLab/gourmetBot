#!/usr/bin/env python

import argparse
import rospy
import time
import baxter_interface
import threading
from sensor_msgs.msg import Range
from run_positions import move_list

from baxter_interface import CHECK_VERSION


left_distance = 0.0

pos_up = {'left_w0': -0.01687378864746094, 'left_w1': 1.6225681765319826, 'left_w2': 0.0122718462890625, 'left_e0': 0.07938350568237305, 'left_e1': -0.05138835633544922, 'left_s0': -0.6879903825805664, 'left_s1': -0.24236896420898438}

pos_down = {'left_s1': 0.24672816419677735}

def move_arm():

    print("moving down")
    move_list(arm='left', p_list=[pos_down], speed=1.0)
    rospy.signal_shutdown("shutdown")

def def_height_sensor():

    height_sensor = HeightSensor()
    rospy.spin()


class HeightSensor():

    def __init__(self):
        self.distance = {}
        root_name = "/robot/range/"
        sensor_name = ["left_hand_range/state"]
        #sensor_name = ["left_hand_range/state","right_hand_range/state"]
        self.__left_sensor  = rospy.Subscriber(root_name + sensor_name[0],Range, callback=self.__sensorCallback, callback_args="left",queue_size=1)
        #self.__right_sensor = rospy.Subscriber(root_name + sensor_name[1],Range, callback=self.__sensorCallback, callback_args="right",queue_size=1)

    def __sensorCallback(self, msg, side):
        global left_distance
        left_distance = msg.range
        if left_distance < 0.15:
            print("Distance to table: {:.2f} cm".format(left_distance * 100))
            rospy.signal_shutdown("shutdown")


print("Checking height...")
rospy.init_node("height_check")
left = baxter_interface.Limb('left')
left.set_joint_position_speed(0.1)
move_list(arm='left', p_list=[pos_up])
thread_move_arm = threading.Thread(name='move_arm', target=move_arm)
thread_height_sensor = threading.Thread(name='height_sensor', target=def_height_sensor)
thread_move_arm.start()
thread_height_sensor.start()

