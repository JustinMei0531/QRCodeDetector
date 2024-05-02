import numpy as np
import cv2
import matplotlib.pyplot as plt


def showImage(image: np.ndarray, title=None) -> None:
    plt.imshow(image)
    plt.axis("off")
    plt.title(title)
    plt.show()


def vctDotProduct(startPoint: tuple, endPoint1: tuple, endPoint2: tuple) -> float:
    x1, x2 = startPoint
    x3, x4 = endPoint1
    x5, x6 = endPoint2

    return (x3 - x1) * (x5 - x1) + (x4 - x2) * (x6 - x2)