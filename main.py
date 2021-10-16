# import the opencv library
import cv2
import matplotlib.pyplot as plt
import numpy as np

# define a video capture object
vid = cv2.VideoCapture(0)


def empty(a):
    pass


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 100)

cv2.createTrackbar("Treshold 1", "Parameters", 150, 255, empty)
cv2.createTrackbar("Treshold 2", "Parameters", 255, 255, empty)


def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if (area > 1000):
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 3)


def main():
    while(True):
        ret, img = vid.read()
        treshold1 = cv2.getTrackbarPos("Treshold 1", "Parameters")
        treshold2 = cv2.getTrackbarPos("Treshold 2", "Parameters")
        kernel = np.ones((5, 5))
        imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgCanny = cv2.Canny(imgGray, treshold1, treshold2)
        imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
        imgContour = img.copy()

        getContours(imgDil, imgContour)

        cv2.imshow('3', imgContour)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
