from random import randint

import cv2  # python-opencv
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg

def x_rotation_mat(theta):
    return np.array([[1, 0, 0],
                      [0, np.cos(theta), -np.sin(theta)],
                      [0, np.sin(theta), np.cos(theta)]])

def y_rotation_mat(theta):
    return np.array([[np.cos(theta), 0, np.sin(theta)],
                     [0, 1, 0],
                     [-np.sin(theta), 0, np.cos(theta)]])


def DLT(P1, P2, point1, point2):
    A = [point1[1] * P1[2, :] - P1[1, :],
         P1[0, :] - point1[0] * P1[2, :],
         point2[1] * P2[2, :] - P2[1, :],
         P2[0, :] - point2[0] * P2[2, :]
         ]
    A = np.array(A).reshape((4, 4))
    B = A.transpose() @ A
    U, s, Vh = linalg.svd(B, full_matrices=False)
    return Vh[3, 0:3] / Vh[3, 3]


def get_lists_of_match_points():
    with open(r'matched_points\matchedPoints1.txt', 'r') as file:  # read match points
        match_points_1_text = file.read().replace(',', ' ')
    with open(r'matched_points\matchedPoints2.txt', 'r') as file:
        match_points_2_text = file.read().replace(',', ' ')
    match_points_1_list = list(match_points_1_text.split("\n"))  # convert to list of ints
    match_points_2_list = list(match_points_2_text.split("\n"))
    list_of_match_points_1 = []
    list_of_match_points_2 = []
    list_of_match_points_1_float = []
    list_of_match_points_2_float = []
    for points1, points2 in zip(match_points_1_list, match_points_2_list):
        if points1 != '':
            int_points_1 = tuple(int(float(el)) for el in points1.split(' '))
            list_of_match_points_1.append(int_points_1)
            float_points_1_f = tuple(float(el) for el in points1.split(' '))
            list_of_match_points_1_float.append(float_points_1_f)
        if points2 != '':
            int_points_2 = tuple(int(float(el)) for el in points2.split(' '))
            list_of_match_points_2.append(int_points_2)
            float_points_2_f = tuple(float(el) for el in points2.split(' '))
            list_of_match_points_2_float.append(float_points_2_f)
    return list_of_match_points_1, list_of_match_points_2, list_of_match_points_1_float, \
               list_of_match_points_2_float


def draw_line_on_image(list_of_match_points_1, list_of_match_points_2, image1, image2):
    for ind in range(len(list_of_match_points_1)):  # draw lines on images
        red = randint(50, 255)
        green = randint(50, 255)
        blue = randint(50, 255)
        if ind < len(list_of_match_points_1) - 1:
            cv2.line(image1, list_of_match_points_1[ind], list_of_match_points_1[ind + 1], (red, green, blue),
                     thickness=6)
            cv2.line(image2, list_of_match_points_2[ind], list_of_match_points_2[ind + 1], (red, green, blue),
                     thickness=6)
    return image1, image2


def get_camera_matrix_in_numpy():
    with open(r'camera_matrixes\cameraMatrix1.txt', 'r') as file:  # read match points
        camera_matrix_1_string = file.read().replace(',', ' ')
    with open(r'camera_matrixes\cameraMatrix2.txt', 'r') as file:
        camera_matrix_2_string = file.read().replace(',', ' ')
    cam_1_string_list = list(camera_matrix_1_string.split("\n"))
    cam_2_string_list = list(camera_matrix_2_string.split("\n"))
    cam_mat_1_list = []
    cam_mat_2_list = []
    for points1, points2 in zip(cam_1_string_list, cam_2_string_list):
        if points1 != '':
            float_points_1 = list(float(el) for el in points1.split(' '))
            cam_mat_1_list.append(float_points_1)
        if points2 != '':
            float_points_2 = list(float(el) for el in points2.split(' '))
            cam_mat_2_list.append(float_points_2)

    cam_mat_1 = np.array([cam_mat_1_list[0], cam_mat_1_list[1], cam_mat_1_list[2]])
    cam_mat_2 = np.array([cam_mat_2_list[0], cam_mat_2_list[1], cam_mat_2_list[2]])
    return cam_mat_1, cam_mat_2


def get_3d_point_array(list_of_match_points_1_float, list_of_match_points_2_float, cam_mat_1, cam_mat_2):
    three_d_points = []
    for point1, point2 in zip(list_of_match_points_1_float, list_of_match_points_2_float):
        point = DLT(cam_mat_1, cam_mat_2, point1, point2)
        three_d_points.append(point)
    return three_d_points


def get_average_vector(three_d_points):
    x_sum = y_sum = z_sum = 0
    len_points = len(three_d_points)
    for point in three_d_points:
        x_sum += point[0]
        y_sum += point[1]
        z_sum += point[2]
    ave_point = np.array([x_sum / len_points, y_sum / len_points, z_sum / len_points])
    return ave_point


def get_centered_xy_points(three_d_points, ave_point):
    array_of_x = []
    array_of_y = []
    list_of_xy_points = []
    for point in three_d_points:
        array_of_x.append((point[0] - ave_point[0]))
        array_of_y.append((point[1] - ave_point[1]))
        list_of_xy_points.append([(point[0] - ave_point[0]), (point[1] - ave_point[1])])
    return array_of_x, array_of_y, list_of_xy_points


def rotate_by_some_angle(three_d_points, angle, cos_mul, sin_mul):
    theta = np.radians(angle)  # random rotation
    if cos_mul == 1 and sin_mul == 1:
        c, s = np.cos(theta), np.sin(theta)
        rotation_mat = np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)))
    elif cos_mul == 1 and sin_mul == 0:
        rotation_mat = x_rotation_mat(angle)
    else:
        rotation_mat = y_rotation_mat(angle)
    for ind, point in enumerate(three_d_points):
        three_d_points[ind] = np.matmul(rotation_mat, point)
    return three_d_points

def create_model_image(array_of_x, array_of_y, image_index, present):
    fig1 = plt.gcf()
    plt.xlim([-4, 4])
    plt.ylim([-4, 4])
    plt.scatter(array_of_x, array_of_y)
    #plt.show()
    for ind in range(len(array_of_x)):
        if ind < len(array_of_x) - 1:
            x_values = [array_of_x[ind], array_of_x[ind + 1]]
            y_values = [array_of_y[ind], array_of_y[ind + 1]]
            plt.plot(x_values, y_values)
    if present == True:
        plt.show()
    path = 'gif_folder/image' + str(image_index) + '.jpg'
    fig1.savefig(path, dpi=100)
    plt.close(fig1)


# ---------- read images --------
image1 = cv2.imread(r'houses_images\house_1.png')
image2 = cv2.imread(r'houses_images\house_2.png')

# ---------- use given points to draw lines on two given images and plot the result --------
list_of_match_points_1, list_of_match_points_2, list_of_match_points_1_float, list_of_match_points_2_float = \
    get_lists_of_match_points()
image1_lines, image2_lines = draw_line_on_image(list_of_match_points_1, list_of_match_points_2, image1, image2)
plt.imshow(image1_lines)
plt.show()
plt.imshow(image2_lines)
plt.show()


# ---------- use given camera matrix and create an array of 3d points of on the given house model --------
cam_mat_1, cam_mat_2 = get_camera_matrix_in_numpy()
three_d_points = get_3d_point_array(list_of_match_points_1_float, list_of_match_points_2_float, cam_mat_1, cam_mat_2)

# ---------- center cloud of points and plot the result on the xy axis --------
ave_point = get_average_vector(three_d_points)
array_of_x, array_of_y, list_of_xy_points = get_centered_xy_points(three_d_points, ave_point)

# ---------- showing result of points on xy axis --------
plt.scatter(array_of_x, array_of_y)
plt.show()

# ---------- drawing lines between the points and plotting the result ----------
for ind in range(len(array_of_x)):
    if ind < len(array_of_x) - 1:
        x_values = [array_of_x[ind], array_of_x[ind + 1]]
        y_values = [array_of_y[ind], array_of_y[ind + 1]]
        plt.plot(x_values, y_values)
plt.show()

# ---------- rotate by random angle -----------
three_d_points = rotate_by_some_angle(three_d_points, randint(50, 255), 1, 1)

# ---------- peresent object after random rotation ----------
ave_point = get_average_vector(three_d_points)
array_of_x, array_of_y, list_of_xy_points = get_centered_xy_points(three_d_points, ave_point)
create_model_image(array_of_x, array_of_y, 100, present=True)

# perform rotations on the x-axis for 36 iterations and the same on the y-axis
# save the result in gif_folder

for angle in range(36):  # rotate by x
    rot_x = True
    rot_y = False
    three_d_points = rotate_by_some_angle(three_d_points, (np.pi * 2)/36, rot_x, rot_y)
    ave_point = get_average_vector(three_d_points)
    array_of_x, array_of_y, list_of_xy_points = get_centered_xy_points(three_d_points, ave_point)
    create_model_image(array_of_x, array_of_y, angle, present=False)

for angle in range(36):  # rotate by y
    rot_x = False
    rot_y = True
    three_d_points = rotate_by_some_angle(three_d_points, (np.pi * 2) / 36, rot_x, rot_y)
    ave_point = get_average_vector(three_d_points)
    array_of_x, array_of_y, list_of_xy_points = get_centered_xy_points(three_d_points, ave_point)
    create_model_image(array_of_x, array_of_y, angle + 36)


