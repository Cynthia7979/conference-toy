from cv2 import *
import pyvirtualcam
import numpy as np
import sys, os


class CameraError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args)


CAMERA_INDEX = 1
VIDEO_CAPTURE = VideoCapture(CAMERA_INDEX + CAP_DSHOW)

MAIN_WINDOW_NAME = 'Conference Toy'
MAIN_GUI = namedWindow(MAIN_WINDOW_NAME)

BUTTON_MARGIN = 30
TEXT_MARGIN = 5

FONT = cv2.FONT_HERSHEY_SIMPLEX
BLACK = (0  , 0  , 0  )
WHITE = (255, 255, 255)


def main():
    # globals()['next_topleft'] = globals()['next_topright'] = -30
    # globals()['next_bottomleft'] = globals()['next_bottomright'] = None

    globals()['buttons'] = []
    globals()['callbacks'] = {}

    # Test capture
    return_value, frame = VIDEO_CAPTURE.read()
    if not return_value:
        raise CameraError('Cannot correctly connect to camera')
    width, height = frame.shape[:2][::-1]

    setMouseCallback(MAIN_WINDOW_NAME, mouse_callback)

    with pyvirtualcam.Camera(width=width, height=height, fps=30) as cam:
        print('WebCam initiated')

        globals()['next_bottomleft'] = globals()['next_bottomright'] = height

        while True:
            if cv2.waitKey(1) & 0xFF in (ord('q'), ord('x')):  # If quit
                return
            return_value, frame = VIDEO_CAPTURE.read()
            show_main_gui(frame, width, height)
            print('continued...')


def show_main_gui(frame, width, height):
    # gui_background = np.zeros((height, width, 4), np.uint8)  # Who in the world would use (h, w, d)???
    # gui_background[:,:,:] = 0

    # Source operations
    frame = flip(frame, 1)

    # GUI Drawing
    # Button 1 Hide GUI
    frame = rectangle(frame,
                      (width-BUTTON_MARGIN-147, BUTTON_MARGIN),
                      (width-BUTTON_MARGIN, BUTTON_MARGIN+35),
                      color=WHITE, thickness=-1)
    putText(frame, 'Hide GUI',
            (width-BUTTON_MARGIN-147+TEXT_MARGIN, BUTTON_MARGIN+35-TEXT_MARGIN),
            FONT, fontScale=1, color=BLACK, thickness=2, lineType=LINE_AA)
    # Button 2 Add Accessory
    frame = rectangle(frame,
                      (BUTTON_MARGIN, BUTTON_MARGIN),
                      (BUTTON_MARGIN+250, BUTTON_MARGIN+35),
                      color=WHITE, thickness=-1)
    putText(frame, 'Add Accessory',
            (BUTTON_MARGIN+TEXT_MARGIN, BUTTON_MARGIN+35-TEXT_MARGIN),
            FONT, fontScale=1, color=BLACK, thickness=2, lineType=LINE_AA)
    # Button 3 Set/Remove Still Frame
    frame = rectangle(frame,
                      (BUTTON_MARGIN, BUTTON_MARGIN + (BUTTON_MARGIN+35)),
                      (BUTTON_MARGIN+400, BUTTON_MARGIN+35 + (BUTTON_MARGIN+35)),
                      color=WHITE, thickness=-1)
    putText(frame, 'Set/Remove Still Frame',
            (BUTTON_MARGIN+TEXT_MARGIN, BUTTON_MARGIN+35-TEXT_MARGIN + (BUTTON_MARGIN+35)),
            FONT, fontScale=1, color=BLACK, thickness=2, lineType=LINE_AA)

    # frame = draw_labelled_button(frame, button_w=147, button_h=35,
    #                              window_w=width, window_h=height,
    #                              text='Hide GUI')
    # frame = draw_labelled_button(frame, button_w=200, button_h=35,
    #                              window_w=width, window_h=height,
    #                              align="topleft",
    #                              text='Add Accessory')
    # frame = draw_labelled_button(frame, button_w=250, button_h=35,
    #                              window_w=width, window_h=height,
    #                              align="topleft",
    #                              text='Set/Remove Still Frame')
    imshow(MAIN_WINDOW_NAME, frame)

def mouse_callback(event, x, y, flag, *userdata):
    print(event, x, y, flag, *userdata)


# def draw_labelled_button(surface, button_w, button_h, window_w, window_h, text, color=(255, 255, 255), align='topright',
#                          margin=10, callback=lambda *_: None):
#     # Draw the Rectangle
#     left_x = window_w-margin - button_w if 'right' in align else margin
#     top_y = globals()['next_'+align]+margin if 'top' in align else globals()['next_'+align]-margin - button_h
#     right_x = window_w-margin if 'right' in align else margin + button_w
#     bottom_y = globals()['next_'+align]+margin + button_h if 'top' in align else globals()['next_'+align]-margin
#     surface = rectangle(surface, (left_x, top_y), (right_x, bottom_y), color, thickness=-1)
#
#     # Draw the Text
#     putText(surface, text, (left_x + 2, bottom_y - 5), FONT, 1, color=(0, 0, 0), thickness=2, lineType=LINE_AA)
#
#     # Update next positions
#     print(globals()['next_'+align], align)
#     if text not in globals()['buttons']:  # New button
#         if 'top' in align:
#             globals()['next_'+align] += button_h
#             print('changed:', globals()['next_' + align], align)
#         else:
#             globals()['next_'+align] -= button_h
#         globals()['buttons'].append(text)
#         globals()['callbacks'][((left_x, top_y), (right_x, bottom_y))] = callback
#
#     return surface


if __name__ == '__main__':
    main()
    print('quitting')
    destroyAllWindows()
    sys.exit()  # Program may fail to exit. In this scenario please kill the process manually.
