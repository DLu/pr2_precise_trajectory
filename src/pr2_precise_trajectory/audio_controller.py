#!/usr/bin/python
import roslib; roslib.load_manifest('precise_sound')
import rospy
import actionlib
from precise_sound import Sound
from precise_sound.msg import *

class AudioController:
    def __init__(self):
        self.client = actionlib.SimpleActionClient('/precise_sound/play', PlaySoundAction)
        self.client.wait_for_server()

    def send_goal(self, sub):
        goal = PlaySoundGoal()
        goal.header.stamp = rospy.Time.now()
        for a in sub:
            goal.filenames.append(move[AUDIO])
            goal.times.append(sub[TIME])

        self.client.send_goal(goal)


