from pepper.pepper_tools.cmd_server.pepper_cmd import PepperRobot
import almath


JOINT_NAMES = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
               "LHand", "RHand"]

# Postures for the Rock Paper Scissors game - In Degrees (except for the hands)
PAPER_DICT = {
                'HeadYaw': 0.0, 'HeadPitch': almath.TO_DEG*(-0.21), 
                'LShoulderPitch': 112.8, 'LShoulderRoll': 4.8, 'LElbowYaw': -85.9, 'LElbowRoll': -14.6, 'LWristYaw': 2.0, 
                'RShoulderPitch': 17.0, 'RShoulderRoll': -1.7, 'RElbowYaw': 90.9, 'RElbowRoll': 77.8, 'RWristYaw': -94.7,
                'LHand': 1.0, 'RHand': 1.0
              }    

SCISSORS_DICT = {
                'HeadYaw': 0.0, 'HeadPitch': almath.TO_DEG*(-0.21), 
                'LShoulderPitch': -59.2, 'LShoulderRoll': 28.3, 'LElbowYaw': -23.7, 'LElbowRoll': -73.5, 'LWristYaw': 2.0, 
                'RShoulderPitch': -53.9, 'RShoulderRoll': -11.8, 'RElbowYaw': 36.0, 'RElbowRoll': 77.8, 'RWristYaw': -95.3,
                'LHand': 1.0, 'RHand': 1.0
              }

ROCK_DICT = {
                'HeadYaw': 0.0, 'HeadPitch': almath.TO_DEG*(-0.21), 
                'LShoulderPitch': 112.8, 'LShoulderRoll': 4.8, 'LElbowYaw': -85.9, 'LElbowRoll': -14.6, 'LWristYaw': 2.0, 
                'RShoulderPitch': 26.6, 'RShoulderRoll': -1.7, 'RElbowYaw': 90.9, 'RElbowRoll': 36.6, 'RWristYaw': -94.7,
                'LHand': 1.0, 'RHand': 0.0
              }

def returnJointValueArrayFromDict(dict):
    # Convert all to radians except for LHand and RHand
    joint_list = []
    
    for joint in JOINT_NAMES:
        # Check if the joint is a hand
        if joint == 'LHand' or joint == 'RHand':
            joint_list.append(dict[joint])
        else:
            joint_list.append(almath.TO_RAD*dict[joint])
    return joint_list




def normalPosture(robot, time = 3.0):
    jointValues = [0.00, -0.21, 1.55, 0.13, -1.24, -0.52, 0.01, 1.56, -0.14, 1.22, 0.52, -0.01,
                    0, 0, 0, 0, 0]
    names = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
               "LHand", "RHand", "HipRoll", "HipPitch", "KneePitch"]
    isAbsolute = True
    robot.motion_service.angleInterpolation(names, jointValues, time, isAbsolute)


def setPosture(robot, jointValues, time = 3.0):
    isAbsolute = True
    robot.motion_service.angleInterpolation(JOINT_NAMES, returnJointValueArrayFromDict(jointValues), time, isAbsolute)