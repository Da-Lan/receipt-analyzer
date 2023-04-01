from PIL import Image
import pytesseract
import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.filters import threshold_local
import os


def save_image(im, title, file_name, cmap):
    """
    Takes an image (matrix of numbers), a title for a graph,
    a file name without extension, matplotlib colormap
    Export the matrix image as a .png image in folder "contrast_optimizer"
    """
    path_name = "contrast_optimizer"

    if not os.path.exists(path_name):
        os.makedirs(path_name)

    plt.imshow(im, cmap=cmap)
    plt.title(title)
    plt.savefig(os.path.join(path_name, file_name + ".png"),
                bbox_inches="tight")
    
    print("Saved image", file_name, ".png")

    return 0


if __name__ == "__main__":

    # load image
    img = cv2.imread('ticket_inter_20230222_crop.jpg')
    save_image(img, "input receipt", "contrast_optimizer_input_receipt", "viridis")

    # to gray scale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    save_image(img_gray, "receipt gray scale", "contrast_optimizer_gray_scale", "gray")

    # dynamic/adaptive threshold, (note for the futur: to grid-search)
    thresh = threshold_local(img_gray,
                            block_size=51,
                            method="gaussian",
                            offset=40)

    img_contr = (img_gray > thresh).astype("uint8") * 255
    save_image(img_contr, "receipt contrasted", "contrast_optimizer_contrasted", "gray")

    print("Result of contrast optimizer image processing")

    # Print result after applying tesseract text extractor
    text_from_image = pytesseract.image_to_string(
        Image.fromarray(img_contr)
    )
    print(text_from_image)