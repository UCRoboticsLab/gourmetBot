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

    time.sleep(2.1)
    grip_left.open()
    #height_sensor = HeightSensor()
    #rospy.spin()


def move_arm():
    pos_up = {'left_w0': 3.044951860473633, 'left_w1': -1.176179767767334, 'left_w2': -0.09932525590209962, 'left_e0': 3.05415574519043, 'left_e1': 1.5941895319885255, 'left_s0': 0.7811797153381348, 'left_s1': 0.39960199478759767}
    pos_down = {'left_w0': 3.0123547687683105, 'left_w1': -0.7198204838928223, 'left_w2': 0.0, 'left_e0': 3.0533887547973633, 'left_e1': 0.28838838779296877, 'left_s0': 0.5756262899963379, 'left_s1': 0.9200049764831544}



    move_list(arm='left', p_list=[pos_up], speed=0.1, threshold=0.1)
    move_list(arm='left', p_list=[pos_down], timeout=1.0, speed=0.1)


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
        if left_distance < 0.2:
            if i < 3:
                print(left_distance)
                #time.sleep(0.2)
                print("Grabbing")
                print("i:", i)
                grip_left.close()
                time.sleep(0.5)
                grip_left.open()
                time.sleep(0.5)
                i+=1
            else:
                rospy.signal_shutdown("reasons")


print("Running grab_left...")
rospy.init_node("grab_left")
left = baxter_interface.Limb('left')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
#if not grip_left.calibrated():
grip_left.calibrate()
grip_left.close()
time.sleep(0.5)
grip_left.set_velocity(100.0)
grip_left.set_moving_force(100.0)
grip_left.set_holding_force(90.0)
#grip_left.open(block=True)
time.sleep(0.5)
thread_height_sensor = threading.Thread(name='height_sensor', target=def_height_sensor)
thread_move_arm = threading.Thread(name='move_arm', target=move_arm)
thread_height_sensor.start()
thread_move_arm.start()
