# -*- coding: utf-8 -*-
"""barycentre.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aGDCx3TMyEcwDdsj-O-fn-dKc_weSfKi
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from PIL import Image
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import cv2
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
import albumentations as A
from skimage.exposure import rescale_intensity


import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.color import rgb2hed, hed2rgb

import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from PIL import Image
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import cv2
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
import seaborn as sns
import albumentations as A
from skimage.exposure import rescale_intensity

from skimage import data
from skimage.color import rgb2hed, hed2rgb

from brown_score import *
from image_preprocessing import *
from roi_selection import *

import os

data_dir = "/content/yolo_txt"

# Define the object class label
object_class = "lymphocyte"

for i in range(500):
    # Read in image from path
    path =f"/content/yolo_images/image_{i}.png"
    ihc_rgb = io.imread(path)
    im = Image.open(path)
    # Separate the stains from the IHC image
    ihc_hed = rgb2hed(ihc_rgb)

    # Create an RGB image for the DAB stain
    null = np.zeros_like(ihc_hed[:, :, 0])
    ihc_d = hed2rgb(np.stack((null, null, ihc_hed[:, :, 2]), axis=-1))

    img_height, img_width, channels = ihc_d.shape
    

    pre_processed = imagePreProcessing(path)
    processed2 = imageProcessing2(pre_processed)
    result, bounding_boxes1 = LF2(processed2,pre_processed)
    bounding_boxes_b = bounding_boxes1

    brown_scores = get_brown_scores(ihc_d, bounding_boxes_b)
    
    bounding_boxes = []
    for j in range(len(bounding_boxes_b)):
        
        if brown_scores[j] > 0.09:
            bounding_boxes.append(bounding_boxes_b[j])



    # Convert bounding box coordinates to YOLO format
    yolo_boxes = []
    for box in bounding_boxes:
        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1
        center_x = float(x1 + w/2) / img_width
        center_y = float(y1 + h/2) / img_height
        width = float(w) / img_width
        height = float(h) / img_height
        yolo_boxes.append([center_x, center_y, width, height])

    #print(bounding_boxes)
    #print(f"image_{i}.png,",bounding_boxes)


    # Define the path to the text file that will contain the YOLO format annotations
    txt_file = os.path.join(data_dir, f"image_{i}.txt")


    # Open the text file for writing
    with open(txt_file, "w") as f:
        # Loop over the bounding box coordinates
        for bbox in yolo_boxes:
            # Convert the bounding box coordinates to YOLO format
            x_center, y_center, w, h = bbox
            x_yolo = x_center
            y_yolo = y_center
            w_yolo = w
            h_yolo = h
            
            # Write the YOLO format annotation to the text file
            f.write(f"{object_class} {x_yolo} {y_yolo} {w_yolo} {h_yolo}\n")

    #print(bounding_boxes)
    #print(f"image_{i}.png,",yolo_boxes)