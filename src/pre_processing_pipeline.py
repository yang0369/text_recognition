import cv2
import os
import numpy as np
import imagehash
from PIL import Image


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


def break_image_into_tokens(image: np.array) -> list:
    """
    crop the original image and split it into 5 single character images
    :param image: image array in scale of 0-255
    :return: tokens
    """
    crop_img_1 = image[11:21, 5:12]
    crop_img_2 = image[11:21, 14:22]
    crop_img_3 = image[11:21, 23:31]
    crop_img_4 = image[11:21, 32:40]
    crop_img_5 = image[11:21, 41:49]
    out = [crop_img_1,
           crop_img_2,
           crop_img_3,
           crop_img_4,
           crop_img_5,
           ]
    return out


def convert_token_to_hash(token: np.array) -> imagehash.ImageHash:
    """
    convert the token image to a hash, which can be used to calculate the similarity with
    other image
    :param token: image token
    :return: hash
    """
    # convert to PIL image type
    image = Image.fromarray(token)

    # get image hash by using average hashing algorithm
    hash_val = imagehash.average_hash(image)
    return hash_val


def start_preprocessing_image(path: str, image_name: str, return_token: bool = True) -> list:
    """
    the one-stop data pre-processing pipeline to process the raw image to our required
    list of hash values
    :param path: directory
    :param image_name: name of image
    :param return_token: return hash token if True, else return np.array
    :return: list of hash
    """
    original_img = read_in_images(path, image_name)
    token_lst = break_image_into_tokens(original_img)
    if return_token:
        out = [convert_token_to_hash(i) for i in token_lst]
    else:
        out = token_lst
    return out




