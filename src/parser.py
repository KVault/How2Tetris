from os import listdir
from os.path import isfile, join
from pathlib import Path

import cv2
import numpy as np


class Parser:
    """List of utilities to parse a given frame and return the content in form of text"""

    def __init__(self, threshold=0.4):
        self._templates_path = '../data/'
        self._templates = {}
        self._threshold = threshold
        for template in listdir(self._templates_path):
            file = join(self._templates_path, template)
            if isfile(file):
                key = Path(file).resolve().stem
                self._templates[key] = cv2.imread(file)

    def get_text(self, frame, numbers_only=False):
        """return the text found in the frame"""
        result = np.empty((0, 2))

        for key in self._templates.keys():
            template = self._templates.get(key)
            h_frame, w_frame, _ = frame.shape
            template = cv2.resize(template, (w_frame // 6, h_frame - 1), interpolation=cv2.INTER_NEAREST)
            h, w, _ = template.shape
            res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            loc = np.where(res >= self._threshold)
            for pt in zip(*loc[::-1]):
                result = np.append(result, [(key, pt[0])], axis=0)
                cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        print(sorted(result, key=lambda x: x[1]))
        return ""

    def get_tetromino(self, frame):
        """return the tetromino found in the frame"""
        pass
