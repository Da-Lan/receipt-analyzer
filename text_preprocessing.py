from PIL import Image
import pytesseract
import cv2
import numpy as np
import os
import argparse
import re


if __name__ == "__main__":

    ##########################
    # Variables
    ##########################

    stop_keywords = ["total eligible", "montant", "cb sans contact"]


    ##########################
    # Script
    ##########################

    # load image
    img = cv2.imread("contrast_optimizer\\ticket_inter_20230222_crop_2.png")

    text_from_image = pytesseract.image_to_string(
        Image.fromarray(img)
    )
    print(text_from_image)

    # to lowercase and anihilate white spaces (multiple, tabs etc...)
    text_from_image_norm = re.sub(' +', ' ', text_from_image.lower())
    print(text_from_image_norm)

    # search if each lines (splited by "\n") has a product <name> <price> pattern
    matches = []
    for l in text_from_image_norm.split("\n"):
        match = re.search(".+ [0-9]+,[0-9]+", l)
        print(match)
        matches.append(match)

    # search for the ID of the last line to delete, containing a stop keyword
    # stop to loop when the first candidate is found
    after_end_id = len(matches)
    for i, match in enumerate(matches):
        if (match is not None) and (any(x in match[0] for x in stop_keywords)):
            print("stop keyword found at index ", i , ":", match[0])
            after_end_id = i
            break

    # only keep lines before the line containing a stop keyword
    matches_elag = [x for x in matches[:after_end_id] if x is not None]
    print(matches_elag)

    # only keep string part, not the matching informations
    products_lines = [x[0] for x in matches_elag]
    print(products_lines)