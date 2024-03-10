import cv2
import numpy as np


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

        if contour_info['length'] < 1000:
            contour_info['coordinates'] = approx.tolist()  # 将坐标转换为列表形式
        else:
            continue

        contours_info.append(contour_info)  # 添加轮廓信息到列表

        # 标记识别出的形状
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        cv2.putText(img, f"{contour_info['shape']}:", (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)

        # 选择性地展示处理后的图像
        cv2.drawContours(img, [cnt], 0, color, 2)  # 在原图上标记轮廓
        cv2.imshow("Contours Detected", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return contours_info

# 调用函数
image_path = '/Users/zhoudexiao/Downloads/triangulation/frames 6/frame_00000.jpg'  # 替换为你的图片路径
contours_info = detect_shapes(image_path)

for contour in contours_info:
    print(contour)
