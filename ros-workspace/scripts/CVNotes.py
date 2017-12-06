import cv2
import numpy as np
from itertools import product

def detect_notes_helper(blur, image_name='notes2.jpg'):
    """
    Uses OpenCV to detect notes from an image to return positions
    :param image_name:
    :return: (list of note frequencies, list of note positions with range 0 to 8))
    """

    # ==================================================================================================================
    # Config
    # ==================================================================================================================
    note_head_pixel_size = 1
    frequencies = [349.2282, 329.6276, 293.6648, 261.6256, 246.9417, 220.0000, 195.9977, 174.6141, 164.8138, ]

    # ==================================================================================================================
    # Read Image
    # ==================================================================================================================
    img_notes_color = cv2.imread(image_name)
    img_notes = cv2.imread(image_name, 0)
    clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(50,50))
    img_notes = clahe.apply(img_notes)
    show(img_notes)

    # ==================================================================================================================
    # Line detections and staff line removal
    # ==================================================================================================================
    edges = cv2.Canny(img_notes, 50, 150, apertureSize=3)
    line_groups = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    ledger_lines = list()
    line_width = img_notes.shape[1] * 0.95

    # Prepares image for blob detection
    for group in line_groups:
        # 10 segments instead of just 5: because HoughLines returns a duplicate line for each one we want.
        for lineI in range(0, 10):
            rho, theta = group[lineI]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x_start = int(x0 + line_width * -b)
            y_start = int(y0 + line_width * a)
            x_end = int(x0 - line_width * -b)
            y_end = int(y0 - line_width * a)
            ledger_lines.append((x_start, x_end, y_start, y_end))

            # Along each line, erase (paint a white circle) parts that ha
            (x_displacement, y_displacement) = (x_end - x_start, y_end - y_start)
            for percent in np.arange(0.0, 1.0, 1 / 1000.0):
                x_eraser = x_start + int(x_displacement * percent)
                y_eraser = y_start + int(y_displacement * percent)

                pixel_top_bot = [img_notes[y_eraser + offset, x_eraser] for offset in [-6, 6]]
                non_white_pixels = [pixel for pixel in pixel_top_bot if not(pixel > 254)]
                if len(non_white_pixels) == 0:
                    # I change size from 6 to 5 to make it cleaner
                    cv2.circle(img_notes, (x_eraser, y_eraser), 5, (255, 0, 0), -1)

    # Check no-line image here:
    show(img_notes)

    # Combine lines by averaging the end points of pairs of nearby lines
    ledger_lines.sort(key=lambda x: (x[2] + x[3]) / 2)
    real_ledger_lines = list()
    for i in range(0, 10, 2):
        element = list()
        line_1 = ledger_lines[i]
        line_2 = ledger_lines[i + 1]
        for coord_idx in range(0, 4):
            element.append((line_1[coord_idx] + line_2[coord_idx]) / 2)
        real_ledger_lines.append(element)

    for i in real_ledger_lines:
        cv2.line(img_notes_color, (i[0], i[2]), (i[1], i[3]), (0, 0, 255), 1)

    # ==================================================================================================================
    # Find pixel positions (keypoints) using blob detection
    # ==================================================================================================================

    # Blur the image
    kernel = np.ones((blur, blur), np.float32) / (blur * blur)
    img_notes = cv2.filter2D(img_notes, -1, kernel)
    print "shoing notes"
    show(img_notes)

    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.filterByInertia = True
    params.filterByConvexity = True
    params.minArea = 8
    params.minInertiaRatio = 0.35
    params.minConvexity = .965

    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3:
        detector = cv2.SimpleBlobDetector(params)
    else:
        detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(img_notes)
    keypoints = filter(lambda x: x.size > note_head_pixel_size, keypoints)
    keypoints.sort(key=lambda x: x.pt[0])

    # ==================================================================================================================
    # Find note positions by computing threshold positions and finding position that coresponds with the threshold
    # that is the closest to a keypoint. Finally, map it to a relevant note frequency.
    # ==================================================================================================================

    tones = list()
    positions = list()

    for kPoint in keypoints:
        (note_x, note_y) = (kPoint.pt[0], kPoint.pt[1])

        cv2.circle(img_notes_color, (int(note_x), int(note_y)), 3, (255, 255, 0), -1)

        thresholds = list()
        for line in real_ledger_lines:
            (x0, x1, y0, y1) = tuple(line)
            slope = 1.0 * (y1 - y0) / (x1 - x0)
            # In case images that are rotated, add the effect of the slope of the staff line to calculate thresholds
            thresh = y0 + slope * (note_x - x0)
            thresholds.append(thresh)
        thresholds.sort()

        # Positions between the staff lines
        for i in range(0, len(thresholds) - 1):
            thresholds.append((thresholds[i] + thresholds[i + 1]) / 2)
        thresholds.sort()

        for i in range(0, len(thresholds)):
            cv2.circle(img_notes_color, (int(note_x), int(thresholds[i])), 2, (255, 0, 13 * i), -1)

        dists = map(lambda x: abs(x - note_y), thresholds)
        note_pos = np.argmin(dists)
        positions.append(note_pos)
        tones.append(frequencies[note_pos])

    show(img_notes_color)
    return tones, positions


def show(to_show):
    cv2.imshow("Results", to_show)
    cv2.waitKey(0)


def detect_notes(image_name='notes2.png'):
    # 27
    return detect_notes_helper(5, image_name)

detect_notes()

# for b in range(5, 70):
#     correct_for_notes2 = [5, 4, 3, 5, 4, 3, 5, 3, 4, 5, 7, 3, 4, 5, 6]
#     (one, two) = detect_notes_helper(b, "notes2.png")
#     # num_matches = 0
#     # for note_i in range(len(correct_for_notes2)):
#     #     if note_i < len(two):
#     #         if correct_for_notes2[note_i] == two[note_i]:
#     #             num_matches += 1
#     #     else:
#     #         break
#     # print "{} found for blur of {}".format(len(two), b)
#     print "{}".format(len(two))



