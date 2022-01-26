import pytest

from src.predicting_pipeline import Captcha


@pytest.mark.parametrize("image_name",
                         [
                             "input21.jpg",
                             "input100.jpg",
                         ])
def test_prediction(image_name):
    predict = Captcha()
    path = "../sampleCaptchas/input"
    save_dir = "../sampleCaptchas/output"
    label = predict(path, image_name, save_dir)
    assert label == "YMB1Q"