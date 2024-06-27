from pepper.pepper_tools.cmd_server.pepper_cmd import PepperRobot
import almath


# Postures for the Rock Paper Scissors game - In Degrees (except for the hands, which are 0-1)


# ADULT POSTURES
# Paper posture
PAPER_DICT = {
                'HeadYaw': 0.0, 'HeadPitch': almath.TO_DEG*(-0.21), 
                'LShoulderPitch': 112.8, 'LShoulderRoll': 4.8, 'LElbowYaw': -85.9, 'LElbowRoll': -14.6, 'LWristYaw': 2.0, 
                'RShoulderPitch': 17.0, 'RShoulderRoll': -1.7, 'RElbowYaw': 90.9, 'RElbowRoll': 77.8, 'RWristYaw': -94.7,
                'LHand': 1.0, 'RHand': 1.0,
}    

# Scissors posture
SCISSORS_DICT = {
                'HeadYaw': 0.0, 'HeadPitch': almath.TO_DEG*(-0.21), 
                'LShoulderPitch': -59.2, 'LShoulderRoll': 28.3, 'LElbowYaw': -23.7, 'LElbowRoll': -73.5, 'LWristYaw': 2.0, 
                'RShoulderPitch': -53.9, 'RShoulderRoll': -11.8, 'RElbowYaw': 36.0, 'RElbowRoll': 77.8, 'RWristYaw': -95.3,
                'LHand': 1.0, 'RHand': 1.0
}

# Rock posture
ROCK_DICT = {
                'HeadYaw': 0.0, 'HeadPitch': almath.TO_DEG*(-0.21), 
                'LShoulderPitch': 112.8, 'LShoulderRoll': 4.8, 'LElbowYaw': -85.9, 'LElbowRoll': -14.6, 'LWristYaw': 2.0, 
                'RShoulderPitch': 26.6, 'RShoulderRoll': -1.7, 'RElbowYaw': 90.9, 'RElbowRoll': 36.6, 'RWristYaw': -94.7,
                'LHand': 1.0, 'RHand': 0.0
}

# Kid postures - Bend over a little with the head and hip
KID_NORMAL_DICT = {
                'LShoulderPitch': almath.TO_DEG*(1.55), 'LShoulderRoll': almath.TO_DEG*(0.13), 'LElbowYaw': almath.TO_DEG*(-1.24), 'LElbowRoll': almath.TO_DEG*(-0.52), 'LWristYaw': almath.TO_DEG*(0.01),
                'RShoulderPitch': almath.TO_DEG*(1.56), 'RShoulderRoll': almath.TO_DEG*(-0.14), 'RElbowYaw': almath.TO_DEG*(1.22), 'RElbowRoll': almath.TO_DEG*(0.52), 'RWristYaw': almath.TO_DEG*(-0.01),
                'LHand': 0.0, 'RHand': 0.0 ,
                'HeadYaw': 0.0, 'HeadPitch': -12.6,
                'HipRoll': 0.0, 'HipPitch': -49.9, 'KneePitch': 19.6,
}

# For Rock Paper Scissors, repeat the same posture but with the KID_NORMAL_DICT values for the head and hip
KID_PAPER_DICT = {
                'HeadYaw': 0.0, 'HeadPitch': -12.6,
                'HipRoll': 0.0, 'HipPitch': -49.9, 'KneePitch': 19.6,
                'LShoulderPitch': 112.8, 'LShoulderRoll': 4.8, 'LElbowYaw': -85.9, 'LElbowRoll': -14.6, 'LWristYaw': 2.0, 
                'RShoulderPitch': 17.0, 'RShoulderRoll': -1.7, 'RElbowYaw': 90.9, 'RElbowRoll': 77.8, 'RWristYaw': -94.7,
                'LHand': 1.0, 'RHand': 1.0 
}

KID_SCISSORS_DICT = {
                'HeadYaw': 0.0, 'HeadPitch': -12.6,
                'HipRoll': 0.0, 'HipPitch': -49.9, 'KneePitch': 19.6,
                'LShoulderPitch': -59.2, 'LShoulderRoll': 28.3, 'LElbowYaw': -23.7, 'LElbowRoll': -73.5, 'LWristYaw': 2.0, 
                'RShoulderPitch': -53.9, 'RShoulderRoll': -11.8, 'RElbowYaw': 36.0, 'RElbowRoll': 77.8, 'RWristYaw': -95.3,
                'LHand': 1.0, 'RHand': 1.0
}

KID_ROCK_DICT = {
                'HeadYaw': 0.0, 'HeadPitch': -12.6,
                'HipRoll': 0.0, 'HipPitch': -49.9, 'KneePitch': 19.6,
                'LShoulderPitch': 112.8, 'LShoulderRoll': 4.8, 'LElbowYaw': -85.9, 'LElbowRoll': -14.6, 'LWristYaw': 2.0, 
                'RShoulderPitch': 26.6, 'RShoulderRoll': -1.7, 'RElbowYaw': 90.9, 'RElbowRoll': 36.6, 'RWristYaw': -94.7,
                'LHand': 1.0, 'RHand': 0.0        
}  

# Convert the dictionary to a list of joint values
def returnJointValueArrayFromDict(dict):
    # Convert all to radians except for LHand and RHand
    joint_list = []
    
    for joint in dict:
        # Check if the joint is a hand
        if joint == 'LHand' or joint == 'RHand':
            joint_list.append(dict[joint])
        else:
            joint_list.append(almath.TO_RAD*dict[joint])
    return joint_list

# Convert the dictionary to a list of joint names
def returnJointNamesArrayFromDict(dict):
    joint_list = []
    for joint in dict:
        joint_list.append(joint)
    return joint_list

# Set the robot to the normal posture
def normalPosture(robot, time = 3.0):
    jointValues = [0.00, -0.21, 1.55, 0.13, -1.24, -0.52, 0.01, 1.56, -0.14, 1.22, 0.52, -0.01,
                    0, 0, 0, 0, 0]
    names = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
               "LHand", "RHand", "HipRoll", "HipPitch", "KneePitch"]
    isAbsolute = True
    robot.motion_service.angleInterpolation(names, jointValues, time, isAbsolute)

# Set the robot to a specific posture
def setPosture(robot, jointValues, time = 3.0):
    isAbsolute = True
    robot.motion_service.angleInterpolation(returnJointNamesArrayFromDict(jointValues), returnJointValueArrayFromDict(jointValues), time, isAbsolute)