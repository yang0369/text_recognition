import re
import logging
import pickle
import pathlib
import numpy as np

from src.pre_processing_pipeline import start_preprocessing_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Captcha(object):
    def __init__(self):
        logger.info("initiating Captcha model...")
        path = pathlib.Path(__file__).parents[1] / "sampleCaptchas" / "model" / "model.p"
        with open(path, 'rb') as fp:
            self.model = pickle.load(fp)
        logger.info("model loaded")

    def __call__(self, im_path: str, img_name: str, save_path: str = None, display: bool = False) -> str:
        """
        Algo for inference
        :param im_path: .jpg image path to load and to infer
        :param img_name: name of image
        :param save_path: output file path to save the one-line outcome
        :param display: to display the original image
        :return: predicted label of the image
        """
        if display:
            tokens = start_preprocessing_image(im_path, img_name, True, True)
        else:
            tokens = start_preprocessing_image(im_path, img_name, True, False)
        labels = self.get_token_label(tokens, self.model)
        logger.info("predicted label as: %s", labels)

        if save_path:
            fp = save_path + "/output" + re.search(r"\d+", img_name).group() + ".txt"
            with open(fp, "w") as txt:
                txt.write(labels)
            logger.info("label was saved at directory: %s", fp)
        return labels

    @staticmethod
    def get_token_label(tokens: list, model: dict) -> str:
        """
        get the label of each token
        :param tokens: list of image hashes
        :param model: dictionary of image hashes
        :return: predicted label of the image
        """
        out = list()
        for i in tokens:
            minimum = np.Inf
            label = None
            for k, v in model.items():
                if v - i < minimum:
                    label = k
                    minimum = v - i
            out.append(label)
        out = "".join(out)
        return out


if __name__ == "__main__":
    predict = Captcha()

    path = pathlib.Path(__file__).parents[1] / "sampleCaptchas" / "input"
    image_name = "input21.jpg"
    labels = predict(path, image_name, save_path=None, display=True)

    # save_dir = "../sampleCaptchas/output"
    # labels = predict(path, image_name, save_path=save_dir, display=True)

