#!/usr/bin/env python
import argparse
import sys
from run_positions import move_list_smooth
import rospy
import baxter_interface
from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header
from sensor_msgs.msg import Range


from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)


def ik_move(limb, x=None, y=None, z=None):

    def set_x(value):
        poses[limb].pose.position.y = 1 - value

    def set_y(value):
        poses[limb].pose.position.z = value

    def set_z(value):
        poses[limb].pose.position.x = value

    def get_x():
        return 1 - poses[limb].pose.position.y

    def get_y():
        return poses[limb].pose.position.z

    def get_z():
        return poses[limb].pose.position.x

    rospy.init_node("rsdk_ik_service_client")
    ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
    iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
    ikreq = SolvePositionIKRequest()
    hdr = Header(stamp=rospy.Time.now(), frame_id='base')
    limb_interface = baxter_interface.Limb(limb)
    current_pose = limb_interface.endpoint_pose()
    poses = {
        'left': PoseStamped(
            header=hdr,
            pose=Pose(
                position=Point(
                    x=current_pose['position'].x,
                    y=current_pose['position'].y,
                    z=current_pose['position'].z
                ),
                orientation=Quaternion(
                    x=-0.866894936773,
                    y=0.885980397775,
                    z=0.008155782462,
                    w=0.262162481772,
                ),
            ),
        ),
        'right': PoseStamped(
            header=hdr,
            pose=Pose(
                position=Point(
                    x=0.656982770038,
                    y=-0.852598021641,
                    z=0.0388609422173,
                ),
                orientation=Quaternion(
                    x=0.367048116303,
                    y=0.885911751787,
                    z=-0.108908281936,
                    w=0.261868353356,
                ),
            ),
        ),
    }
    ikreq.pose_stamp.append(poses[limb])
    if x == None:
        x = get_x()

    if y == None:
        y = get_y()

    if z == None:
        z = get_z()
    set_x(x)
    set_y(y)
    set_z(z)

    try:
        rospy.wait_for_service(ns, 5.0)
        resp = iksvc(ikreq)
    except Exception as e:
        rospy.logerr("Service call failed: %s" % (e,))
        return 1
    if (resp.isValid[0]):
        print("SUCCESS - Valid Joint Solution Found:")
        # Format solution into Limb API-compatible dictionary
        limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
        print(limb_joints)
        move_list_smooth(arm='left', p_list=[limb_joints])

    else:
        print("INVALID POSE - No Valid Joint Solution Found.")

    return 0
def main():
    '''
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__)
    parser.add_argument(
        '-l', '--limb', choices=['left', 'right'], required=True,
        help="the limb to test"
    )
    args = parser.parse_args(rospy.myargv()[1:])
    return ik_test(args.limb)
    '''

    ik_move('left', y=0.5)

if __name__ == '__main__':
    sys.exit(main())