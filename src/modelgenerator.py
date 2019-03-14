from typing import NamedTuple
import cv2
import numpy as np


class ModelGenerator:
    def __init__(self):
        pass

    def refresh(self, frame):
        """Processes the given frame and returns a debug image showing where the system looked
        for things and the model status for that frame"""
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = self.crop_window_border(frame)
        return None, frame

    @staticmethod
    def crop_window_border(frame: np.ndarray):
        """Uses contours to find the second largest contour of the window
        This happens to be the game window WITHOUT the window border and the menus

        :returns a cropped OpenCV Image"""
        _, binary_image = cv2.threshold(frame, 1, 255, 0)
        contours, hier = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Get all the contours and its areas in a list
        contours_list = []
        for contour in contours:
            area = cv2.contourArea(contour)
            contours_list.append(Contour(area=area, value=contour))

        # Now sort the list and get the SECOND BIGGEST which turns out to be "-2"
        contours_list = sorted(contours_list, key=lambda x: x.area)

        # Get the rectangle enclosing that contour area and crop the image
        x, y, w, h = cv2.boundingRect(contours_list[-2].value)
        frame = frame[y:y + h, x:x + w]
        return frame

    @staticmethod
    def crop_black_border(self, ar_horiz: int, ar_vert: int):
        """Using the Aspect Ratio passed as a parameter this method will process the image and
        crop any black border either top-down or on the sides of the image. We need this since
        the actual game aspect ratio won't change but the window in which it's contained can.

        In order to do this we will find the largest image (with that aspect ratio)
        that can fit in the current frame and crop the current frame to the found image"""
        pass


class Contour(NamedTuple):
    area: int
    value: tuple
