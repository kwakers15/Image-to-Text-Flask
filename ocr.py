from s3 import get_dir_names, get_all_images
import cv2
import pytesseract
import numpy as np
import tempfile
from Messages import Messages
import os
import functools


def compare(x, y):
    return int(x.split("_")[0]) - int(y.split("_")[0])


def get_convos():
    convos = []
    conversationNames = get_dir_names()
    for name in conversationNames:
        with tempfile.TemporaryDirectory() as tmpdirname:
            senderName, receiverName = get_all_images(name, tmpdirname)
            messages = Messages(name, senderName, receiverName)
            sortedImgs = sorted(
                os.listdir(tmpdirname),
                key=functools.cmp_to_key(compare),
            )
            for imgName in sortedImgs:
                img = cv2.imread(
                    os.path.join(tmpdirname, imgName), cv2.IMREAD_GRAYSCALE
                )
                img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)[1]
                custom_config = r"-l eng+kor --psm 6"
                read_str = pytesseract.image_to_string(
                    img, config=custom_config
                ).replace("\n\n", "\n")
                messages.addMessage(read_str, senderName in imgName)
        convos.append(messages)
    return convos
