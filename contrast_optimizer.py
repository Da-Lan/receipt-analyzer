from PIL import Image
import pytesseract
import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.filters import threshold_local
import os
import argparse


def save_image(im, file_name, cmap):
    """
    Takes an image (matrix of numbers),
    a file name without extension, a matplotlib colormap
    Export the matrix image as a .png image file in folder "contrast_optimizer"
    """
    path_name = "contrast_optimizer"

    if not os.path.exists(path_name):
        os.makedirs(path_name)
    
    plt.imsave(fname=os.path.join(path_name, file_name + ".png"),
               arr=im,
               cmap='gray',
               format='png')

    print("Saved image", file_name + ".png")

    return 0


if __name__ == "__main__":

    # get script input args
    parser = argparse.ArgumentParser(description='Get input argument')
    parser.add_argument('input_filename')
    args = parser.parse_args()
    print("run contrast_optimizer with args", args)

    # load image
    img = cv2.imread(args.input_filename)
    save_image(img, args.input_filename.split(".")[0] + "_0", "viridis")

    # to gray scale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    save_image(img_gray, args.input_filename.split(".")[0] + "_1", "gray")

    # dynamic/adaptive threshold, (note for the futur: to grid-search)
    thresh = threshold_local(img_gray,
                            block_size=51,
                            method="gaussian",
                            offset=40)

    img_contr = (img_gray > thresh).astype("uint8") * 255
    save_image(img_contr, args.input_filename.split(".")[0] + "_2", "gray")

    print("Result of contrast optimizer image processing")

    # Print result after applying tesseract text extractor
    text_from_image = pytesseract.image_to_string(
        Image.fromarray(img_contr)
    )
    print(text_from_image)