import stag
import cv2
import numpy as np

img_path = "testimage.jpg"
img = cv2.imread(img_path)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(corners, ids) = stag.detectMarkers(img_gray)

img_out = img

for bounding_box, id in zip(corners, ids):
    bounding_box = np.round(bounding_box).astype(int)
    green = (50, 255, 50)
    red = (0, 0, 255)
    white = (255, 255, 255)

    center = tuple(np.round(np.mean(bounding_box, axis=0)).astype(int))

    # draw white circle at top-left corner
    img_out = cv2.circle(img_out, bounding_box[0], 6, white, -1, cv2.LINE_AA)
    # draw white border
    for i in range(4):
        img_out = cv2.line(img_out, tuple(map(int, bounding_box[i])), tuple(map(int, bounding_box[(i+1)%4])), white, 3, cv2.LINE_AA)

    # draw green circle at top-left corner
    img_out = cv2.circle(img_out, bounding_box[0], 5, green, -1, cv2.LINE_AA)
    # draw green border
    for i in range(4):
        img_out = cv2.line(img_out, tuple(map(int, bounding_box[i])), tuple(map(int, bounding_box[(i+1)%4])), green, 2, cv2.LINE_AA)

    # draw white circle at center
    img_out = cv2.circle(img_out, center, 6, white, -1, cv2.LINE_AA)
    # draw green circle at center
    img_out = cv2.circle(img_out, center, 6, green, -1, cv2.LINE_AA)

    img_out = cv2.putText(img_out, f"{id}", center, cv2.FONT_HERSHEY_DUPLEX, 2, white, 5, cv2.LINE_AA)
    img_out = cv2.putText(img_out, f"{id}", center, cv2.FONT_HERSHEY_DUPLEX, 2, red, 2, cv2.LINE_AA)


cv2.imwrite("testimage_result.jpg", img_out)
print("Detected Corners: ", corners)
print("Detected Ids: ", ids)
print("Results are visualized in testimage_result.jpg")

