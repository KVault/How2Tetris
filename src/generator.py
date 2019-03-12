from typing import NamedTuple

import cv2


class Generator:
    def __init__(self):
        pass

    def refresh(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # cv2.rectangle(frame, (20, 20), (80, 80), (0, 255, 0), 3)
        frame = self.crop_window_border(frame)
        return None, frame

    @staticmethod
    def crop_window_border(frame):
        _, binary_image = cv2.threshold(frame, 1, 255, 0)
        contours, hier = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours_list = []
        for contour in contours:
            area = cv2.contourArea(contour)
            contours_list.append(Contour(area=area, value=contour))

        contours_list = sorted(contours_list, key=lambda x: x.area)
        x, y, w, h = cv2.boundingRect(contours_list[-2].value)
        frame = frame[y:y + h, x:x + w]
        return frame


class Contour(NamedTuple):
    area: int
    value: tuple
