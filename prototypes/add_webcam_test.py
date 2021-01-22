import pyvirtualcam
import cv2
import numpy as np

print('Starting')
capture = cv2.VideoCapture(1+cv2.CAP_DSHOW)

with pyvirtualcam.Camera(width=640, height=480, fps=30) as cam:
    print('WebCam initiated')
    while True:
        return_value, frame = capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        # frame = cv2.resize(frame, (1280, 720))
        print(frame.shape)
        cv2.imshow('hi',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 对不起 我孤陋寡闻.jpg
            break
        cam.send(frame)
        print('frame')
        cam.sleep_until_next_frame()

# with pyvirtualcam.Camera(width=1280, height=720, fps=30) as cam:
#     print('WebCam initiated')
#     while True:
#         frame = np.zeros((cam.height, cam.width, 4), np.uint8) # RGBA
#         frame[:,:,:3] = cam.frames_sent % 255 # grayscale animation
#         frame[:,:,3] = 255
#         print('frame')
#         cam.send(frame)
#         cam.sleep_until_next_frame()

# I see
# 是OBS的问题，我先下播了各位（
