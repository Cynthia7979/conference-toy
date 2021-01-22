import numpy as np
import cv2

capture = cv2.VideoCapture(1+cv2.CAP_DSHOW)
print('getting video')

while True:

    return_value, frame = capture.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 对不起 我孤陋寡闻.jpg
        break

capture.release()
cv2.destroyAllWindows()
