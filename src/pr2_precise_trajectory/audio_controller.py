#!/usr/bin/python
import roslib; roslib.load_manifest('precise_sound')
import rospy
import actionlib
from pr2_precise_trajectory import *
from precise_sound import Sound
from precise_sound.msg import *

class AudioController:
    def __init__(self):
        self.client = actionlib.SimpleActionClient('/precise_sound/play', PlaySoundsAction)
        self.client.wait_for_server()

    def send_goal(self, sub):
        goal = PlaySoundsGoal()
        goal.header.stamp = rospy.Time.now()
        for a in sub:
            goal.filenames.append(a[AUDIO])
            goal.times.append(a[TIME])
        print goal

        self.client.send_goal(goal)


