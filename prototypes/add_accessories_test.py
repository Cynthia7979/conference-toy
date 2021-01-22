"""Sorry for the waiting!
我吃到瓜了 震惊.jpg"""

import cv2

background_img = cv2.imread('../resources/mopemope.jpg')
accessory_img = cv2.imread('../resources/pigeon.png', cv2.IMREAD_UNCHANGED)

delta_x = delta_y = 100  # 原来可以这么写
y1, y2 = delta_y, delta_y + accessory_img.shape[0]
x1, x2 = delta_x, delta_x + accessory_img.shape[1]

alpha_accessory = accessory_img[:, :, 3] / 255.0
alpha_back = 1.0 - alpha_accessory

for c in range(0, 3):
    background_img[y1:y2, x1:x2, c] = (alpha_accessory * accessory_img[:, :, c] +
                                       alpha_back * background_img[y1:y2, x1:x2, c])

cv2.imwrite('../result.jpg', background_img)
