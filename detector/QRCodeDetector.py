import cv2
import numpy as np
from utils.util import showImage, vctDotProduct

class QRCodeDetector:
    def __init__(self, img_path: str) -> None:
        self.__image: np.ndarray = cv2.imread(img_path, cv2.IMREAD_COLOR)
        self.__image_copy = self.__image.copy()
        self.__point_info: list = []
        self.__position_angles: list = []
        self.__is_sorted = False
        self.__preprocess()
        self.__getRelativeArea()
        self.__getPositionAngle()

    def __findChildrenContours(self, index: int, hierarchy: np.ndarray, all_contours: tuple) ->list:
        children_contours: list = []
        # Iterate through hierarchy to find children contours of the given contour
        for i, hier in enumerate(hierarchy[0]):
            # Check if the current contour's parent index matches the given contour's index
            if hier[3] == index:
                # Add the child contour to the list
                children_contours.append(all_contours[i])
                # Recursively find children contours of the current contour
                children_contours.extend(self.__findChildrenContours(i, hierarchy, all_contours))
        return children_contours


    def __preprocess(self) -> None:
        # Convert image to grayscale
        gray: np.ndarray = cv2.cvtColor(self.__image, cv2.COLOR_BGRA2GRAY)
        # Binarize grayscale images
        _, thres = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        kernel: np.ndarray = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # Edge detection
        canny: np.ndarray = cv2.Canny(thres, 200, 255)
        # Morphology operation
        self.__image : np.ndarray = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=1)
        return
    
    def __getRelativeArea(self) -> None:
        contours, hierarchy = cv2.findContours(self.__image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for i in range(len(contours)):
            children_contours: list = self.__findChildrenContours(i, hierarchy, contours)
            if len(children_contours) == 4:
                rect: cv2.typing.RotatedRect = cv2.minAreaRect(contours[i])
                (x, y), (w, h), angle = rect
                self.__point_info.append(((x, y, w, h), children_contours))
        return
    
    def __getPositionAngle(self) -> None:
        for (x, y, w, h), children_contours in self.__point_info:
            outer_contour_area: float = float(w * h)
            (_x, _y), (_w, _h), angle = cv2.minAreaRect(children_contours[1])
            mid_contour_area: float = float(_w * _h)
            (_x, _y), (_w, _h), angle = cv2.minAreaRect(children_contours[3])
            inner_contour_area: float = float(_w * _h)

            if outer_contour_area == 0 or mid_contour_area == 0 or inner_contour_area == 0:
                return
            ratio1: float = outer_contour_area / mid_contour_area
            ratio2: float = outer_contour_area / inner_contour_area
            ratio3: float = mid_contour_area / inner_contour_area
            # print(ratio1, ratio2, ratio3)
            if 1.90 < ratio1 < 2.30 and 2.45 < ratio3 < 3.00:
                self.__position_angles.append((x, y, w, h))

    def getImage(self) -> np.ndarray:
        return self.__image.copy()
    
    
    def markQRCode(self, line_color=(0, 0, 255)) -> np.ndarray:
        if len(self.__position_angles) < 3:
            return self.__image_copy.copy()
        if self.__is_sorted == False:
            self.__position_angles.sort()
            self.__is_sorted = True
        for i in range(0, len(self.__position_angles) - 2, 3):
            x1, x2, _, _ = self.__position_angles[i]
            x3, x4, _, _ = self.__position_angles[i + 1]
            x5, x6, _, _ = self.__position_angles[i + 2]
            self.__image_copy: np.ndarray = cv2.line(self.__image_copy, (int(x1), int(x2)), (int(x3), int(x4)), line_color, thickness=2)
            self.__image_copy: np.ndarray = cv2.line(self.__image_copy, (int(x1), int(x2)), (int(x5), int(x6)), line_color, thickness=2)
            self.__image_copy: np.ndarray = cv2.line(self.__image_copy, (int(x3), int(x4)), (int(x5), int(x6)), line_color, thickness=2)
        
        return self.__image_copy.copy()


