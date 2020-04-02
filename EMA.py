# import color as color
import easygui
import cv2
import numpy as np
import math
import time
import sys
import msvcrt as m

# open video file
video_path = easygui.fileopenbox()
# open video file
# video_path = '베타영상_빨.mp4'
cap = cv2.VideoCapture(video_path)
# print(video_path)

output_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # (width, height)
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

#변환하는 곳 여기서 함#############################################################
point_list = [] # 변환하려는 원본 좌표
mouse_mod = -1

point_temp = [] # 변환된 곳에서 아는 거리 저장하는 좌표
start_xy = [0, 0]
end_xy = [0, 0]

def mouse_callback(event, x, y, flags, param):
    global point_list, count, img_original, mouse_mod, img_result, start_xy, end_xy


    # 마우스 왼쪽 버튼 누를 때마다 좌표를 리스트에 저장
    if event == cv2.EVENT_LBUTTONDOWN and mouse_mod == 1:
        point_list.append((x, y))
        print(point_list)
        cv2.circle(img_original, (x, y), 3, (0, 0, 255), -1)

    elif event == cv2.EVENT_LBUTTONDOWN and mouse_mod == 0:
        point_temp.append((x, y))
        cv2.line(img_result, (point_temp[0][0], point_temp[0][1]), (x, y), (0, 255, 255), 3)

    elif event == cv2.EVENT_LBUTTONDOWN and mouse_mod == 2:
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

def perstpective(perspect_map, pointList, onepixel): #이동경로 변환하는 함수

    trans_list = list()
    trans_point = np.ones((1,3))
    num = 0
    for temp_list in pointList:

        for i in perspect_map[0:3]:       # x                      y
            trans_point[0][num] = (i[0] * temp_list[0]) + (i[1] * temp_list[1]) + i[2]
            num += 1
        trans_point /= trans_point[0][2] # z값 나누기
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
mouse_mod = 1
cv2.setMouseCallback('original', mouse_callback)

# 원본 이미지
img_original = img


while(True):
    cv2.imshow('original', img_original)

    height, weight = img_original.shape[:2]

    if cv2.waitKey(1) & 0xFF == 32: # spacebar를 누르면 루프에서 빠져나옵니다.
        break


# 좌표 순서 - 상단왼쪽 끝, 상단오른쪽 끝, 하단왼쪽 끝, 하단오른쪽 끝
# 원본 좌표
pts1 = np.float32([list(point_list[0]), list(point_list[1]), list(point_list[2]), list(point_list[3])])
# 목적 좌표
pts2 = np.float32([[0, 0], [1024, 0], [1024, 1024], [0, 1024]])

# 원근 변환 행렬
perspect_map = cv2.getPerspectiveTransform(pts1,pts2)
# print(type(perspect_map))

result1 = "result1"
cv2.namedWindow(result1, cv2.WINDOW_NORMAL)
img_result = cv2.warpPerspective(img_original, perspect_map, (1024,1024))

cv2.imshow(result1, img_result)
cv2.waitKey(0)

print("아는 거리 클릭")
cv2.destroyWindow('original')
mouse_mod = 0 # 거리 표시모드
cv2.setMouseCallback(result1, mouse_callback)

while(True):

    cv2.imshow(result1, img_result)

    if cv2.waitKey(1)&0xFF == 32: # spacebar를 누르면 루프에서 빠져나옵니다.
        break

# print("거리 입력하기")
arg_length = math.sqrt(pow(point_temp[0][0] - point_temp[1][0], 2) + pow(point_temp[0][1] - point_temp[1][1], 2))
# real_length = float(input("거리를 입력하세요: "))
real_length = 27.432

onepixel = real_length / arg_length
print("onepixl의 값: ", onepixel)

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
length = 0.0
pix_num_move = 0.0
pointList = list()
mean_avg_list = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
mean_avg_list_size = 10
mean_avg_K = int(2 / (mean_avg_list_size + 1) * 100) # int사용으로 100곱함
mean_avg_EMA = [0, 0]
isRecording = True
frame = 1
frame1 = 0
frame2 = 0
cal_count = 0

start_a = 0
num = 255
run_time = 0

while True:
    k = cv2.waitKey(1)

    if k == ord('a'):
        frame1 = frame
        print("시작 프레임: ", frame1)
        start_a = 1
    elif k == ord('s'):
        frame2 = frame
        print("끝 프레임: ", frame2)
        run_time = (frame2 - frame1) / fps
        print("시간: ", run_time)
        start_a = 2
    elif k == ord('q'):
        break
    elif k == ord('w'):
        print("일시정지")
        while cv2.waitKey(1) != ord('w') and cv2.waitKey(1) != ('q'):
             if cv2.waitKey(1) == ord('q'):
                break
    frame += 1

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
    center_y = int(top + h / 2)
    nowPoint[0] = center_x  # 0번 인덱스 x 1번 인덱스 y
    nowPoint[1] = center_y

    if start_a == 1:
        cal_count += 1
        point_sum[0] += nowPoint[0]
        point_sum[1] += nowPoint[1]

        if cal_count == mean_avg_list_size:
            point_mean[0] = point_sum[0] / mean_avg_list_size
            point_mean[1] = point_sum[1] / mean_avg_list_size

        if cal_count == (mean_avg_list_size + 1):
            mean_avg_EMA[0] = int((nowPoint[0] * mean_avg_K + point_mean[0] * (100 - mean_avg_K)) / 100)
            mean_avg_EMA[1] = int((nowPoint[1] * mean_avg_K + point_mean[1] * (100 - mean_avg_K)) / 100)

        if cal_count > (mean_avg_list_size + 1):
            mean_avg_EMA[0] = int((nowPoint[0] * mean_avg_K + mean_avg_EMA[0] * (100 - mean_avg_K)) / 100)
            mean_avg_EMA[1] = int((nowPoint[1] * mean_avg_K + mean_avg_EMA[1] * (100 - mean_avg_K)) / 100)

        pointList.append(mean_avg_EMA[0:2])


    # print("Now: ", nowPoint)
    temp_x = 0
    temp_y = 0

    #이동경로 그리기
    for [x, y] in pointList:
        # print("x: ",x,y)
        if temp_x != 0 and temp_y != 0:
            cv2.line(img, (x, y), (temp_x, temp_y), (0, 255, 255), 2)
        temp_x = x
        temp_y = y

    # print(pointList)
    # 거리계산하기
    length = math.sqrt(pow(nowPoint[0] - prePoint[0], 2) + pow(nowPoint[1] - prePoint[1], 2))

    # if length != 0.0:
        # print("이동픽셀: ", length)
#    cv2.line(img, (nowPoint[0], nowPoint[1]), (prePoint[0], prePoint[1]), (0, 255, 0), 2)

    if length > 100:
       length = 0
    #다음 거리 계산을 위한 직전좌표 저장
    prePoint[0:2] = nowPoint[0:2]
    cv2.line(img, (center_x, center_y), (center_x, center_y), (255, 0, 255), 3)

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
pers_distance = round(perstpective(perspect_map, pointList, onepixel), 2)
print("변환된 물리적 거리는", pers_distance, "M 입니다")
# perstpective(perspect_map,pointList, onepixel)

# 출발점과 도착점만 계산할 때
# v2 = 마지막 거리 - 중간거리 / run_time
# v1 = 중간 거리 - 이전거리(0) / start_time - 이전 시간(0)
# v2가 선수 속도
v = round(pers_distance / run_time * 3.6, 2)
print("선수의 속도 ", v, "km/h 입니다.")
# a = (v2 - v1) / run_time - (start_time - 이전 시간)
a = round(v / run_time, 2)
print("선수의 가속도는 ", a, "km/h^2 입니다")
Shortest_distance = round(math.sqrt(pow(pointList[0][0] - pointList[-1][0], 2) + pow(pointList[0][1] - pointList[-1][1], 2)), 2)
efficiency = round(Shortest_distance/pix_num_move*100, 2)
print("선수의 효율성: ", efficiency, "% 입니다")

file = open("결과파일.txt", 'w')
file.write("영상 이름: ")
file.write(video_path)
file.write("\n")
file.write("선수 기록\n")
file.write("뛴거리: %f M \n"%pers_distance)
file.write("속도: %f km/h\n"%v)
file.write("가속도: %f km/h^2\n" % a)
file.write("경로 효율성: %f %%\n" % efficiency)
file.close()