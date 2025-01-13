#!/usr/bin/env python

# Assuming core opencv-python, with graphical capabilities to show
# images at different stages of processing
import cv2
import numpy
from PIL import Image
import tesserocr


# TODO: Move flags to more durable configuration style or arguments
DEBUG = False
COMMON_SHAPE = (4, 2)
CHAR_WHITELIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.$ '

def show(title: str, image: cv2.typing.MatLike, wait: bool = True):
    '''Helper for showing image and waiting for key press'''
    cv2.imshow(title, image)
    if wait:
        cv2.waitKey(0)


def debug_show(title: str, image: cv2.typing.MatLike, wait: bool = True):
    '''Only show if DEBUG flag is set to True'''
    if DEBUG:
        show(title, image, wait)


def load_source_image(path: str) -> cv2.typing.MatLike:
    '''Loads image at supplied path and raises if no image is loaded'''
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise Exception(f'File could not be read at path {path}')
    return img


if __name__ == '__main__':
    # Initial implementation based on guidance here:
    # https://pyimagesearch.com/2021/10/27/automatically-ocring-receipts-and-scans/
    # and
    # https://medium.com/@jaelin_75015/faded-torn-rotated-receipt-ocr-with-image-preprocessing-1fb03c036504

    # TODO: Path should be passed in in the future...
    img = load_source_image('/home/thomasem/Downloads/heb-2.jpg')

    # Threshold to improve contrast using Otsu's method
    thresh_type = cv2.THRESH_BINARY+cv2.THRESH_OTSU
    _, thresholded = cv2.threshold(img, 0, 255, thresh_type)
    show('Thresholded', thresholded, wait=False)

    # Erode to make black text on white background more distinct
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morphed = cv2.erode(thresholded, kernel)
    show('Morphed', morphed, wait=False)

    p_img = Image.fromarray(thresholded)
    p_api = tesserocr.PyTessBaseAPI()

    try:
        p_api.SetImage(p_img)
        p_api.SetVariable('tessedit_char_whitelist', CHAR_WHITELIST)
        p_api.SetPageSegMode(tesserocr.PSM.SINGLE_COLUMN)

        print(p_api.GetUTF8Text())
    finally:
        # Clean up the API object and destroy cv2 windows
        p_api.End()
        # Opportunity to compare before closing windows
        cv2.waitKey(0)
        cv2.destroyAllWindows()
