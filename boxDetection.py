import cv2
import tempfile
import os
from s3 import upload_to_bucket

PNG_EXTENSION = ".png"


def getImagesForOCR(filename, conversationName, senderName, receiverName, darkMode):
    orig_image = cv2.imread(filename)

    # Get dimensions of original screenshot and
    h, w, _ = orig_image.shape
    x1 = int((155 / 1170) * w)
    y1 = int((270 / 2532) * h)
    x2 = int((1140 / 1170) * w)
    y2 = int((2300 / 2532) * h)

    cropped_image = orig_image[y1:y2, x1:x2]

    if darkMode:
        # Adjust the brightness and contrast
        # g(i,j)=α⋅f(i,j)+β
        # control Contrast by 1.5
        alpha = 1.5
        # control brightness by 50
        beta = 50
        image = cv2.convertScaleAbs(cropped_image, alpha=alpha, beta=beta)
    else:
        image = cropped_image

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 51, 9
    )

    # Fill rectangular contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (255, 255, 255), -1)

    # Morph open
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # Draw rectangles
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    rects = []
    for i in range(len(cnts) - 1, -1, -1):
        x, y, w, h = cv2.boundingRect(cnts[i])
        # Dont detect small rectangles like screen battery, profile pic
        if w > 70 and h > 70:
            # If this detected rectangle does not lie within the previous rectangle
            if not (rects and rects[-1][1] + rects[-1][-1] > y):
                # print(str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h))
                # cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
                rects.append((x, y, w, h))

    # cv2.imwrite('image.png', image)

    # crop image according to rects and upload to 'conversationName' folder,
    # with names of images as '1_sender', '2_receiver'
    with tempfile.TemporaryDirectory() as tmpdirname:
        for i in range(len(rects)):
            x, y, w, h = rects[i]
            cropped_image_name = (
                str(i) + str(receiverName if x == 0 else senderName) + PNG_EXTENSION
            )
            cv2.imwrite(
                os.path.join(tmpdirname, cropped_image_name),
                image[y : y + h, x : x + w],
            )
            upload_to_bucket(
                os.path.join(tmpdirname, cropped_image_name),
                os.path.join(conversationName, cropped_image_name),
            )
