import roslib; roslib.load_manifest('pr2_precise_trajectory')
import rospy
from actionlib import SimpleActionClient, SimpleGoalState
from pr2_controllers_msgs.msg import *

class PointHeadController:
    def __init__(self):
        self.client = SimpleActionClient('/head_traj_controller/point_head_action', PointHeadAction)

        #wait for the action servers to come up 
        rospy.loginfo("[HEAD] Waiting for pointer controller")
        self.client.wait_for_server()
        rospy.loginfo("[HEAD] Got pointer controller")

