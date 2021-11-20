import os
import cv2
import numpy as np
import time
import cv2.aruco as aruco
import cv2
import matplotlib.pyplot as plt
np.seterr(divide='ignore', invalid='ignore')


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


def lower_resolution(img, size=20):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.resize(
        result, (size, size), interpolation=cv2.INTER_CUBIC)

    return result


def center_robot(mat):

    pass


def possible_directions(mat, SIZE_OF_GRID):
    onTrack = False
    possible_directions = []

    # lowest center point in camera matrix
    robot_position = mat[-1][int(SIZE_OF_GRID/2) - 1: int(SIZE_OF_GRID/2) + 1]

    # straight
    straight_line = mat[SIZE_OF_GRID //
                        2:, int(np.floor(SIZE_OF_GRID/2)) - 1: int(np.ceil(SIZE_OF_GRID/2)) + 1]

    # straight line sides
    straight_line_left_side = mat[SIZE_OF_GRID //
                                  2 + 1:, int(np.floor(SIZE_OF_GRID/2)) - 2]
    straight_line_right_side = mat[SIZE_OF_GRID //
                                   2 + 1:, int(np.ceil(SIZE_OF_GRID/2)) + 2]
    # right turn
    right = mat[3 * SIZE_OF_GRID // 4:, -1].mean() < 128

    # left turn
    left = mat[3 * SIZE_OF_GRID // 4:, 0].mean() < 128

    if (not all(robot_position)):
        onTrack = True
        if (straight_line.mean() < 85):
            possible_directions.append("straight")
        elif ((straight_line_left_side.mean() < 128 and not left) or (straight_line_right_side.mean() < 128 and not right) and ("straight" not in possible_directions)):
            possible_directions.append("straight")
        if (right):
            possible_directions.append("right")
        if (left):
            possible_directions.append("left")

    # clear_console()
    print("\nMatrix: \n", mat)
    print("On track: ", onTrack)
    print("Possible directions: ", possible_directions)

    return possible_directions


def command_to_send_to_robot(command):
    # there has to be implemented command sending to the robot
    # for now it's just printing of command
    print("Command: ", command)


def find_aruco_markers(frame, markerSize=6, totalMarkers=250, draw=True):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()

    bboxs, ids, rejected = aruco.detectMarkers(
        gray, arucoDict, parameters=arucoParam)

    if draw:
        aruco.drawDetectedMarkers(frame, bboxs)

        return [bboxs, ids]
