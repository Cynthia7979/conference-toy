import pyvirtualcam
import sys, os
from cv2 import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename


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
    globals()['buttons'] = []
    globals()['callbacks'] = {}
    globals()['gui_hidden'] = False

    Tk().withdraw()

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
            # print('continued...')


def show_main_gui(frame, width, height):
    # Source operations
    frame = flip(frame, 1)

    # Button 1 "Hide GUI"
    # Display
    button_1_topleft = (width-BUTTON_MARGIN-147, BUTTON_MARGIN)
    button_1_bottomright = (width-BUTTON_MARGIN, BUTTON_MARGIN+35)
    frame = rectangle(frame,
                      button_1_topleft,
                      button_1_bottomright,
                      color=WHITE, thickness=-1)
    putText(frame, 'Hide GUI',
            (width-BUTTON_MARGIN-147+TEXT_MARGIN, BUTTON_MARGIN+35-TEXT_MARGIN),
            FONT, fontScale=1, color=BLACK, thickness=2, lineType=LINE_AA)
    # Interactions
    add_click_callback(button_1_topleft, button_1_bottomright, toggle_gui)

    if not globals()['gui_hidden']:
        # Button 2 "Add Accessory"
        # Display
        button_2_topleft = (BUTTON_MARGIN, BUTTON_MARGIN)
        button_2_bottomright = (BUTTON_MARGIN+250, BUTTON_MARGIN+35)
        frame = rectangle(frame,
                          button_2_topleft,
                          button_2_bottomright,
                          color=WHITE, thickness=-1)
        putText(frame, 'Add Accessory',
                (BUTTON_MARGIN+TEXT_MARGIN, BUTTON_MARGIN+35-TEXT_MARGIN),
                FONT, fontScale=1, color=BLACK, thickness=2, lineType=LINE_AA)
        # Interactions


        # Button 3 Set/Remove Still Frame
        # Display
        button_3_topleft = (BUTTON_MARGIN, BUTTON_MARGIN + (BUTTON_MARGIN+35))
        button_3_bottomright = (BUTTON_MARGIN+400, BUTTON_MARGIN+35 + (BUTTON_MARGIN+35))
        frame = rectangle(frame,
                          button_3_topleft,
                          button_3_bottomright,
                          color=WHITE, thickness=-1)
        putText(frame, 'Set/Remove Still Frame',
                (BUTTON_MARGIN+TEXT_MARGIN, BUTTON_MARGIN+35-TEXT_MARGIN + (BUTTON_MARGIN+35)),
                FONT, fontScale=1, color=BLACK, thickness=2, lineType=LINE_AA)
        #Interactions


    imshow(MAIN_WINDOW_NAME, frame)


def mouse_callback(event, x, y, flag, *userdata):
    print(event, x, y, flag, *userdata)
    if event == 1:  # Left click
        for (topleft, bottomright), callback in globals()['callbacks'].items():
            if clicked((x, y), topleft, bottomright):
                callback()


def clicked(mousepos, rect_topleft, rect_bottomright):
    x, y = mousepos
    left, top = rect_topleft
    right, bottom = rect_bottomright
    print(mousepos, rect_topleft, rect_bottomright, f'({left} <= {x} <= {right}) and ({top} <= {y} <= {bottom}) = {(left <= x <= right) and (top <= y <= bottom)}')
    return (left <= x <= right) and (top <= y <= bottom)


def add_click_callback(rect_topleft, rect_bottomright, callback):
    globals()['callbacks'][(rect_topleft, rect_bottomright)] = callback


def toggle_gui():
    print('Toggled GUI')
    globals()['gui_hidden'] = not globals()['gui_hidden']


if __name__ == '__main__':
    main()
    print('quitting')
    destroyAllWindows()
    sys.exit()  # Program may fail to exit. In this scenario please kill the process manually.
