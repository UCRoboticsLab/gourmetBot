#!/usr/bin/env python

import argparse
import rospy
import baxter_interface

from baxter_interface import CHECK_VERSION

class HeadShaker(object):

    def __init__(self):
        self._done = False
        self._head = baxter_interface.Head()

        print("Getting robot state... ")
        self._rs = baxter_interface.RobotEnable(CHECK_VERSION)
        self._init_state = self._rs.state().enabled
        print("Enabling robot... ")
        self._rs.enable()
        print("Running. Ctrl-c to quit")

    def clean_shutdown(self):
        print("\nExiting example...")
        if self._done:
            self.set_neutral()
        if not self._init_state and self._rs.state().enabled:
            print("Disabling robot...")
            self._rs.disable()

    def set_neutral(self):
        self._head.set_pan(0.0)

    def headshake(self, i):
        self.set_neutral()
        """
        Performs the shaking
        """
	for x in range(i):
		self._head.set_pan(0.3, speed=15, timeout=3)
		self._head.set_pan(-0.3, speed=15, timeout=3)
	self._head.set_pan(0.0, speed=15, timeout=3)

        

        self._done = True
        rospy.signal_shutdown("Example finished.")

    def handwave(self, limb, joint_name, delta):
        current_position = limb.joint_angle(joint_name)
        joint_command = {joint_name: current_position + delta}
        limb.set_joint_positions(joint_command)
	print("limb:", limb)
	print("joint_name:", joint_name)
	print("delta:", delta)
	print("current_position:", current_position)
	print("joint_command:", joint_command)

    print("beep")
    left = baxter_interface.Limb('left')
    lj = left.joint_names()
    handwave(left, 'right_e0', 0.6185)

def main():
    parser = argparse.ArgumentParser(description = 'Process an integer.')
    parser.add_argument('integer', metavar = 'N', type = int, nargs = 1, 
			help = 'Number of head shakes [1 - 10]', choices = range(1, 11))
    args = parser.parse_args()

    print("Initializing node... ")
    rospy.init_node("rsdk_head_shaker")

    headshaker = HeadShaker()
    rospy.on_shutdown(headshaker.clean_shutdown)
    print("Shaking head...")

    if not args:
	i = 2
    elif (args.integer[0] < 1):
	print("Integer too small, defaulting to 2")
	i = 2
    elif (args.integer[0] > 10):
	print("Integer too large, defaulting to 2")
	i = 2
    else:
	i = args.integer[0]
    #headshaker.headshake(i)
    left = baxter_interface.Limb('left')
    lj = left.joint_names()
    print("Running handwave")
    left.set_joint_positions({'left_s0': 0.9448399179626465})
    print("Done.")

if __name__ == '__main__':
    main()
