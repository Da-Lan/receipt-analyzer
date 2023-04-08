from PIL import Image
import pytesseract
import cv2
import numpy as np
import os
import argparse
import re
from datetime import datetime
import pandas as pd


if __name__ == "__main__":

    ##########################
    # Variables
    ##########################

    stop_keywords = ["total eligible", "montant", "cb sans contact"]
    path_name = "text_preprocessing"


    ##########################
    # Script
    ##########################

    # get script input args
    parser = argparse.ArgumentParser(description='Get input argument')
    parser.add_argument('input_filename')
    parser.add_argument('date', nargs='?', default=datetime.today().strftime('%Y-%m-%d'))
    args = parser.parse_args()
    print("run text_preprocessing with args", args)

    # load image
    img = cv2.imread(args.input_filename)

    # Application of tesseract text extractor
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

    # Separate product names from their price into 2 lists
    products_dict = []
    for l in products_lines:
        key_val = l.rsplit(" ", 1)
        products_dict.append(key_val)

    # transpose
    products_dict_t = list(map(list, zip(*products_dict)))
    print(products_dict_t)

    # add today date to dataframe on each line, product names and prices
    df = pd.DataFrame({"date": args.date,
                    "name": products_dict_t[0],
                    "price": products_dict_t[1]})
    
    df["price"] = df["price"].str.replace(",", ".").astype(float)

    # Save result in a csv file
    if not os.path.exists(path_name):
        os.makedirs(path_name)

    df.to_csv(os.path.join(path_name,
                           args.input_filename.split(".")[0]
                           .rsplit("\\", 1)[1]
                           + "_0"
                           + ".csv"),
              sep=";",
              index=False)

    print("Saved csv", args.input_filename + ".csv")