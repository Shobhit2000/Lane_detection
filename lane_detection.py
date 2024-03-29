import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    height = image.shape[0]
    #height = height-50
    triangle = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, triangle, 255)
    masked = cv2.bitwise_and(mask, image)
    return masked

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope= parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_average = np.average(left_fit, axis=0)
    right_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_average)
    right_line = make_coordinates(image, right_average)
    return np.array([left_line, right_line])

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

img = cv2.imread('test_image.jpg')
lane_image= np.copy(img)

#canny_image = canny(lane_image)
#masks = region_of_interest(canny_image)
#lines = cv2.HoughLinesP(masks, 2, np.pi/180, 100, np.array([]), minLineLength= 40, maxLineGap= 5)
#averaged_lines= average_slope_intercept(lane_image, lines)
#line_image = display_lines(lane_image, averaged_lines)
#final_image= cv2.addWeighted(lane_image, 0.9, line_image, 1, 1)
#cv2.imshow("result", final_image)
#cv2.waitKey(0)

cap= cv2.VideoCapture('test2.mp4')
while (cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    masks = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(masks, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    final_image = cv2.addWeighted(frame, 0.9, line_image, 1, 1)
    cv2.imshow("result", final_image)
    cv2.waitKey(1)