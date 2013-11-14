import roslib; roslib.load_manifest('pr2_precise_trajectory')
import rospy
from trajectory_msgs.msg import JointTrajectory,JointTrajectoryPoint
from pr2_controllers_msgs.msg import *
from actionlib import SimpleActionClient, SimpleGoalState, SimpleActionServer
from pr2_precise_trajectory.msg import HeadSequenceAction

import trajectory_msgs.msg

HEAD_JOINTS = ['head_pan_joint', 'head_tilt_joint']
ACTION_NAME = '/head_controller/head_sequence'

class HeadController:
    def __init__(self):
        self.angle_client = SimpleActionClient('/head_traj_controller/joint_trajectory_action', JointTrajectoryAction)
        self.point_client = SimpleActionClient('/head_traj_controller/point_head_action', PointHeadAction)
        #wait for the action servers to come up 
        rospy.loginfo("[HEAD] Waiting for controller")
        self.angle_client.wait_for_server()
        self.point_client.wait_for_server()
        rospy.loginfo("[HEAD] Got controller")

        self.server = SimpleActionServer(ACTION_NAME, HeadSequenceAction, self.execute, False) 
        self.server.start()

        self.client = SimpleActionClient(ACTION_NAME, HeadSequenceAction)
        self.client.wait_for_server()

    def start_trajectory(self, trajectory, set_time_stamp=True, wait=True):
        """Creates an action from the trajectory and sends it to the server"""
        goal = JointTrajectoryGoal()
        goal.trajectory = trajectory
        if set_time_stamp:
            goal.trajectory.header.stamp = rospy.Time.now()
        self.angle_client.send_goal(goal)

        if wait:
            self.wait()

    def execute(self, goal):
        r = rospy.Rate(100)

        # wait to start
        while rospy.Time.now() < goal.header.stamp:
            r.sleep()

        start_time = goal.header.stamp
        for mode, pan, tilt, frame, time in zip(goal.mode, goal.pans, goal.tilts, goal.frames, goal.times):
            if mode == 0:
                jgoal = JointTrajectoryGoal()
                jgoal.trajectory.header.stamp = start_time
                jgoal.trajectory.joint_names = HEAD_JOINTS
                pt = JointTrajectoryPoint()
                pt.positions = [pan, tilt]
                pt.time_from_start = rospy.Duration(time)
                jgoal.trajectory.points.append(pt)
                self.angle_client.send_goal(jgoal)
                self.angle_client.wait_for_result()
            else:
                pgoal = PointHeadGoal()
                pgoal.pointing_frame = '/head_tilt_link'
                pgoal.target.header.frame_id = frame
                pgoal.target.header.stamp = start_time
                pgoal.min_duration = rospy.Duration(time) #self.rate.sleep_dur * dist * self.SPEED_SCALE
                self.point_client.send_goal(pgoal)
                self.point_client.wait_for_result()
            
            start_time += rospy.Duration(time)
        self.server.set_succeeded()

    def wait(self):
        self.angle_client.wait_for_result()

    def is_done(self):
        return self.angle_client.get_state() > SimpleGoalState.ACTIVE

