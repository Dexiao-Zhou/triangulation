import cv2
import numpy as np
import csv
import os

def detect_shapes(image_path):
    # 读取图片
    img = cv2.imread(image_path)
    # 转换为灰度图
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 设定黑色的阈值范围
    lower = np.array([0, 0, 0])
    upper = np.array([10, 10, 10])

    # 找到阈值内的颜色
    mask = cv2.inRange(img, lower, upper)
    # 对掩码应用滤波以平滑处理
    smooth_mask = cv2.medianBlur(mask, 3)

    # 显示结果
    # cv2.imshow('Color-based Binary Image', smooth_mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # 二值化
    # _, thresh = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY_INV)

    # 寻找轮廓
    contours, _ = cv2.findContours(smooth_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_info = []  # 用于存储所有轮廓的坐标信息
    for cnt in contours:
        # 轮廓近似
        epsilon = 0.05 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        contour_info = {'shape': '', 'length': 0, 'coordinates': []}
        # 根据边角的数量识别形状
        if len(approx) == 3:
            shape_name = "Triangle"
            color = (0, 255, 0)  # 三角形，用绿色标记
            contour_info['shape'] = "Triangle"
        elif len(approx) == 4:
            shape_name = "Rectangle"
            color = (0, 0, 255)  # 矩形，用红色标记
            contour_info['shape'] = "Rectangle"
        else:
            continue  # 如果不是三角形或矩形，则跳过

        contour_info['length'] = cv2.arcLength(cnt, True)

        if contour_info['length'] < 1000 and contour_info['length'] > 100:
            contour_info['coordinates'] = approx.tolist()  # 将坐标转换为列表形式
        else:
            continue

        contours_info.append(contour_info)  # 添加轮廓信息到列表

        # 标记识别出的形状
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        cv2.putText(img, f"{contour_info['shape']}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # 选择性地展示处理后的图像
        cv2.drawContours(img, [cnt], 0, color, 2)  # 在原图上标记轮廓
        cv2.imshow("Contours Detected", img)
        cv2.waitKey(1)
        # cv2.destroyAllWindows()

    return contours_info

def generate_csv_headers(max_points):
    # 动态生成列标题
    fieldnames = ['image', 'shape', 'length']
    for i in range(max_points):
        fieldnames.extend([f'point_{i+1}_x', f'point_{i+1}_y'])
    return fieldnames

def process_images_in_folder(folder_path, csv_file_path):
    max_points = 0
    data = []

    # 预处理：遍历所有图像，收集形状信息和最大点数
    filenames = sorted(os.listdir(folder_path))
    for filename in filenames:
        if filename.endswith(".jpg"):
            image_path = os.path.join(folder_path, filename)
            contours_info = detect_shapes(image_path)
            for contour_info in contours_info:
                max_points = max(max_points, len(contour_info['coordinates']))
                data.append((filename, contour_info))

    # 生成列标题
    fieldnames = generate_csv_headers(max_points)

    # 写入CSV文件
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # 写入数据
        for filename, contour_info in data:
            row_dict = {
                'image': filename,
                'shape': contour_info['shape'],
                'length': contour_info['length']
            }
            for i, point in enumerate(contour_info['coordinates']):
                row_dict[f'point_{i+1}_x'] = point[0][0]
                row_dict[f'point_{i+1}_y'] = point[0][1]
            writer.writerow(row_dict)

# 调用函数
# image_path = '/Users/zhoudexiao/Downloads/triangulation/frames 4/frame_00000.jpg'  # 替换为你的图片路径
# contours_info = detect_shapes(image_path)

# # print一下当前的图片的数据信息
# for contour in contours_info:
#     print(contour)


folder_path_3 = '/Users/zhoudexiao/Desktop/Project/triangulation/frames 3'  # 更新为你的文件夹路径
csv_file_path_3 = '/Users/zhoudexiao/Desktop/Project/triangulation/frames 3/shapes_data.csv'
process_images_in_folder(folder_path_3, csv_file_path_3)

# folder_path_4 = '/Users/zhoudexiao/Downloads/triangulation/frames 4'  # 更新为你的文件夹路径
# csv_file_path_4 = '/Users/zhoudexiao/Downloads/triangulation/frames 4/shapes_data.csv'
# process_images_in_folder(folder_path_4, csv_file_path_4)

# folder_path_5 = '/Users/zhoudexiao/Downloads/triangulation/frames 5'  # 更新为你的文件夹路径
# csv_file_path_5 = '/Users/zhoudexiao/Downloads/triangulation/frames 5/shapes_data.csv'
# process_images_in_folder(folder_path_5, csv_file_path_5)

# folder_path_6 = '/Users/zhoudexiao/Downloads/triangulation/frames 6'  # 更新为你的文件夹路径
# csv_file_path_6 = '/Users/zhoudexiao/Downloads/triangulation/frames 6/shapes_data.csv'
# process_images_in_folder(folder_path_6, csv_file_path_6)
