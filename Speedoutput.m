clc
clear
close all
speeds = readtable('SpeedData.csv');
speeds = table2array(speeds)/5.5;

speeds_real = readtable('x-velocity_real.csv');
speeds_real = table2array(speeds_real(:,3));
speeds_real = str2double(speeds_real);
speeds_real = abs(speeds_real)/10000;

% 定义移动平均滤波器参数
window_size = 40; % 窗口大小
% 应用移动平均滤波器
filtered_speeds = movmean(speeds, window_size);

% 定义移动平均滤波器参数
window_size = 20; % 窗口大小
% 应用移动平均滤波器
filtered_speeds = movmean(filtered_speeds, window_size);


time1 = linspace(0, 10, length(speeds));
time2 = linspace(0, 10, length(speeds_real));

% % Butterworth 滤波器
% order = 4;
% cutoff_frequency = 10; % 截止频率，根据你的需求调整
% % 假设采样频率为 Fs，根据您的实际情况进行修改
% Fs = 1000; % 例如，假设采样频率为 1000 Hz
% 
% [b, a] = butter(order, cutoff_frequency/(Fs/2), 'low');

% % 应用滤波器
% filtered_speeds = filter(b, a, speeds);

% 绘制原始信号和滤波后的信号
figure;
subplot(2,1,1);
hold on;
plot(time1, speeds(:,2), 'b', 'LineWidth', 1.5);
plot(time1, filtered_speeds(:,2), 'r','LineWidth', 3)
legend('speeds compute through video', 'filtered speeds');
xlabel('time');
ylabel('amplitude');
grid on;


subplot(2,1,2);
hold on;

plot(time2,speeds_real)
legend('real speeds');
xlabel('time');
ylabel('amplitude');
grid on;