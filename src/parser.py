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
        result = np.zeros(1)

        for key in self._templates.keys():
            template = self._templates.get(key)
            h, w, _ = template.shape
            res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= self._threshold)
            result = np.append(result, zip(*loc[::-1]))
        return ""

    def get_tetromino(self, frame):
        """return the tetromino found in the frame"""
        pass
