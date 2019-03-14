import cv2

from src.modelgenerator import ModelGenerator
from src.screencapture import ScreenCapture


def main():
    screen_capture = ScreenCapture()
    generator = ModelGenerator()
    while True:
        frame_rgb = screen_capture.frame_rgb()
        model, frame = generator.refresh(frame_rgb)
        cv2.imshow("Frame", frame)
        cv2.waitKey(15)


# Fuck you Python
if __name__ == '__main__':
    main()
