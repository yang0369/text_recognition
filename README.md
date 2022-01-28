# Read CAPTCHAS By Machine



## Project Introduction

CAPTCHA (Completely Automated Public Turing test to tell Computers and Humans Apart) is a type of security measure used to protect websites from malicoious spam and web-bots. In this assignment, the captchas are images which contains exactly 5 characters with same font, font size, spacing, colour and structures etc. 

There are two sets of imagery provoided: 

 ┣ 📂sampleCaptchas
 ┃ ┣ 📂input
 ┃ ┣ 📂output

Here we have 26 images stored in the input folder, among which 25 images have their labels in the output folder, and 1 image ("input100.jpg") for me to predict its content. 



## Project Directory

```
📦text_recognition_1
 ┣ 📂.git
 ┣ 📂images
 ┣ 📂sampleCaptchas
 ┃ ┣ 📂cleaned_input
 ┃ ┣ 📂input
 ┃ ┣ 📂model
 ┃ ┣ 📂output
 ┣ 📂src
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜pre_processing_pipeline.py
 ┃ ┗ 📜predicting_pipeline.py
 ┣ 📂test_src
 ┃ ┗ 📜test_predicting_pipeline.py
 ┣ 📜.gitignore
 ┣ 📜AIS Test 2.docx
 ┣ 📜EDA.ipynb
 ┣ 📜README.md
 ┗ 📜requirements.txt
```

Notes:

- [ ] 📜EDA.ipynb : used to explore and clean the data, subsequently to experiment some modelling ideas. 
- [ ] 📜pre_processing_pipeline.py and 📜predicting_pipeline.py : used to make the final idea into full pipeline.
- [ ] 📜test_predicting_pipeline.py : a simple test case for test image



## Quick Tour

First of all, let's take a look at the original image:

<img src="./images/test_image.png" alt="test_image" style="zoom:50%;" />

Noticed that the images have three channels and some noise background, we can convert them to single channel grayscale with totally white background for the ease of character recognition later. 

<img src="./images/cleaned_image.png" alt="cleaned_image" style="zoom:50%;" />

Now, I have this cleaned version of image using otsu algorithm, which is a method to search for the best threshold value to binarize a grayscale image. A short intro about this otsu algorithm, it bascially tries each pixel value, from 0 to 255, to see which value as a threshold can separate the pixel values into two groups with the minimum weighted average of intra variances.

Time for the modelling part. The first idea that came to my mind was OCR. Because this task is indeed just to identify characters from images. So I have tried with the popular python library - pytesseract, it is a wrapper for google's OCR engine, and supports various image types such as jpeg, png, gif etc. 

With the tesseract model, I tried with some images. Well, the result is pretty good considering that we did not feed the model with any of our images, it can predict most of the characters and digits correct (I guess the credits go to the cleaniness of the original images) 

<img src="./images/OCR_1.png" alt="OCR_1" style="zoom:50%;" />

But error is expected, the example below shows OCR recognised "5" as "S", this is quite easy to understand as both "5" and "S" do look alike. There seems to be some room for improvement still.

<img src="./images/OCR_2.png" alt="OCR_2" style="zoom:50%;" />

Next, I tried to train my own OCR model with 25 images, erm... I knew the data size is too small for a data-hungry monster like neural network. But I guess no harm to try and check the result out. So here we go with a Keras-based RNN model. The result on the validation set was super poor. Since I am not an expert on computer vision, I tried to validate the model with the Keras tutorial dataset, instead of feeding all thousands of images, I trained the model with 25 images. As a consequence, it performed as bad as mine. Therefore, I have decided to skip this episode. 

<img src="/Users/6estates/Desktop/personal_git/text_recognition_1/images/RNN.png" alt="RNN" style="zoom:50%;" />

Lastly, I tried with pixel matching - the simplest and most brute-force way. As all the characters have same font size and same structure, I first cropped each character in training dataset to individual rectangular shape, then converted the image to an image hash using "imagehash" libraray, subsequently stored all the individual characters to a python dictionary, where the key is the label and value is the hash. Here, you may wonder what is the hash of an image? Well, image hash is derived with a few steps below:

1. reduce the size of raster image.
2. get the mean value of all pixel values in the image.
3. take the boolean of each pixel by comparing each pixel value with the mean.

Now take glimpse at the dict of image hash, each hash is bascially a 2d array of boolean value.

<img src="./images/Hashdict.png" alt="Hashdict" style="zoom:50%;" />

 This image hash has one great feature - they can be used to get the dissimilarity between two images.  e.g. hash of char "L" - hash of char "L" = 0, while hash of char "L" - hash of char "A" = 8. With this dictionary of image hashes, we can easily get the label of any images!

