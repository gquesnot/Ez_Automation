import cv2
import numpy as np

from util.hswfilter import HsvFilter
from util.json_function import apply_json_config


class Vision:
    # constants
    HSV_TRACKBAR = "HSV Trackbar"
    CANNY_BLUR_TRACKBAR = "CannyBlur Trackbar"
    MASK_TRACKBAR = "Mask Trackbar"

    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None
    h_min = {}
    s_min = {}
    v_min = {}
    h_max = {}
    s_max = {}
    s_add = {}
    s_sub = {}
    v_add = {}
    canny_on = {}
    canny_kernel = {}
    canny_ratio = {}
    low_threshold = {}
    max_threshold = {}
    blur_on = {}
    blur_kernel = {}
    blur_ratio = {}
    R = {}
    G = {}
    B = {}

    # constructor
    def __init__(self, hsv=True, method=cv2.TM_CCOEFF_NORMED):
        self.hsv_filter = HsvFilter()
        self.track_list_elem = apply_json_config(self, "vision")
        # load the image we're trying to match
        # https://docs.opencv2.org/4.2.0/d4/da8/group__imgcodecs.html

        # Save the dimensions of the needle image
        # self.needle_w = self.needle_img.shape[1]
        # self.needle_h = self.needle_img.shape[0]
        self.hsv = hsv
        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def find(self, haystack_img, threshold=0.5, max_results=10):
        # run the OpenCV2 algorithm
        result = cv2.matchTemplate(haystack_img, self.needle_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        # print(locations)

        # if we found no results, return now. this reshape of the empty array allows us to
        # concatenate together results without causing an error
        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

        # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
        # locations by using groupRectangles().
        # First we need to create the list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        # print(rectangles)

        # for performance reasons, return a limited number of results.
        # these aren't necessarily the best results.
        if len(rectangles) > max_results:
            print('Warning: too many results, raise the threshold.')
            rectangles = rectangles[:max_results]

        return rectangles

    # given a list of [x, y, w, h] rectangles returned by find(), convert those into a list of
    # [x, y] positions in the center of those rectangles where we can click on those found items
    def get_click_points(self, rectangles):
        points = []

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:
            # Determine the center position
            center_x = x + int(w / 2)
            center_y = y + int(h / 2)
            # Save the points
            points.append((center_x, center_y))

        return points

    # given a list of [x, y, w, h] rectangles and a canvas image to draw on, return an image with
    # all of those rectangles drawn
    def draw_rectangles(self, haystack_img, rectangles):
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv2.LINE_4

        for (x, y, w, h) in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv2.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img

    # given a list of [x, y] positions and a canvas image to draw on, return an image with all
    # of those click points drawn on as crosshairs
    def draw_crosshairs(self, haystack_img, points):
        # these colors are actually BGR
        marker_color = (255, 0, 255)
        marker_type = cv2.MARKER_CROSS

        for (center_x, center_y) in points:
            # draw the center point
            cv2.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        return haystack_img

    # create gui window with controls for adjusting arguments in real-time
    def init_control_gui(self):
        cv2.namedWindow(self.HSV_TRACKBAR, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.HSV_TRACKBAR, 450, 300)
        cv2.moveWindow(self.HSV_TRACKBAR, 0, 0)
        cv2.namedWindow(self.CANNY_BLUR_TRACKBAR, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.CANNY_BLUR_TRACKBAR, 450, 250)
        cv2.moveWindow(self.CANNY_BLUR_TRACKBAR, 0, 500)
        cv2.namedWindow(self.MASK_TRACKBAR, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.MASK_TRACKBAR, 450, 200)
        cv2.moveWindow(self.MASK_TRACKBAR, 0, 950)

        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.

        def nothing():
            pass

        # create trackbars for bracketing.
        # OpenCV2 scale for HSV is H: 0-179, S: 0-255, V: 0-255
        for elem_name in self.track_list_elem:
            elem = getattr(self, elem_name)
            cv2.createTrackbar(elem_name, elem['trackbarName'], elem['min'], elem['max'], nothing)
            cv2.setTrackbarPos(elem_name, elem['trackbarName'], elem['value'])

    # returns an HSV filter object based on the control GUI values
    def update_filter(self):

        # Get current positions of all trackbars
        # print(self.hsv_filter.__dict__)
        for elem_name in self.track_list_elem:
            elem = getattr(self, elem_name)
            elem['value'] = cv2.getTrackbarPos(elem_name, elem['trackbarName'])

    def get_hsv_filter(self):
        result = {}
        for elem_name in self.track_list_elem:
            elem = getattr(self, elem_name)
            result[elem_name] = elem['value']
        self.hsv_filter = HsvFilter(datas=result)
        return self.hsv_filter

    # given an image and an HSV filter, apply the filter and return the resulting image.
    # if a filter is not supplied, the control GUI trackbars will be used
    def apply_hsv_filter(self, original_image, hsv_filter=None):
        # convert image to HSV
        if self.hsv:
            hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)  #
        else:
            hsv = original_image

        # if we haven't been given a defined filter, use the filter values from the GUI
        if not hsv_filter:
            self.update_filter()
            hsv_filter = self.get_hsv_filter()

        # add/subtract saturation and value
        h, s, v = cv2.split(hsv)
        s = self.shift_channel(s, hsv_filter.SAdd)
        s = self.shift_channel(s, -hsv_filter.SSub)
        v = self.shift_channel(v, hsv_filter.VAdd)
        v = self.shift_channel(v, -hsv_filter.VSub)
        hsv = cv2.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.HMin, hsv_filter.SMin, hsv_filter.VMin])
        upper = np.array([hsv_filter.HMax, hsv_filter.SMax, hsv_filter.VMax])
        # Apply the thresholds
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        if self.hsv:
            img = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
        else:
            img = result
        if hsv_filter.BlurOn == 1:
            img = cv2.bilateralFilter(img, hsv_filter.BlurRatio, hsv_filter.BlurKernel, hsv_filter.BlurKernel)
        if hsv_filter.CannyOn == 1:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.Canny(img, hsv_filter.LowThreshold, hsv_filter.MaxThreshold, hsv_filter.CannyKernel)
        return img

    # apply adjustments to an HSV channel
    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c

    def centeroid(self, point_list):
        point_list = np.asarray(point_list, dtype=np.int32)
        length = point_list.shape[0]
        sum_x = np.sum(point_list[:, 0])
        sum_y = np.sum(point_list[:, 1])
        return [np.floor_divide(sum_x, length), np.floor_divide(sum_y, length)]
