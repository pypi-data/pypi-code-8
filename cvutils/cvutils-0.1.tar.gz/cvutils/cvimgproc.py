import cv2, os

def imresize(image, width, height = None):
    '''
    This function resizes the image. If no height is supplied,
    it is calculated automatically from the width supplied.

    image --> input image (numpy array)
    width --> width to which the image is be resized
    height --> (optional) height to which the image is be resized
    '''
    if not height:
        height = image.shape[0]*width/image.shape[1]
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

