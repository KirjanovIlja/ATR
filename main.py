from my_lib import *


SIZE_OF_GRID = 8
THRESH_LOW = 120
THRESH_HIGH = 255
SOURCE = "TEST_1.MOV"

ARUCO_ID_VALUE = {
    100: "left",
    101: "right",
    102: "straight"
}


def main():
    vid = cv2.VideoCapture(SOURCE)
    LAST_READED_ARUCO_ID = None

    while(vid.isOpened()):

        # Video reading
        ret, img = vid.read()
        cv2.imshow('Original', img)

        # Frame processing
        img_lowered_resolution = lower_resolution(img, SIZE_OF_GRID)
        img_lowered_resolution = cv2.threshold(
            img_lowered_resolution, THRESH_LOW, THRESH_HIGH, cv2.THRESH_BINARY)[1]

        # Retrieve the possible directions from input image
        possible_directions_array = possible_directions(
            img_lowered_resolution, SIZE_OF_GRID)

        # Try to find, read and get Aruco code value
        aruco_marker = find_aruco_markers(img)

        # Check if Aruco marker is recognized, if so, get its value
        if (aruco_marker[1] != None):

            # Get direction from aruco marker id
            aruco_marker_value = ARUCO_ID_VALUE[aruco_marker[1][0][0]]
            LAST_READED_ARUCO_ID = aruco_marker_value

            # If it's possible to go the direction aruco points to then send command to the robot
            if (aruco_marker_value in possible_directions_array):
                command_to_send_to_robot(aruco_marker_value)
                exit()  # Exit when command is sent
            else:
                command_to_send_to_robot(
                    "No Aruco markers. Going default way - straight")
        else:
            command_to_send_to_robot(
                "No Aruco markers. Going default way - straight")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("Last readed ARUCO marker ID: ", LAST_READED_ARUCO_ID)
        clear_console()
    vid.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
