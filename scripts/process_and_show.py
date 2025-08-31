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


def scale(image: cv2.typing.MatLike, scale_pct: int) -> cv2.typing.MatLike:
    '''Scale image by supplied percent'''
    # Interestingly, opencv's shape property on images is in the order
    # (h, w) while it expects the order (w, h) in the resize function.
    dims = (int(img.shape[1] * scale_pct / 100),
            int(img.shape[0] * scale_pct / 100))
    resized = cv2.resize(image, dims, interpolation = cv2.INTER_AREA)
    debug_show('Resized', resized)

    return resized


def edge_detection(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    '''Apply edge detection (Canny)'''
    # Convert to grayscale and blur for Canny edge detection:
    # https://en.wikipedia.org/wiki/Canny_edge_detector

    # Blur to reduce noise in overall image
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    debug_show('Blurred', blurred)

    # Open to reduce noise and clarify border of receipt
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    opened = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel)
    debug_show('Opened', opened)

    # Apply Canny edge detection
    edged = cv2.Canny(opened, 75, 200)
    debug_show('Edged', edged)

    return edged


def approximate_contour(edged: cv2.typing.MatLike) -> cv2.typing.MatLike:
    '''Find major contour (receipt) and return approximation, which
    should be a quadrilateral'''
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) < 1:
        raise Exception('No major contours')
    if len(contours) > 1:
        raise Exception('More than one major contour')

    c = contours[0]
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
    sides = len(approx)

    # TODO: Consider adding a series of epsilon values to try if we
    # can't get it down to 4 on the first try.
    if sides != 4:
        raise Exception(f'Could not approximate to four sides; found {sides}')
    return approx


def load_source_image(path: str) -> cv2.typing.MatLike:
    '''Loads image at supplied path and raises if no image is loaded'''
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise Exception(f'File could not be read at path {path}')
    return img


def order_coords(coords: cv2.typing.MatLike) -> cv2.typing.MatLike:
    '''Order coordinates in the following order:
    top-left, top-right, bottom-right, bottom-left'''
    rect = numpy.zeros(COMMON_SHAPE, dtype="float32")

    # Use sum for top-left & bottom-right
    s = coords.sum(axis=1)
    # Top-left (smallest sum)
    rect[0] = coords[numpy.argmin(s)]
    # Bottom-Right (largest sum)
    rect[2] = coords[numpy.argmax(s)]

    # Use difference for top-right & bottom-left
    diff = numpy.diff(coords, axis=1)
    # Top-right (smallest diff)
    rect[1] = coords[numpy.argmin(diff)]
    # Bottom-left (largest diff)
    rect[3] = coords[numpy.argmax(diff)]

    return rect


# Revise this function once methodology is refined
# borrowed from https://pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_coords(pts)
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = numpy.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = numpy.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = numpy.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = numpy.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = numpy.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped


if __name__ == '__main__':
    # Initial implementation based on guidance here:
    # https://pyimagesearch.com/2021/10/27/automatically-ocring-receipts-and-scans/
    # and
    # https://medium.com/@jaelin_75015/faded-torn-rotated-receipt-ocr-with-image-preprocessing-1fb03c036504

    # TODO: Path should be passed in in the future...
    img = load_source_image('/home/thomasem/Downloads/heb.jpeg')

    # Resize image down to reduce noise, and simply be more manageable
    # during testing
    scale_pct = 25
    resized = scale(img, scale_pct=scale_pct)
    contour = approximate_contour(edge_detection(resized))

    # traced = resized.copy()
    # cv2.drawContours(traced, [contour], -1, (0, 255, 0), 2)
    # debug_show('Traced', traced)

    # Reshape and scale coordinates back to original size
    scaled_coords = contour.reshape(COMMON_SHAPE).astype(float)
    transformed = four_point_transform(img, scaled_coords * (100 / scale_pct))
    debug_show('Transformed', transformed)

    # Threshold to improve contrast using Otsu's method
    thresh_type = cv2.THRESH_BINARY+cv2.THRESH_OTSU
    _, thresholded = cv2.threshold(transformed, 0, 255, thresh_type)
    show('Thresholded', thresholded, wait=False)

    # Erode to make black text on white background more distinct
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morphed = cv2.erode(thresholded, kernel)
    show('Morphed', morphed, wait=False)

    p_img = Image.fromarray(morphed)
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
