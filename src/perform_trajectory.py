#!/usr/bin/env python
import roslib; roslib.load_manifest('pr2_precise_trajectory')
import rospy
from pr2_precise_trajectory.converter import load_trajectory
from pr2_precise_trajectory.full_controller import FullPr2Controller
import sys
import yaml

if __name__ == '__main__':
    rospy.init_node('perform_trajectory')

    movements = load_trajectory(sys.argv[1])
    if len(sys.argv)>2:
        for arg in sys.argv[2:]:
            arg = sys.argv[2]
            if arg[0]=='-':
                continue

            for i, m in enumerate(movements):
                if 'label' not in m:
                    continue
                label = m['label']
                if label==arg:
                    movements = movements[i:]
                    break
    mux = '-m' in sys.argv
        
    controller = FullPr2Controller(mux_it = mux)
    controller.do_action(movements)

    print "Completely done"
    rospy.spin()

