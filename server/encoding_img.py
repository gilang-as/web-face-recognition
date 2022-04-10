import base64
import numpy as np
import cv2


# Encoding base 64
def encodingImage(image):
    (flag, imJpg) = cv2.imencode(".jpg", image)
    image_encoding = base64.b64encode(imJpg).decode('utf-8')
    return image_encoding


def decodingImage(image_encoding):
    # base64--> bytes
    image_encoding = base64.b64decode(image_encoding.encode('utf-8'))
    # bytes --> jpg
    decoByte = np.frombuffer(image_encoding, dtype=np.uint8)
    # Jpg --> unit8
    decoJpg = cv2.imdecode(decoByte, cv2.IMREAD_COLOR)
    return decoJpg
