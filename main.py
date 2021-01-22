from cv2 import *
import pyvirtualcam
import numpy as np
import sys, os


class CameraError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args)


CAMERA_INDEX = 1
VIDEO_CAPTURE = VideoCapture(CAMERA_INDEX+CAP_DSHOW)

MAIN_WINDOW_NAME = 'Conference Toy'
MAIN_GUI = namedWindow(MAIN_WINDOW_NAME)

FONT = cv2.FONT_HERSHEY_SIMPLEX


def main():
    # Test capture
    return_value, frame = VIDEO_CAPTURE.read()
    if not return_value:
        raise CameraError('Cannot correctly connect to camera')
    width, height = frame.shape[:2][::-1]

    setMouseCallback(MAIN_WINDOW_NAME, mouse_callback)

    with pyvirtualcam.Camera(width=width, height=height, fps=30) as cam:
        print('WebCam initiated')

        while True:
            return_value, frame = VIDEO_CAPTURE.read()
            show_main_gui(frame, width, height)
            if cv2.waitKey(1) & 0xFF in (ord('q'), ord('x')):  # If quit
                raise Exception


def show_main_gui(frame, width, height):
    # gui_background = np.zeros((height, width, 4), np.uint8)  # Who in the world would use (h, w, d)???
    # gui_background[:,:,:] = 0

    # Source operations
    frame = flip(frame, 1)

    # GUI Drawing
    frame = draw_labelled_button(frame, button_w=147, button_h=35,
                                          window_w=width, window_h=height,
                                          text='Hide GUI')
    imshow(MAIN_WINDOW_NAME, frame)
    # imshow(MAIN_WINDOW_NAME, gui_background)


def mouse_callback(event, x, y, flag, *userdata):
    print(event, x, y)


def draw_labelled_button(surface, button_w, button_h, window_w, window_h, text, color=(255,255,255), align='topright',
                         margin=30):
    # Draw the Rectangle
    left_x = window_w-margin-button_w if 'right' in align else margin
    top_y = margin if 'top' in align else window_h-margin-button_h
    right_x = window_w-margin if 'right' in align else margin+button_w
    bottom_y = margin+button_h if 'top' in align else window_h-margin
    surface = rectangle(surface, (left_x, top_y), (right_x, bottom_y), color, thickness=-1)

    # Draw the Text
    putText(surface, text, (left_x+2, bottom_y-2), FONT, 1, color=(0,0,0), thickness=2, lineType=LINE_AA)

    return surface


if __name__ == '__main__':
    main()
    destroyAllWindows()
    sys.exit()
