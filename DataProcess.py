import csv

def classify_shapes(input_csv, output_csv_triangle, output_csv_rectangle):
    triangles = []
    rectangles = []

    # 步骤1: 读取原始数据
    with open(input_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过头部行（如果存在）
        for row in reader:
            shape_type = row[1]  # 假设形状类型在第二列
            if shape_type.lower() == 'triangle':
                triangles.append(row)
            elif shape_type.lower() == 'rectangle':
                rectangles.append(row)

    # 步骤2: 写入三角形数据
    with open(output_csv_triangle, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['image', 'Shape', 'length', 'point_1_x', 'point_1_y', 'point_2_x','point_2_y', 'point_3_x', 'point_3_y'])  # 示例头部，根据需要调整
        writer.writerows(triangles)

    # 步骤3: 写入四边形数据
    with open(output_csv_rectangle, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['image', 'Shape', 'length', 'point_1_x', 'point_1_y', 'point_2_x','point_2_y', 'point_3_x', 'point_3_y', 'point_4_x', 'point_4_y'])  # 示例头部，根据需要调整
        writer.writerows(rectangles)

# 调用函数
input_csv = '/Users/zhoudexiao/Desktop/Project/triangulation/frames 3/shapes_data.csv'  # 原始数据文件路径
output_csv_triangle = '/Users/zhoudexiao/Desktop/Project/triangulation/frames 3/triangles.csv'  # 分类后的三角形数据文件路径
output_csv_rectangle = '/Users/zhoudexiao/Desktop/Project/triangulation/frames 3/rectangles.csv'  # 分类后的四边形数据文件路径
classify_shapes(input_csv, output_csv_triangle, output_csv_rectangle)
