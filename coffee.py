#!/usr/bin/env python

import rospy
import baxter_interface
import time
from run_positions import move_list

from baxter_interface import CHECK_VERSION

print("Test")

rospy.init_node("coffee")
left = baxter_interface.Limb('left')
right = baxter_interface.Limb('right')
grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
grip_right = baxter_interface.Gripper('right', CHECK_VERSION)


pos_above_glass = {'left_w0': 0.08973787598876953, 'left_w1': -0.8521263266967773, 'left_w2': -0.12655341485595703, 'left_e0': -0.0487038899597168, 'left_e1': -0.050237870745849615, 'left_s0': -0.8095583598815919, 'left_s1': 0.6036214393432617}

pos_around_glass = {'left_w0': 0.09510680874023437, 'left_w1': -0.5242379336608887, 'left_w2': -0.02032524541625977, 'left_e0': -0.08858739039916992, 'left_e1': -0.04947088035278321, 'left_s0': -0.8210632157775879, 'left_s1': 0.5978690113952637}

pos_under_spout = {'left_w0': -0.13115535721435548, 'left_w1': -0.46019423583984376, 'left_w2': 0.13153885241088867, 'left_e0': -0.07554855371704101, 'left_e1': -0.04985437554931641, 'left_s0': -0.5641214341003419, 'left_s1': 0.5767767755859375}

pos_above_spout = {'left_w0': -0.2063204157348633, 'left_w1': -1.0112768332580566, 'left_w2': 0.26116022883911133, 'left_e0': -0.11236409258422853, 'left_e1': -0.04947088035278321, 'left_s0': -0.6204952279907227, 'left_s1': 0.5721748332275391}

pos_above_spout_align = {'left_w0': -0.2665291615905762, 'left_w1': -1.1155875267150879, 'left_w2': 1.647878859503174, 'left_e0': -0.09855826550903321, 'left_e1': -0.04908738515625, 'left_s0': -0.6304661031005859, 'left_s1': 0.5767767755859375}

pos_press_spout = {'left_w0': -0.2665291615905762, 'left_w1': -0.9155875267150879, 'left_w2': 1.647878859503174, 'left_e0': -0.09855826550903321, 'left_e1': -0.04908738515625, 'left_s0': -0.6304661031005859, 'left_s1': 0.5767767755859375}

pos_above_beans = {'left_w0': 0.04371845240478516, 'left_w1': -0.634301055065918, 'left_w2': 0.005752427947998047, 'left_e0': -0.11274758778076173, 'left_e1': -0.04947088035278321, 'left_s0': -1.0009224629516602, 'left_s1': 0.5583690061523437}

pos_around_beans = {'left_w0': -0.01112136069946289, 'left_w1': -0.3290388786254883, 'left_w2': 0.06941263057250976, 'left_e0': -0.1457281746826172, 'left_e1': -0.04985437554931641, 'left_s0': -1.0016894533447267, 'left_s1': 0.5307573520019532}

pos_pour_beans_align = {'left_w0': -1.9504565695678713, 'left_w1': -0.9038981782287598, 'left_w2': 1.4983157328552248, 'left_e0': -0.13575729957275393, 'left_e1': -0.04640291878051758, 'left_s0': -1.1255584018249511, 'left_s1': 0.22779614674072268}

pos_pour_beans = {'left_w0': -1.8426944193420411, 'left_w1': -0.7374612629333497, 'left_w2': -0.2442864401916504, 'left_e0': -0.16682041049194338, 'left_e1': -0.0487038899597168, 'left_s0': -1.0365875162292482, 'left_s1': 0.28110197905883794}

pos_pour_beans_shake = {'left_s1': 0.23110197905883794}

print("Program started")

right.set_joint_position_speed(0.5)
grip_left.calibrate()
move_list(neutral=False, arm='left', p_list=[pos_above_beans, pos_around_beans])
grip_left.close()
time.sleep(0.5)
move_list(neutral=False, arm='left', p_list=[pos_pour_beans_align], threshold=0.05)
move_list(neutral=False, arm='left', p_list=[pos_pour_beans, pos_pour_beans_shake, pos_pour_beans])
time.sleep(0.5)
move_list(neutral=False, arm='left', p_list=[pos_above_beans, pos_around_beans])
grip_left.open()
time.sleep(0.5)
move_list(neutral=False, arm='left', p_list=[pos_above_beans, pos_above_glass], threshold=0.1)
move_list(neutral=False, arm='left', p_list=[pos_around_glass])
grip_left.close()
time.sleep(0.5)
move_list(neutral=False, arm='left', p_list=[pos_under_spout])
grip_left.open()
time.sleep(0.5)
move_list(neutral=False, arm='left', p_list=[pos_above_spout], threshold=0.1)
move_list(neutral=False, arm='left', p_list=[pos_above_spout_align, pos_press_spout])
print("waiting...")
time.sleep(0.5)
move_list(neutral=False, arm='left', p_list=[pos_above_spout_align, pos_above_spout, pos_under_spout])
grip_left.close()
time.sleep(0.5)
move_list(neutral=False, arm='left', p_list=[pos_around_glass])
grip_left.open()
move_list(neutral=False, arm='left', p_list=[pos_above_glass])


print("Program executed")
