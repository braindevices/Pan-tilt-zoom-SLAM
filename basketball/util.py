"""
Other functions.

Create by Jimmy, 2018.9
"""

import math
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt


def overlap_pan_angle(fl_1, pan_1, fl_2, pan_2, im_width):
    """
    :param fl_1: focal length in pixel
    :param pan_1:  pan angle in degree
    :param fl_2:
    :param pan_2:
    :param im_width: image with in pixel
    :return: overlapped pan angle
    """
    # overlap angle (in degree) between two cameras

    w = im_width/2
    delta_angle = math.atan(w/fl_1) * 180.0/math.pi
    pan1_min = pan_1 - delta_angle
    pan1_max = pan_1 + delta_angle


    delta_angle = math.atan(w/fl_2) * 180.0/math.pi
    pan2_min = pan_2 - delta_angle
    pan2_max = pan_2 + delta_angle

    angle1 = max(pan1_min, pan2_min)
    angle2 = min(pan1_max, pan2_max)

    return max(0, angle2 - angle1)


def get_overlap_index(index1, index2):
    """
    This function get two arrays, and return the shared numbers in these two arrays as an new array.
    :param index1: array 1
    :param index2: array 2
    :return: overlapped numbers in two array
    """
    index1_overlap = np.ndarray([0], np.int8)
    index2_overlap = np.ndarray([0], np.int8)
    ptr1 = 0
    ptr2 = 0
    while ptr1 < len(index1) and ptr2 < len(index2):
        if index1[ptr1] == index2[ptr2]:
            index1_overlap = np.append(index1_overlap, ptr1)
            index2_overlap = np.append(index2_overlap, ptr2)
            ptr1 += 1
            ptr2 += 1
        elif index1[ptr1] < index2[ptr2]:
            ptr1 += 1
        elif index1[ptr1] > index2[ptr2]:
            ptr2 += 1
    return index1_overlap, index2_overlap


def add_gauss(points, var, max_width, max_height):
    """
    Add Gaussian noise to 2D points.
    :param points: array [N, 2]
    :param var: variance for Gauss distribution
    :return: array [N, 2] with noise
    """
    noise_points = np.zeros_like(points)
    for i in range(len(points)):
        noise_points[i, 0] = points[i, 0] + random.gauss(0, var)
        noise_points[i, 1] = points[i, 1] + random.gauss(0, var)

        if noise_points[i, 0] > max_width:
            noise_points[i, 0] = max_width

        if noise_points[i, 0] < 0:
            noise_points[i, 0] = 0

        if noise_points[i, 1] > max_height:
            noise_points[i, 1] = max_height

        if noise_points[i, 1] < 0:
            noise_points[i, 1] = 0

    return noise_points


def draw_camera_plot(ground_truth_pan, ground_truth_tilt, ground_truth_f,
                     estimate_pan, estimate_tilt, estimate_f):
    """
    draw plot for ground truth and estimated camera pose.
    """

    sequence_length = len(ground_truth_pan)

    plt.figure("pan percentage error")
    x = np.array([i for i in range(sequence_length)])
    plt.plot(x, (estimate_pan - ground_truth_pan) / ground_truth_pan * 100, 'b', label='predict')
    plt.xlabel("frame")
    plt.ylabel("error %")
    plt.legend(loc="best")

    plt.figure("tilt percentage error")
    x = np.array([i for i in range(sequence_length)])
    plt.plot(x, (estimate_tilt - ground_truth_tilt) / ground_truth_tilt * 100, 'b', label='predict')
    plt.xlabel("frame")
    plt.ylabel("error %")
    plt.legend(loc="best")

    plt.figure("f percentage error")
    x = np.array([i for i in range(sequence_length)])
    plt.plot(x, (estimate_f - ground_truth_f) / ground_truth_f * 100, 'b', label='predict')
    plt.xlabel("frame")
    plt.ylabel("error %")
    plt.legend(loc="best")

    """absolute value"""
    plt.figure("pan")
    x = np.array([i for i in range(sequence_length)])
    plt.plot(x, ground_truth_pan, 'r', label='ground truth')
    plt.plot(x, estimate_pan, 'b', label='predict')
    plt.xlabel("frame")
    plt.ylabel("pan angle")
    plt.legend(loc="best")

    plt.figure("tilt")
    x = np.array([i for i in range(sequence_length)])
    plt.plot(x, ground_truth_tilt, 'r', label='ground truth')
    plt.plot(x, estimate_tilt, 'b', label='predict')
    plt.xlabel("frame")
    plt.ylabel("tilt angle")
    plt.legend(loc="best")

    plt.figure("f")
    x = np.array([i for i in range(sequence_length)])
    plt.plot(x, ground_truth_f, 'r', label='ground truth')
    plt.plot(x, estimate_f, 'b', label='predict')
    plt.xlabel("frame")
    plt.ylabel("f")
    plt.legend(loc="best")

    plt.show()


def save_camera_pose(pan, tilt, f, path, file_name):
    """
    This function saves camera pose to .mat file.
    Assume the length of sequence is n.
    :param pan: an array [n] of pan angle
    :param tilt: an array [n] of tilt angle
    :param f: an array [n] of focal length
    :param path: folder path for mat file
    """
    camera_pose = dict()
    camera_pose['pan'] = pan
    camera_pose['tilt'] = tilt
    camera_pose['f'] = f

    print(path + '/' + file_name)

    sio.savemat(path + '/' + file_name, mdict=camera_pose)


def load_camera_pose(path):
    """
    :param path: file path for .mat
    :return: 3 arrays (pan, tilt, zoom) each of size [n]. (n is length of sequence)
    """
    camera_pos = sio.loadmat(path)
    pan = camera_pos['pan'].squeeze()
    tilt = camera_pos['tilt'].squeeze()
    f = camera_pos['f'].squeeze()

    return pan, tilt, f
