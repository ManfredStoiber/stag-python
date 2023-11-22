import stag
import cv2
import numpy as np

# load image
image = cv2.imread("example.jpg")

# detect markers
(corners, ids, rejected_corners) = stag.detectMarkers(image, 21)

# draw detected markers with ids
stag.drawDetectedMarkers(image, corners, ids)

# draw rejected quads without ids with different color
stag.drawDetectedMarkers(image, rejected_corners, border_color=(255, 0, 0))

# save resulting image
cv2.imwrite("example_result.jpg", image)