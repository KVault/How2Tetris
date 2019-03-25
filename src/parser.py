from os import listdir
from os.path import isfile, join
from pathlib import Path

import cv2


class Parser:
    """List of utilities to parse a given frame and return the content in form of text"""

    def __init__(self, threshold=0.2):
        self._templates_path = '../data/'
        self._templates = {}
        self._threshold = threshold
        for template in listdir(self._templates_path):
            file = join(self._templates_path, template)
            if isfile(file):
                key = Path(file).resolve().stem
                self._templates[key] = cv2.imread(file)

    def get_char(self, frame, numbers_only=False):
        """return the char found in the frame"""
        char = ''
        final_max = -1

        black = [0, 0, 0]
        frame = cv2.copyMakeBorder(frame, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=black)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)

        cv2.imshow('test', frame)

        for key in self._templates.keys():
            template = self._templates.get(key)

            res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val > final_max:
                char = key
                final_max = max_val
        return char

    def get_tetromino(self, frame):
        """return the tetromino found in the frame"""
        pass
