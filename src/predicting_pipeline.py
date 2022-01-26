import logging
import pickle
from pathlib import Path
import re
from src.pre_processing_pipeline import start_preprocessing_image

logger = logging.getLogger('Captcha')
logger.setLevel(logging.INFO)


class Captcha(object):
    def __init__(self):
        logger.info("initiating Captcha model...")
        path = Path(__file__).parents[1] / "sampleCaptchas" / "model" / "model.p"
        with open(path, 'rb') as fp:
            self.model = pickle.load(fp)
        logger.info("model loaded")

    def __call__(self, im_path, img_name, save_path):
        """
        Algo for inference
        args:
            im_path: .jpg image path to load and to infer
            save_path: output file path to save the one-line outcome
        """
        tokens = start_preprocessing_image(im_path, img_name, True)
        temp = list()
        for i in tokens:
            minimum = 100
            label = None
            for k, v in self.model.items():
                if v - i < minimum:
                    label = k
                    minimum = v - i
            temp.append(label)
        labels = "".join(temp)
        logger.info(f"predicted label as: {labels}")
        fp = save_path + "/output" + re.search(r"\d+", img_name).group() + ".txt"
        with open(fp, "w") as txt:
            txt.write(labels)
        logger.info(f"label is saved at directory: {fp}")
        return labels
