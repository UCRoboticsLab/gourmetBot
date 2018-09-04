#!/usr/bin/env python

import argparse
import rospy
import time
import baxter_interface
import threading
from sensor_msgs.msg import Range
from run_positions import move_list

from baxter_interface import CHECK_VERSION


left_effort = 0.0

pos_up = {'left_w0': -0.01687378864746094, 'left_w1': 1.6225681765319826, 'left_w2': 0.0122718462890625, 'left_e0': 0.07938350568237305, 'left_e1': -0.05138835633544922, 'left_s0': -0.6879903825805664, 'left_s1': -0.24236896420898438}

pos_down = {'left_s1': 0.24672816419677735}

def move_arm():

    print("moving down")
    #move_list(arm='left', p_list=[pos_down], speed=0.1)
    #rospy.signal_shutdown("shutdown")

def def_height_sensor():
    i = 0

    while not rospy.is_shutdown() and i < 10:
        left_effort = left.joint_efforts()['left_s1']
        left_angle = left.joint_angles()['left_s1']
        print ("left_s1 effort:", left_effort)
        print ("left_s1 position:", left_angle)
        time.sleep(0.5)
        i += 1

    rospy.signal_shutdown("reason")


print("Checking height...")
rospy.init_node("height_check")
left = baxter_interface.Limb('left')
left.set_joint_position_speed(0.1)
#move_list(arm='left', p_list=[pos_up])
thread_move_arm = threading.Thread(name='move_arm', target=move_arm)
thread_height_sensor = threading.Thread(name='height_sensor', target=def_height_sensor)
thread_move_arm.start()
thread_height_sensor.start()

