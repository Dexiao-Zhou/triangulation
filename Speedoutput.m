clc
clear
close all
speeds = readtable('SpeedData.csv');
speeds = table2array(speeds)/4;

speeds_real = readtable('x-velocity_real.csv');
speeds_real = table2array(speeds_real(:,3));
speeds_real = str2double(speeds_real);
speeds_real = abs(speeds_real)/10000;

% 定义移动平均滤波器参数
window_size = 30; % 窗口大小

% 应用移动平均滤波器
filtered_speeds = movmean(speeds, window_size);

time1 = linspace(0, 10, length(speeds));
time2 = linspace(0, 10, length(speeds_real));

% 绘制原始信号和滤波后的信号
figure;
subplot(2,1,1);
hold on;
plot(time1, speeds(:,2), 'b', 'LineWidth', 1.5);
plot(time1, filtered_speeds(:,2), 'r','LineWidth', 1.5)
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

