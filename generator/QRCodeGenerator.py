import qrcode
import os
import cv2
import numpy as np
import time
import hashlib
from random import randint

class QRCodeGenerator:
    def __init__(self, max_length=32) -> None:
        self.max_length = max_length
        
    def generate(self, n = 5, fgColor=(0, 0, 0), bgColor=(255, 255, 255), rotate=False) -> None:
        if n <= 0:
            n = 5
        if not os.path.exists("./images"):
            os.mkdir("./images")
        for _ in range(n):
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=15, border=3)
            cur_time = time.time()
            hash_code = hashlib.md5(str(cur_time).encode("utf-8")).hexdigest()[:self.max_length]
            qr.add_data(hash_code)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color=fgColor, back_color=bgColor)
            qr_img = qr_img.convert("RGB")  # Convert to RGB mode for compatibility with OpenCV
            qr_array = cv2.cvtColor(np.array(qr_img), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV
            h, w, c = qr_array.shape
            if rotate == True:
                angle: float = float(randint(-15, 15))
                matrix: np.ndarray = cv2.getRotationMatrix2D((w / 2, h / 2), angle=angle, scale=1.0)
                qr_array = cv2.warpAffine(qr_array, matrix, (w, h))
            cv2.imwrite("./images/qrcode{}.png".format(_ + 1), qr_array)
        
        return
    
if __name__ == "__main__":
    generator = QRCodeGenerator(24)
    generator.generate(5, (123, 253, 97), (123, 123, 123), True)
        