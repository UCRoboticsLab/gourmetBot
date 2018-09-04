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
i = 0

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
        global left_distance, i
        left_distance = msg.range
        if left_distance < 0.1:
            while i < 1:
                print(left_distance)
                #time.sleep(0.2)
                print("Grabbing")
                print("i:", i)
                grip_left.close()
                time.sleep(0.5)
                grip_left.stop()
                #grip_left.open()
                i+=1
            rospy.signal_shutdown("reasons")


print("Running grab_left...")
rospy.init_node("grab_left")
left = baxter_interface.Limb('left')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
#if not grip_left.calibrated():
grip_left.calibrate()
grip_left.set_velocity(100.0)
grip_left.set_moving_force(90.0)
grip_left.set_holding_force(50.0)
grip_left.open(block=True)
time.sleep(0.5)
thread_height_sensor = threading.Thread(name='height_sensor', target=def_height_sensor)
thread_height_sensor.start()

