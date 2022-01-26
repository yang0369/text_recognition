import cv2
import glob
import os
import numpy as np
import pytesseract
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from pathlib import Path
from collections import Counter
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def read_in_images(path: str, image_name: str) -> np.array:
    """
    read in image based on its path, and clean the image
    :param path: directory
    :param image_name: name of image
    :return: image array in scale of 0-255
    """
    file_path = os.path.join(path, image_name)
    image = cv2.imread(file_path)

    # convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # clear background noise
    _, image = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
    return image


def perform




