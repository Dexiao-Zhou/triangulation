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
        cv2.putText(img, f"{contour_info['shape']}", (x, y),0.5, color, 2)

        # 选择性地展示处理后的图像
        cv2.drawContours(img, [cnt], 0, color, 2)  # 在原图上标记轮廓
        cv2.imshow("Contours Detected", img)
        cv2.waitKey(1)
        # cv2.destroyAllWindows()

    return contours_info

def process_images_in_folder(folder_path, csv_file_path):
    # 检查CSV文件是否已存在，以决定是否需要写入头部
    file_exists = os.path.isfile(csv_file_path)

    with open(csv_file_path, 'a', newline='') as csvfile:
        fieldnames = ['image', 'shape', 'length', 'point_x', 'point_y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        
        filenames = sorted(os.listdir(folder_path))  # 这里添加了排序
        for filename in filenames:
            if filename.endswith(".jpg"):  # 检查文件扩展名
                image_path = os.path.join(folder_path, filename)
                contours_info = detect_shapes(image_path)
                
                for contour_info in contours_info:
                    shape = contour_info['shape']
                    length = contour_info['length']
                    coordinates = contour_info['coordinates']
                    
                    # for point in contour_info['coordinates']:
                    #     x, y = point[0], point[1]  # 假设每个坐标是一个包含两个元素的列表或元组
                    #     writer.writerow({'image': filename, 'shape': shape, 'length': length, 'point_x': x, 'point_y': y})

# 调用函数
# image_path = '/Users/zhoudexiao/Downloads/triangulation/frames 4/frame_00000.jpg'  # 替换为你的图片路径
# contours_info = detect_shapes(image_path)

# # print一下当前的图片的数据信息
# for contour in contours_info:
#     print(contour)


folder_path = '/Users/zhoudexiao/Downloads/triangulation/frames 3'  # 更新为你的文件夹路径
csv_file_path = '/Users/zhoudexiao/Downloads/triangulation/frames 3/shapes_data.csv'
process_images_in_folder(folder_path, csv_file_path)