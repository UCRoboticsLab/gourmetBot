#!/usr/bin/python2

import argparse
import sys

import rospy

import baxter_interface


def off_lights(navs):
    for nav in navs:
        nav.inner_led = False
        nav.outer_led = False


def main():
    rospy.init_node('light_show')

    navs = (
        baxter_interface.Navigator('left'),
        baxter_interface.Navigator('right'),
        baxter_interface.Navigator('torso_left'),
        baxter_interface.Navigator('torso_right'),)
    rate = rospy.Rate(10)
    i = 0

    for nav in navs:
        nav.inner_led = True
        nav.outer_led = False

    while not rospy.is_shutdown() and i < 10:
        for nav in navs:
            nav.inner_led = not nav.inner_led
            nav.outer_led = not nav.outer_led
        rate.sleep()
        i += 1

    off_lights(navs)


print("Running light show...")
main()
print("Program executed.")
