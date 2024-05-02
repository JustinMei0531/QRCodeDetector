import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import qrcode
import pandas as pd


area_df: pd.DataFrame = pd.DataFrame(columns=["outerArea", "midArea", "innerArea"])



def showImage(image: np.ndarray, title=None) -> None:
    plt.imshow(image)
    plt.axis("off")
    plt.title(title)
    plt.show()
    return

def findChildrenContours(contour_index, hierarchy, all_contours):
    children_contours = []
    print(type(hierarchy), type(all_contours))
    # Iterate through hierarchy to find children contours of the given contour
    for i, hier in enumerate(hierarchy[0]):
        # Check if the current contour's parent index matches the given contour's index
        if hier[3] == contour_index:
            # Add the child contour to the list
            children_contours.append(all_contours[i])
            # Recursively find children contours of the current contour
            children_contours.extend(findChildrenContours(i, hierarchy, all_contours))
    return children_contours


def getRelativeArea(image: np.ndarray) -> list:
    point_info: list = []
    
    grey: np.ndarray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thres = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel: np.ndarray = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    canny: np.ndarray = cv2.Canny(thres, 200, 255)
    morph = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        children_contours = findChildrenContours(i, hierarchy, contours)
        if len(children_contours) == 4:
            rect = cv2.minAreaRect(contours[i])
            
            (x, y), (w, h), angle = rect
            # x, y, w, h = cv2.boundingRect(contours[i])
            point_info.append(((x - w / 2, y - h / 2, w, h), children_contours))
            
    return point_info

def getPositionAngle(point_info: list) -> list:
    position_angles: list = []
    for (x, y, w, h), children_contours in point_info:
        outer_contour_area: float = float(w * h)
        (_x, _y), (_w, _h), angle = cv2.minAreaRect(children_contours[1])
        mid_contour_area: float = float(_w * _h)
        (_x, _y), (_w, _h), angle = cv2.minAreaRect(children_contours[3])
        inner_contour_area: float = float(_w * _h)

        
        ratio1: float = outer_contour_area / mid_contour_area
        ratio2: float = outer_contour_area / inner_contour_area
        ratio3: float = mid_contour_area / inner_contour_area
        print(ratio1, ratio2, ratio3)
        if ratio3 > 2.50 and ratio3 < 3.00 and ratio1 > 1.90 and ratio1 < 2.30:
            # Only add the outer contour infomation to the list.
            position_angles.append((x, y, w, h))
    print('*' * 50)
    return position_angles


if __name__ == "__main__":
    # img: np.ndarray = cv2.imread("./images/code2.jpeg", cv2.IMREAD_COLOR)
    # point_info = getRelativeArea(img)
    # position_angle = getPositionAngle(point_info)
    # print(position_angle)
    # for (x, y, w, h) in position_angle:
    #     img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), thickness=3)
    # showImage(img)
    # print(area_df)

    for i in range(1, 50):
        img: np.ndarray = cv2.imread("./images/qrcode{}.png".format(i), cv2.IMREAD_COLOR)
        point_info = getRelativeArea(img)
        position_angle = getPositionAngle(point_info)
        
        for (x, y, w, h) in position_angle:
            x, y, w, h = int(x), int(y), int(w), int(h)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), thickness=3)
        showImage(img, title="qrcode{}.png".format(i))

# 2.03 5.67 2.78
# 2.03 5.50 2.69
# 2.14 5.56 2.59
# 2.34 6.38 2.72
# 