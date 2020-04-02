# 단순이동평균 + 보정 + 프레임(line349)
import easygui
import cv2
import numpy as np
import math

# open video file
video_path = easygui.fileopenbox()
# open video file
# video_path = '베타영상_빨.mp4'
cap = cv2.VideoCapture(video_path)
# print(video_path)

output_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # (width, height)
fit_to = 'height'
fps = cap.get(cv2.CAP_PROP_FPS)

# initialize writing video
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)

# check file is opened
if not cap.isOpened():
    print("영상 파일이 실행되지 않았습니다.")
    # exit()

# initialize tracker  트랙커
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

tracker = OPENCV_OBJECT_TRACKERS['csrt']()

# global variables
top_bottom_list, left_right_list = [], []
count = 0

# main
ret, img = cap.read()

# 변환하는 곳 여기서 함#############################################################
point_list = [[147, 482], [616, 401], [1040, 491], [518, 647]]  # 변환하려는 원본 좌표
count = 0
mouse_mod = -1

point_temp = [[0, 0], [1024, 0]]  # 변환된 곳에서 아는 거리 저장하는 좌표
start_xy = [0, 0]
end_xy = [0, 0]


def mouse_callback(event, x, y, flags, param):
    global point_list, count, img_original, mouse_mod, img_result, start_xy, end_xy

    # 마우스 왼쪽 버튼 누를 때마다 좌표를 리스트에 저장
    # if event == cv2.EVENT_LBUTTONDOWN and mouse_mod == 1:
    #     point_list.append((x, y))
    #     print(point_list)
    #     cv2.circle(img_original, (x, y), 3, (0, 0, 255), -1)

    # if event == cv2.EVENT_LBUTTONDOWN and mouse_mod == 0:
    #     point_temp.append((x, y))
    #     cv2.line(img_result, (point_temp[0][0], point_temp[0][1]), (x, y), (0, 255, 255), 3)

    if event == cv2.EVENT_LBUTTONDOWN and mouse_mod == 2:
        start_xy[0] = x
        start_xy[1] = y

    elif event == cv2.EVENT_LBUTTONUP and mouse_mod == 2:
        end_xy[0] = x
        end_xy[1] = y
        cv2.line(img_original, (start_xy[0], start_xy[1]), (end_xy[0], end_xy[1]), (0, 0, 255), 2)


def calculation_length(start, end, perspect_map, onepixel):
    trans_pts1 = np.ones((1, 3))
    trans_pts2 = np.ones((1, 3))
    num = 0
    for i in perspect_map[0:3]:
        trans_pts1[0][num] = i[0] * start[0] + i[1] * start[1] + i[2]
        trans_pts2[0][num] = i[0] * end[0] + i[1] * end[1] + i[2]
        num += 1

    trans_pts1 /= trans_pts1[0][2]
    trans_pts2 /= trans_pts2[0][2]

    print("변환전 픽셀: ", math.sqrt(pow(start[0] - end[0], 2) + pow(start[1] - end[1], 2)))
    trans_length = math.sqrt(pow(trans_pts1[0][0] - trans_pts2[0][0], 2) + pow(trans_pts1[0][1] - trans_pts2[0][1], 2))
    print("변환후 픽셀: ", trans_length)

    return trans_length * onepixel


def perstpective(perspect_map, pointList, onepixel):  # 이동경로 변환하는 함수
    trans_list = list()
    trans_point = np.ones((1, 3))
    num = 0
    for temp_list in pointList:
        for i in perspect_map[0:3]:  # x                      y
            trans_point[0][num] = (i[0] * temp_list[0]) + (i[1] * temp_list[1]) + i[2]
            num += 1
        trans_point /= trans_point[0][2]  # z값 나누기
        num = 0
        trans_list.append(trans_point[0:2])
        trans_point = np.ones((1, 3))

    temp = []
    trans_length = 0.0
    for temp_list2 in trans_list:
        if len(temp):
            trans_length += (math.sqrt(pow(temp[0][0] - temp_list2[0][0], 2) + pow(temp[0][1] - temp_list2[0][1], 2)))
        temp = temp_list2

    return trans_length * onepixel


cv2.namedWindow('original')
# mouse_mod = 1
# cv2.setMouseCallback('original', mouse_callback)

# 원본 이미지
img_original = img

# while(True):
#     cv2.imshow('original', img_original)
#
#     height, weight = img_original.shape[:2]
#
#     if cv2.waitKey(1)&0xFF == 32: # spacebar를 누르면 루프에서 빠져나옵니다.
#         break

# 좌표 순서 - 상단왼쪽 끝, 상단오른쪽 끝, 하단왼쪽 끝, 하단오른쪽 끝
# 원본 좌표
pts1 = np.float32([list(point_list[0]), list(point_list[1]), list(point_list[2]), list(point_list[3])])
# 목적 좌표
pts2 = np.float32([[0, 0], [1024, 0], [1024, 1024], [0, 1024]])

# 원근 변환 행렬
perspect_map = cv2.getPerspectiveTransform(pts1, pts2)
# print(type(perspect_map))

# result1 = "result1"
# cv2.namedWindow(result1, cv2.WINDOW_NORMAL)
img_result = cv2.warpPerspective(img_original, perspect_map, (1024, 1024))

# cv2.imshow(result1, img_result)
# cv2.waitKey(0)

print("아는 거리 클릭")
cv2.destroyWindow('original')
mouse_mod = 0  # 거리 표시모드
# cv2.setMouseCallback(result1, mouse_callback)

# while(True):
#     cv2.imshow(result1, img_result)
#
#     if cv2.waitKey(1)&0xFF == 32: # spacebar를 누르면 루프에서 빠져나옵니다.
#         break

# print("거리 입력하기")
arg_length = math.sqrt(pow(point_temp[0][0] - point_temp[1][0], 2) + pow(point_temp[0][1] - point_temp[1][1], 2))
# real_length = float(input("거리를 입력하세요: "))
real_length = 27.432

onepixel = real_length / arg_length
print("onepixel의 값: ", onepixel)

#######################마우스로 선 그어서 거리 알아보기
# mouse_mod =2
# cv2.setMouseCallback('original', mouse_callback)

# while(True):
#     cv2.setMouseCallback('original', mouse_callback)
#     cv2.imshow('original', img_original)
#     # cv2.waitKey(0)
#
#     length1 = calculation_length(start_xy, end_xy,perspect_map,onepixel)
#     print(length1)
#
#     if cv2.waitKey(1)&0xFF == 32: # spacebar를 누르면 루프에서 빠져나옵니다.
#         break

cv2.waitKey(0)

##########################################################################################################

cv2.namedWindow('Select Window', cv2.WINDOW_NORMAL)
cv2.imshow('Select Window', img)

print("====================")
print("a: 시작시간 저장")
print("s: 도착시간 저장")
print("q: 영상 끝내기")
print("w: 영상 일시정지")

# select ROI 영상의 추적 부분을 지정한다.
rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select Window')

# initialize tracker
tracker.init(img, rect)

nowPoint = [0, 0]
prePoint = [0, 0]
point_sum = [0, 0]
point_mean = [0, 0]
pre_point_mean = [0, 0]
length = 0.0
pix_num_move = 0.0
pointList = list()
route_pointList = list()
# mean_avg_list = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
mean_avg_list_size = int(fps / 2)  # 이동평균 리스트 크기
mean_avg_list = []
for i in range(mean_avg_list_size):  # 개수만큼 만듬
    mean_avg_list.append([0, 0])
isRecording = True
frame = 1
frame1 = 0
frame2 = 0

run_time = 0
start_a = 0
num = 255

fir_top = 0
pre_top = 0
f_t_h_cal = 0
t_p_h_cal = 0
adj_center_x = 0
adj_center_y = 0

# point_list_center_x = int(abs(point_list[0][0] - point_list[2][0]) / 2)
# point_list_center_y = 0
# if point_list[0][1] >= point_list[3][1]: # 3루가 1루보다 아래에 있을때 (같은 y축 위치도 포함)
#     point_list_center_y = point_list[0][1] - int(abs(point_list[0][1] - point_list[2][1]) / 2)
# if point_list[0][1] < point_list[3][1]: # 3루가 1루보다 위에 있을때
#     point_list_center_y = point_list[0][1] + int(abs(point_list[0][1] - point_list[2][1]) / 2)

# 홈과 2루 비율
slope_13 = (point_list[0][1] - point_list[2][1]) / (point_list[0][0] - point_list[2][0])
constant_13 = point_list[0][1] - slope_13 * point_list[0][0]
slope_h2 = (point_list[1][1] - point_list[3][1]) / (point_list[1][0] - point_list[3][0])
constant_h2 = point_list[1][1] - slope_h2 * point_list[1][0]
constant_ip = -(constant_13 - constant_h2) / (slope_13 - slope_h2)
intersect_point = [int(constant_ip), int(slope_13 * constant_ip + constant_13)]

point_list_y_ratio = math.sqrt((pow(intersect_point[0] - point_list[3][0], 2)) + (pow(intersect_point[1] - point_list[3][1], 2))) / \
                     math.sqrt((pow(intersect_point[0] - point_list[1][0], 2)) + (pow(intersect_point[1] - point_list[1][1], 2)))

print("비율: ", point_list_y_ratio)

# frame1 = 61
# frame2 = 160

pre_frame = 0

frame_num = 3
speed = 18

start_run_time = 0
end_run_time = 0
pre_time = 0
cur_time = 0
route_pers_distance = 0
pre_route_pers_distance = 0

line_count = 1
pre_route_pointList_index = 0

base1_list = list()
base2_list = list()
base3_list = list()
baseh_list = list()
base1_check = 0
base2_check = 0
base3_check = 0
baseh_check = 0
base1_time = 0
base2_time = 0
base3_time = 0
baseh_time = 0

base_time_count = 0
base_check_slope = 0
base_check_constant = 0

while True:
    k = cv2.waitKey(1)

    # if frame == frame1:
    #     start_a = 1
    # if frame == frame2:
    #     run_time = (frame2 - frame1) / fps
    #     print("시간: ", run_time)
    #     start_a = 2
    if k == ord('a'):
        frame1 = frame
        # print("시작 프레임: ", frame1)
        start_run_time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2)
        start_a = 1
    # elif k == ord('s'):
        # frame2 = frame
        # # print("끝 프레임: ", frame2)
        # end_run_time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2)
        # run_time = end_run_time - start_run_time
        # print("시간: ", run_time)
        # start_a = 2
    elif k == ord('q'):
        break
    elif k == ord('w'):
        print("일시정지")
        while cv2.waitKey(1) != ord('w') and cv2.waitKey(1) != ('q'):
            if cv2.waitKey(1) == ord('q'):
                break
    frame += 1

    count += 1
    # read frame from video
    ret, img = cap.read()

    if not ret:  # 프로그램이 끝나고 종료되는 곳
        break

    # update tracker and get position from new frame 트랙커가 따라가게 만드는 함수
    # success 성공했는지 안했는지 판단 bool box는 rect
    success, box = tracker.update(img)
    # if success:

    left, top, w, h = [int(v) for v in box]
    right = left + w
    bottom = top + h
    center_x = int(left + w / 2)
    center_y = int(top + h)
    # nowPoint[0] = center_x  # 0번 인덱스 x 1번 인덱스 y
    # nowPoint[1] = center_y

    constant_b1 = center_y - slope_13 * center_x  # 1, 3루
    constant_b2 = center_y - slope_h2 * center_x  # h, 2루

    if frame == 2:
        fir_top = top

    adj_center_x = int(left + w / 2)

    # 정면방향에서 촬영될 때를 기준
    # if (constant_b1 == 0 and constant_b2 == 0):  # 2,4면이랑 각 선에 있을때
    #     f_t_h_cal = (h * (abs(fir_top - top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))  # 초기위치 - 현재위치

    # 오른쪽방향에서 촬영될 때를 기준
    if (constant_b1 > constant_13 and constant_b2 < constant_h2) or (constant_b1 < constant_13 and constant_b2 > constant_h2) or (constant_b1 == constant_13 and constant_b2 >= constant_h2):  # 2,4면이랑 각 선에 있을때
        f_t_h_cal = (h * (abs(fir_top - top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))  # 초기위치 - 현재위치
    if (constant_b1 > constant_13 and constant_b2 > constant_h2) or (constant_b1 < constant_13 and constant_b2 < constant_h2):  # 1,3면에 있을때
        f_t_h_cal = (h * (abs(fir_top - top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) * point_list_y_ratio)  # 초기위치 - 현재위치

    # # 왼쪽방향에서 촬영될 때를 기준
    # if (constant_b1 > 0 and constant_b2 > 0) or (constant_b1 < 0 and constant_b2 < 0) or (constant_b1 == 0 and constant_b2 <= 0):  # 1,3면이랑 각 선에 있을때
    #     f_t_h_cal = (h * (abs(fir_top - top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))  # 초기위치 - 현재위치
    # if (constant_b1 > 0 and constant_b2 < 0) or (constant_b1 < 0 and constant_b2 > 0):  # 2,4면에 있을때
    #     f_t_h_cal = (h * (abs(fir_top - top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) * point_list_y_ratio)  # 초기위치 - 현재위치

    t_p_h_cal = (h * (abs(top - pre_top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))  # 현재위치 - 이전위치

    if fir_top > top:  # 초기위치보다 멀때
        if top < pre_top:  # 위쪽움직임
            adj_center_y = int(top + h - f_t_h_cal - t_p_h_cal)
        if top > pre_top:  # 아래쪽움직임
            adj_center_y = int(top + h - f_t_h_cal + t_p_h_cal)
        if top == pre_top:
            adj_center_y = int(top + h - f_t_h_cal)

    if fir_top < top:  # 초기위치보다 가까워질때
        if top < pre_top:
            adj_center_y = int(top + h + f_t_h_cal - t_p_h_cal)
        if top > pre_top:
            adj_center_y = int(top + h + f_t_h_cal + t_p_h_cal)
        if top == pre_top:
            adj_center_y = int(top + h + f_t_h_cal)

    if fir_top == top:
        if top < pre_top:
            adj_center_y = int(top + h - t_p_h_cal)
        if top > pre_top:
            adj_center_y = int(top + h + t_p_h_cal)
        if top == pre_top:
            adj_center_y = int(top + h)

    pre_top = top

    nowPoint[0] = adj_center_x  # 0번 인덱스 x 1번 인덱스 y
    nowPoint[1] = adj_center_y

    if count % frame_num == 0:
        if start_a == 1:
            point_sum[0] -= mean_avg_list[0][0]
            point_sum[1] -= mean_avg_list[0][1]

            mean_avg_list.pop(0)

            if start_a == 1:
                point_sum[0] += nowPoint[0]
                point_sum[1] += nowPoint[1]

            if start_a == 1:
                mean_avg_list.append(nowPoint[0:2])
            if start_a == 2:
                mean_avg_list.append([0, 0])

            if mean_avg_list.count([0, 0]) < mean_avg_list_size:
                point_mean[0] = int(point_sum[0] / (mean_avg_list_size - mean_avg_list.count([0, 0])))
                point_mean[1] = int(point_sum[1] / (mean_avg_list_size - mean_avg_list.count([0, 0])))

                pointList.append(point_mean[0:2])

        if frame1 + 1 == frame:
            pre_route_pers_distance = route_pers_distance
            pre_time = cur_time

        cur_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        route_run_time = round(cur_time - pre_time, 2)
        # print("시간 ", route_run_time)
        pre_time = cur_time

        route_pers_distance = round(perstpective(perspect_map, pointList, onepixel), 2)
        # print("거리 ", route_pers_distance - pre_route_pers_distance)
        route_v = round(abs(route_pers_distance - pre_route_pers_distance) / route_run_time * 3.6, 2)
        # print("속도 ", route_v)
        pre_route_pers_distance = route_pers_distance

        route_pointList.append(route_v)

    if frame1 == (frame + 1):
        pre_point_mean[0] = point_mean[0]
        pre_point_mean[1] = point_mean[1]

    if pre_point_mean[0] != point_mean[0]:
        if pre_point_mean[1] != point_mean[1]:
            base_check_slope = (point_mean[1] - pre_point_mean[1]) / (point_mean[0] - pre_point_mean[0])
            base_check_constant = point_mean[1] - base_check_slope * point_mean[0]
        if pre_point_mean[1] == point_mean[1]: # y=?
            base_check_slope = 0
            base_check_constant = pre_point_mean[1] # y축 이동 위치
    if pre_point_mean[0] == point_mean[0]:
        if pre_point_mean[1] != point_mean[1]: # x=?
            base_check_slope = 0
            base_check_constant = pre_point_mean[0] # x축 이동 위치
        if pre_point_mean[1] == point_mean[1]: # 같은 점
            base_check_slope = 0
            base_check_constant = 0

    if ((point_list[2][0] - 50 <= pre_point_mean[0] and pre_point_mean[0] <= point_list[2][0] + 20) or (point_list[2][0] - 50 <= point_mean[0] and point_mean[0] <= point_list[2][0] + 20)) and base1_check != 1:
        if base_check_slope != 0:
            if (pre_point_mean[1] >= point_list[2][1] and point_mean[1] <= point_list[2][1]) or (pre_point_mean[1] <= point_list[2][1] and point_mean[1] >= point_list[2][1]):
                base1_check = 1
                base1_list = pointList
                print("1루 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                base1_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time
        if base_check_slope == 0:
            if pre_point_mean[0] != point_mean[0]:
                if pre_point_mean[1] == point_list[2][1]:
                    base1_check = 1
                    base1_list = pointList
                    print("1루 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                    base1_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time
            if pre_point_mean[0] == point_mean[0]:
                if (pre_point_mean[1] <= point_list[2][1] and point_mean[1] >= point_list[2][1]) or (pre_point_mean[1] >= point_list[2][1] and point_mean[1] <= point_list[2][1]):
                    base1_check = 1
                    base1_list = pointList
                    print("1루 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                    base1_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time

    if ((point_list[0][0] - 20 <= pre_point_mean[0] and pre_point_mean[0] <= point_list[0][0] + 50) or (point_list[0][0] - 20 <= point_mean[0] and point_mean[0] <= point_list[0][0] + 50)) and base3_check != 3:
        if base_check_slope != 0:
            if (pre_point_mean[1] >= point_list[0][1] and point_mean[1] <= point_list[0][1]) or (pre_point_mean[1] <= point_list[0][1] and point_mean[1] >= point_list[0][1]):
                base3_check = 3
                base3_list = pointList
                print("3루 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                base3_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time
        if base_check_slope == 0:
            if pre_point_mean[0] != point_mean[0]:
                if pre_point_mean[1] == point_list[0][1]:
                    base3_check = 3
                    base3_list = pointList
                    print("3루 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                    base3_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time
            if pre_point_mean[0] == point_mean[0]:
                if (pre_point_mean[1] <= point_list[0][1] and point_mean[1] >= point_list[0][1]) or (pre_point_mean[1] >= point_list[0][1] and point_mean[1] <= point_list[0][1]):
                    base3_check = 3
                    base3_list = pointList
                    print("3루 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                    base3_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time

    if ((point_list[1][1] - 30 <= pre_point_mean[1] and pre_point_mean[1] <= point_list[1][1] + 30) or (point_list[1][1] - 30 <= point_mean[1] and point_mean[1] <= point_list[1][1] + 30)) and base2_check != 2:
        if base_check_slope != 0:
            if (pre_point_mean[0] <= point_list[1][0] and point_mean[0] >= point_list[1][0]) or (pre_point_mean[0] >= point_list[1][0] and point_mean[0] <= point_list[1][0]):
                base2_check = 2
                base2_list = pointList
                print("2루 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                base2_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time
        if base_check_slope == 0:
            if pre_point_mean[0] == point_mean[0]:
                if pre_point_mean[0] == point_list[1][0]:
                    base2_check = 2
                    base2_list = pointList
                    print("2루 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                    base2_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time
            if pre_point_mean[0] != point_mean[0]:
                if (pre_point_mean[0] <= point_list[1][0] and point_mean[0] >= point_list[1][0]) or (pre_point_mean[0] >= point_list[1][0] and point_mean[0] <= point_list[1][0]):
                    base2_check = 2
                    base2_list = pointList
                    print("2루 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                    base2_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time

    if ((point_list[3][1] - 30 <= pre_point_mean[1] and pre_point_mean[1] <= point_list[3][1] + 30) or (point_list[3][1] - 30 <= point_mean[1] and point_mean[1] <= point_list[3][1] + 30)) and baseh_check != 4:
        if base_check_slope != 0:
            if (pre_point_mean[0] <= point_list[3][0] and point_mean[0] >= point_list[3][0]) or (pre_point_mean[0] >= point_list[3][0] and point_mean[0] <= point_list[3][0]):
                baseh_check = 4
                baseh_list = pointList
                print("홈 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                baseh_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time
        if base_check_slope == 0:
            if pre_point_mean[0] == point_mean[0]:
                if pre_point_mean[0] == point_list[3][0]:
                    baseh_check = 4
                    baseh_list = pointList
                    print("홈 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                    baseh_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time
            if pre_point_mean[0] != point_mean[0]:
                if (pre_point_mean[0] <= point_list[3][0] and point_mean[0] >= point_list[3][0]) or (pre_point_mean[0] >= point_list[3][0] and point_mean[0] <= point_list[3][0]):
                    baseh_check = 4
                    baseh_list = pointList
                    print("홈 통과ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                    baseh_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start_run_time

    pre_point_mean[0] = point_mean[0]
    pre_point_mean[1] = point_mean[1]

    # print("Now: ", nowPoint)

    temp_x = 0
    temp_y = 0

    color_cal = 0
    route_pointList_i = 0
    # 이동경로 그리기
    for [x, y] in pointList:
        # print("x: ",x,y)
        if temp_x != 0 and temp_y != 0:
            route_pointList_index = route_pointList[route_pointList_i]
            if line_count == 1:
                pre_route_pointList_index = route_pointList_index
                line_count += 1

            route_pointList_index_div = abs(route_pointList_index - pre_route_pointList_index) / 2

            color_cal1 = 0
            if route_pointList_index >= pre_route_pointList_index:
                color_cal1 = abs(pre_route_pointList_index + route_pointList_index_div - 20) * 5
            if route_pointList_index < pre_route_pointList_index:
                color_cal1 = abs(pre_route_pointList_index - route_pointList_index_div - 20) * 5
            color_cal2 = abs(route_pointList_index - speed) * 5

            pre_route_pointList_index = route_pointList_index

            if route_pointList_index - speed >= 0:
                large_color1_255 = 127 - color_cal1
                if large_color1_255 <= 0:
                    large_color1_255 = 0
                large_color2_255 = 127 - color_cal2
                if large_color2_255 <= 0:
                    large_color2_255 = 0
                cv2.line(img, (x, y), (int((temp_x + x) / 2), int((temp_y + y) / 2)), (0, large_color1_255, 255), 2)
                cv2.line(img, (int((temp_x + x) / 2), int((temp_y + y) / 2)), (temp_x, temp_y), (0, large_color2_255, 255), 2)
            if route_pointList_index - speed < 0:
                little_color1_255 = 127 + color_cal1
                if little_color1_255 >= 255:
                    little_color1_255 = 255
                little_color2_255 = 127 + color_cal2
                if little_color2_255 >= 255:
                    little_color2_255 = 255
                cv2.line(img, (x, y), (int((temp_x + x) / 2), int((temp_y + y) / 2)), (0, little_color1_255, 255), 2)
                cv2.line(img, (int((temp_x + x) / 2), int((temp_y + y) / 2)), (temp_x, temp_y), (0, little_color2_255, 255), 2)

            route_pointList_i += 1
        temp_x = x
        temp_y = y

    #print("ㅡㅡㅡㅡㅡㅡㅡ")
    # print(pointList)
    # 거리계산하기
    length = math.sqrt(pow(point_mean[0] - pre_point_mean[0], 2) + pow(point_mean[1] - pre_point_mean[1], 2))

    # if length != 0.0:
    # print("이동픽셀: ", length)
    #    cv2.line(img, (nowPoint[0], nowPoint[1]), (prePoint[0], prePoint[1]), (0, 255, 0), 2)

    if length > 100:
        length = 0
    # 다음 거리 계산을 위한 직전좌표 저장
    # prePoint[0:2] = nowPoint[0:2]
    cv2.line(img, (adj_center_x, adj_center_y), (adj_center_x, adj_center_y), (255, 0, 255), 3)

    cv2.line(img, ((point_list[2][0] - 50), point_list[2][1]), ((point_list[2][0] + 20), point_list[2][1]), (0, 0, 255), 2)
    cv2.line(img, ((point_list[0][0] - 20), point_list[0][1]), ((point_list[0][0] + 50), point_list[0][1]), (0, 0, 255), 2)
    cv2.line(img, ((point_list[1][0]), point_list[1][1] - 30), ((point_list[1][0]), point_list[1][1] + 30), (0, 0, 255), 2)
    cv2.line(img, ((point_list[3][0]), point_list[3][1] - 30), ((point_list[3][0]), point_list[3][1] + 30), (0, 0, 255), 2)
    if length != 0.0:
        pix_num_move += length
    # print("이동거리: ", pix_num_move)
    # print("총 프레임: ", count)

    # visualize 영상의 사각형의 이미지 그리는 함수
    pt1 = (int(left), int(top))
    pt2 = (int(right), int(bottom))
    rect2 = cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)

    cv2.imshow('img', img)
    # cv2.imshow('result', result_img)
    # # write video
    out.write(img)

cap.release()
out.release()
cv2.destroyAllWindows()
###########################################
# 이동경로 변환하기
# print(pointList)
if base1_check == 1:
    pointList = base1_list
    run_time = base1_time
if base2_check == 2:
    pointList = base2_list
    run_time = base2_time
if base3_check == 3:
    pointList = base3_list
    run_time = base3_time
if baseh_check == 4:
    pointList = baseh_list
    run_time = baseh_time

pers_distance = round(perstpective(perspect_map, pointList, onepixel), 2)
print("변환된 물리적 거리는", pers_distance, "M 입니다")
# perstpective(perspect_map,pointList, onepixel)

# 출발점과 도착점만 계산할 때
# v2 = 마지막 거리 - 중간거리 / run_time
# v1 = 중간 거리 - 이전거리(0) / start_time - 이전 시간(0)
# v2가 선수 속도
v = round(pers_distance / run_time * 3.6, 2)
print("선수의 평균속도 ", v, "km/h 입니다.")
# a = (v2 - v1) / run_time - (start_time - 이전 시간)
a = round(v / run_time, 2)
print("선수의 평균가속도는 ", a, "km/h^2 입니다")
# Shortest_distance = round(math.sqrt(pow(pointList[0][0] - pointList[-1][0], 2) + pow(pointList[0][1] - pointList[-1][1], 2)), 2)
# efficiency = round(Shortest_distance / pix_num_move * 100, 2)
# print("선수의 효율성: ", efficiency, "% 입니다")

file = open("결과파일.txt", 'w')
file.write("영상 이름: ")
file.write(video_path)
file.write("\n")
file.write("선수 기록\n")
file.write("뛴거리: %f M \n" % pers_distance)
file.write("속도: %f km/h\n" % v)
file.write("가속도: %f km/h^2\n" % a)
# file.write("경로 효율성: %f %%\n" % efficiency)
file.close()