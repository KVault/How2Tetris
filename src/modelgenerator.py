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
        frame = self.crop_black_border(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        self.get_score(frame)
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
    def crop_black_border(frame, ar_horiz=16, ar_vert=15):
        """Using the Aspect Ratio passed as a parameter this method will process the image and
        crop any black border either top-down or on the sides of the image. We need this since
        the actual game aspect ratio won't change but the window in which it's contained can.

        In order to do this we will find the largest image (with that aspect ratio)
        that can fit in the current frame and crop the current frame to the found image"""

        aspect_ratio = float(ar_horiz) / float(ar_vert)
        h_origin, w_origin = frame.shape
        calculated_width = int(h_origin * aspect_ratio)
        calculated_hight = int(w_origin / aspect_ratio)
        if w_origin > calculated_width:
            to_crop = w_origin - calculated_width
            frame = frame[0:h_origin, int(to_crop / 2):w_origin - int(to_crop / 2)]
        else:
            to_crop = h_origin - calculated_hight
            frame = frame[int(to_crop / 2):h_origin - int(to_crop / 2), 0:h_origin]
        return frame

    @staticmethod
    def get_rect_percentage(frame, x_percent, y_percent, w_percent, h_percent):
        h_origin, w_origin, _ = frame.shape
        x_offset = int(w_origin * (x_percent / 100))
        y_offset = int(h_origin * (y_percent / 100))
        w_rect = int(w_origin * (w_percent / 100)) + x_offset
        h_rect = int(h_origin * (h_percent / 100)) + y_offset
        return (x_offset, y_offset), (w_rect, h_rect)

    def get_score(self, frame):
        rect = self.get_rect_percentage(frame, x_percent=75, y_percent=6, w_percent=23, h_percent=28)
        cv2.rectangle(frame, rect[0], rect[1], (0, 255, 0), 3)


class Contour(NamedTuple):
    area: int
    value: tuple
