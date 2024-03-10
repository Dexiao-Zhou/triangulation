import cv2
import os

def video_to_frames(video_path, frames_dir):
    # 确保保存帧的目录存在
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)

    # 加载视频
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    while True:
        # 逐帧读取视频
        success, frame = cap.read()
        if not success:
            break  # 如果没有帧了，就结束循环

        # 构建保存帧的路径
        frame_path = os.path.join(frames_dir, f"frame_{frame_count:05d}.jpg")
        # 保存帧为图片
        cv2.imwrite(frame_path, frame)
        frame_count += 1

    # 释放视频资源
    cap.release()
    print(f"Total frames extracted: {frame_count}")

# camera 3
video_path_3 = '/Users/zhoudexiao/Downloads/triangulation/camera 3.mp4'  # 视频文件路径
frames_dir_3 = 'frames 3'  # 保存帧的目录
video_to_frames(video_path_3, frames_dir_3)

# camera 4
video_path_4 = '/Users/zhoudexiao/Downloads/triangulation/camera 4.mp4'  # 视频文件路径
frames_dir_4 = 'frames 4'  # 保存帧的目录
video_to_frames(video_path_4, frames_dir_4)

# camera 5
video_path_5 = '/Users/zhoudexiao/Downloads/triangulation/camera 5.mp4'  # 视频文件路径
frames_dir_5 = 'frames 5'  # 保存帧的目录
video_to_frames(video_path_5, frames_dir_5)

# camera 6
video_path_6 = '/Users/zhoudexiao/Downloads/triangulation/camera 6.mp4'  # 视频文件路径
frames_dir_6 = 'frames 6'  # 保存帧的目录
video_to_frames(video_path_6, frames_dir_6)