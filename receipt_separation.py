#Python script for converting the scanned PDFs files to JPG images,
#then applying image processing via openCV to extract individual receipts
# from the original scanned pages

#in using the pdf2image library, poppler library has to be installed, and
#the poppler bin directory has to be added in the environment variable Path.

import glob, os
import cv2
import time
import numpy as np
import time

import read_config

from PIL import Image, ImageChops
from pdf2image import convert_from_path

#reading the PDF files in the directory, and then converting each to JPEG files

pdf_dir = (read_config.get_parameter_values()[10]).format(os.getenv('username'))
jpg_dir = (read_config.get_parameter_values()[14]).format(os.getenv('username'))


def separate_receipts():

    def save_asJPG():
        os.chdir(pdf_dir)
        for pdf_file in os.listdir(pdf_dir):

            if pdf_file.endswith(".pdf"):
                pages  = convert_from_path(pdf_file, 300)

                filename, extension = os.path.splitext(pdf_file)
                save_to = os.path.join(jpg_dir, "%s.jpg" % (filename))
                for page in pages:
                    page.save(save_to, "JPEG")


    def trimExcessBorder(im):
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)

    #this function takes the image, crops excess white border,and
    #processes the image for recognition (until morphological closing)
    def processImage(file):

        scanned_page = cv2.imread(jpg_file)

        scanned_page = cv2.imread(jpg_file)
        scanned_page = scanned_page[10:2440, 30:3480]

        gray = cv2.cvtColor(scanned_page, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3,3), 0 )
        #second parameter is the kernel size to be convolved
        canny_edged = cv2.Canny (blurred, 70, 250)

        #enlarge the image
        kernel_dilate = np.ones ((10,10), np.uint8)
        dilated = cv2.dilate(canny_edged, kernel_dilate, iterations = 1)

        #close gaps between the white pixels
        kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (20,20))
        closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE,kernel_close)

        #finding the contours
        return scanned_page, closed

    save_asJPG()


    count = 0

    for jpg_file in os.listdir(jpg_dir):

        if jpg_file.endswith("jpg"):
            os.chdir(jpg_dir)

            #cropping excess border from scanned PDFs
            #jpg_file_directory = os.path.join(new_file_directory, jpg_file)
            trimExcessBorder(Image.open(jpg_file)).save(jpg_file)

            scanned_page = processImage(jpg_file)[0]
            closed = processImage(jpg_file)[1]

            (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for i in cnts:
                peri = cv2.arcLength (i, True)
                approx = cv2.approxPolyDP(i, 0.02 * peri, True)

                x,y,w,h = cv2.boundingRect(i)

                path = (read_config.get_parameter_values()[9]).format(os.getenv('username'))
           
                if h > 500:
                    individual_receipt = scanned_page[y:y+h, x:x+w]
                    cv2.imwrite(os.path.join(path,'{}.jpg'.format(count)), individual_receipt)

                    count = count + 1
                    print(str(count)+ " ----- Saved to {}".format(path))


if __name__ == "__main__":
        print("Receipt separation starting...")
        print(" ")
        separate_receipts()
    
