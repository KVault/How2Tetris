import cv2

from src.ScreenCapture import ScreenCapture


def main():
    screen_capture = ScreenCapture()
    while True:
        frame = screen_capture.frame_gray()
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)


# Fuck you Python
if __name__ == '__main__':
    main()
