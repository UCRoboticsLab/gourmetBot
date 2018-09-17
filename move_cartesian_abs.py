#!/usr/bin/env python

import argparse
import rospy
import time
import threading
import baxter_interface
from run_positions import cartesian_move_abs

from baxter_interface import CHECK_VERSION

rospy.init_node("move_cartesian_absolute")

def main():
	arg_fmt = argparse.RawDescriptionHelpFormatter
	parser = argparse.ArgumentParser(formatter_class=arg_fmt,
									 description=main.__doc__)
	parser.add_argument(
		'-l', '--limb', choices=['left', 'right'], required=True,
		help="the limb to move"
	)
	parser.add_argument(
		'-x', type=float, required=False,
		help="movement on the x-plane"
	)
	parser.add_argument(
		'-y', type=float, required=False,
		help="movement on the y-plane"
	)
	parser.add_argument(
		'-z', type=float, required=False,
		help="movement on the z-plane"
	)
	args = vars(parser.parse_args())
	cartesian_move_abs(args['limb'], args['x'], args['y'], args['z'])


main()
