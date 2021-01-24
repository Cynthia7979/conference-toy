import pyvirtualcam
import sys, os
import numpy as np
from PIL import Image
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
    globals()['mousemove_callbacks'] = [move_moving_accessories]
    globals()['mousedown_callbacks'] = []
    globals()['mouseup_callbacks'] = []
    globals()['button_up_callbacks'] = {}
    globals()['button_down_callbacks'] = {}

    globals()['gui_hidden'] = False
    globals()['frame_placeholder'] = None

    globals()['accessories'] = {}
    globals()['image_map'] = []
    globals()['moving_accessory_index'] = None
    globals()['last_mousepos'] = (0, 0)

    root = Tk()
    root.withdraw()
    # root.call('wm', 'attributes', '.', '-topmost', True)

    # Test capture
    return_value, frame = VIDEO_CAPTURE.read()
    if not return_value:
        raise CameraError('Cannot correctly connect to camera')
    width, height = frame.shape[:2][::-1]

    setMouseCallback(MAIN_WINDOW_NAME, mouse_callback)

    with pyvirtualcam.Camera(width=width, height=height, fps=15) as cam:
        print('WebCam initiated')

        globals()['next_bottomleft'] = globals()['next_bottomright'] = height

        while True:
            if cv2.waitKey(1) & 0xFF in (ord('q'), ord('x')):  # If quit
                return

            if globals()['frame_placeholder'] is not None:
                frame = globals()['frame_placeholder']
            else:
                return_value, frame = VIDEO_CAPTURE.read()
            show_main_gui(frame.copy(), width, height)

            for accessory_index in globals()['accessories'].keys():
                frame = display_accessory(frame, accessory_index)
            frame = cvtColor(frame, COLOR_BGR2RGBA)
            cam.send(frame)
            cam.sleep_until_next_frame()

            # print('continued...')


def show_main_gui(frame, width, height):
    # Source operations
    frame = flip(frame, 1)

    # Accessories
    for accessory_index in globals()['accessories'].keys():
        frame = display_accessory(frame, accessory_index)

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
        add_click_callback(button_2_topleft, button_2_bottomright, lambda: add_accessory(frame))

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
        add_click_callback(button_3_topleft, button_3_bottomright, lambda: add_frame_placeholder(width, height))

    imshow(MAIN_WINDOW_NAME, frame)


def mouse_callback(event, x, y, flag, *userdata):
    # print(event, x, y, flag, *userdata)
    globals_copy = complete_copy(globals())  # Prevent changing dictionary during callback loop
    if event is 0:
        for callback in globals_copy['mousemove_callbacks']:
            callback((x, y))
    elif event in (1, 3):  # Left/Right button down
        print('mouse button down')
        for callback in globals_copy['mousedown_callbacks']:
            callback()
        for (topleft, bottomright), callback in globals_copy['button_down_callbacks'].items():
            if clicked((x, y), topleft, bottomright):
                callback()
    elif event in (2, 4):  # Left/Right button up
        print('mouse button up')
        for callback in globals_copy['mouseup_callbacks']:
            callback()
        for (topleft, bottomright), callback in globals_copy['button_up_callbacks'].items():
            if clicked((x, y), topleft, bottomright):
                callback()
    globals()['last_mousepos'] = (x, y)


def clicked(mousepos, rect_topleft, rect_bottomright):
    x, y = mousepos
    left, top = rect_topleft
    right, bottom = rect_bottomright
    print(mousepos, rect_topleft, rect_bottomright, f'({left} <= {x} <= {right}) and ({top} <= {y} <= {bottom}) = {(left <= x <= right) and (top <= y <= bottom)}')
    return (left <= x <= right) and (top <= y <= bottom)


def add_click_callback(rect_topleft, rect_bottomright, callback):
    globals()['button_down_callbacks'][(rect_topleft, rect_bottomright)] = callback


def toggle_gui():
    print('Toggled GUI')
    globals()['gui_hidden'] = not globals()['gui_hidden']


def add_accessory(frame):
    print('Adding accessory')
    file_path = askopenfilename(filetypes=[('images', '.jpg .png')])  # TODO: Add GIF Support
    if file_path:
        # accessory_img = imread(file_path, IMREAD_UNCHANGED)
        accessory_img = Image.open(file_path).convert('RGBA')
        accessory_img = np.array(accessory_img)
        accessory_img = cvtColor(accessory_img, COLOR_RGBA2BGRA)

        x2, y2 = (accessory_img.shape[1], accessory_img.shape[0])
        # Shrink the most different side and, to scale, the other side
        if any([accessory_img.shape[i] > frame.shape[i] for i in (0, 1)]):
            d_width = accessory_img.shape[0] - frame.shape[0]
            d_height = accessory_img.shape[1] - frame.shape[1]
            new_width, new_height, *_ = accessory_img.shape  # Prevent undefined
            if d_width >= d_height:
                new_width = frame.shape[0]
                new_height = int(accessory_img.shape[1] * (frame.shape[0] / accessory_img.shape[0]))
            elif d_height > d_width:
                new_height = frame.shape[1]
                new_width = int(accessory_img.shape[0] * (frame.shape[1] / accessory_img.shape[1]))
            accessory_img = resize(accessory_img, (new_width, new_height))
            (x2, y2) = (new_width, new_height)


        topleft = (0, 0)
        bottomright = (x2, y2)
        globals()['image_map'].append(accessory_img)
        accessory_index = len(globals()['image_map'])-1
        globals()['accessories'][accessory_index] = (topleft, bottomright)
        # globals()['button_down_callbacks'][(topleft, bottomright)] = lambda: register_moving_accessory(accessory_index)
        # globals()['button_up_callbacks'][(topleft, bottomright)] = lambda: unregister_moving_accessory(accessory_index)
        print('Added accessory from', file_path)


def add_frame_placeholder(width, height):
    print('Adding placeholder frame')
    file_path = askopenfilename(filetypes=[('images', '.jpg .png')])
    if file_path:
        # accessory_img = imread(file_path, IMREAD_UNCHANGED)
        placeholder_img = Image.open(file_path).convert('RGBA')
        placeholder_img = np.array(placeholder_img)
        placeholder_img = cvtColor(placeholder_img, COLOR_RGBA2BGRA)
        placeholder_img = resize(placeholder_img, (width, height))
        globals()['frame_placeholder'] = placeholder_img


def register_moving_accessory(accessory_index):
    print('Start moving', accessory_index)
    globals()['moving_accessory_index'] = accessory_index


def unregister_moving_accessory(accessory_index):
    print('Stop moving', accessory_index)
    globals()['moving_accessory_index'] = None


def display_accessory(frame, accessory_index):
    frame = frame.copy()
    (x1, y1), (x2, y2) = globals()['accessories'][accessory_index]
    accessory_img = globals()['image_map'][accessory_index]

    alpha_accessory = accessory_img[:, :, 3] / 255.0
    alpha_back = 1.0 - alpha_accessory

    for c in range(0, 3):
        frame[y1:y2, x1:x2, c] = (alpha_accessory * accessory_img[:, :, c] +
                                  alpha_back * frame[y1:y2, x1:x2, c])  # FIXME: If add mopemope.jpg ValueError
    return frame


def complete_copy(dictionary):
    copy = {}
    for key, value in dictionary.items():
        if type(value) == list:
            value = tuple(value)
        elif type(value) == dict:
            value = value.copy()
        copy[key] = value
    return copy


def move_moving_accessories(mousepos):
    x, y = mousepos
    last_x, last_y = globals()['last_mousepos']
    delta_x, delta_y = x - last_x, y - last_y
    delta_x = 0 if delta_x < 0 else delta_x
    delta_y = 0 if delta_y < 0 else delta_y
    moving_accessory_index = globals()['moving_accessory_index']
    if moving_accessory_index is not None:
        print('Moved', moving_accessory_index, 'by', delta_x, delta_y)
        (left, top), (right, bottom) = globals()['accessories'][moving_accessory_index]
        new_topleft = (left+delta_x, top+delta_y)
        new_bottomright = (right+delta_x, bottom+delta_y)
        # Change image-position map
        globals()['accessories'][moving_accessory_index] = (new_topleft, new_bottomright)
        # Change click area
        globals()['button_down_callbacks'][(new_topleft, new_bottomright)] = lambda: register_moving_accessory(
            moving_accessory_index)
        globals()['button_up_callbacks'][(new_topleft, new_bottomright)] = lambda: unregister_moving_accessory(
            moving_accessory_index)
        del globals()['button_up_callbacks'][((left, top), (right, bottom))]  # FIXME: KeyError?
        del globals()['button_down_callbacks'][((left, top), (right, bottom))]


if __name__ == '__main__':
    main()
    print('quitting')
    destroyAllWindows()
    sys.exit()  # Program may fail to exit. In this scenario please kill the process manually.
