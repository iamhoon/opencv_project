# 단순이동평균 + 보정 + 프레임(line349) + 다중객체 추적을 위한 클래스 추가
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

select_player_num = int(input("추적할 인원 수: "))
# select ROI 영상의 추적 부분을 지정한다.
# tracker = OPENCV_OBJECT_TRACKERS['csrt']()
# 멀티트레킹을 위한 변수
rect_list = []
tracker = []
player_list = []
success_list = []
box_list = []

# 선수의 수만큼 tracker와 추적 ROI를 만듬
for i in range(0, select_player_num):
    tracker.append(OPENCV_OBJECT_TRACKERS['csrt']())
    rect_list.append(cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True))
    print("선수 순서: " + str(i))

# rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select Window')
# initialize tracker 선수의 수만큼 tracker 초기화
for i in range(0, select_player_num):
    tracker[i].init(img, rect_list[i])

isRecording = True
frame = 1
frame1 = 0
frame2 = 0

run_time = 0
start_a = 0
num = 255

# 홈과 2루 비율
slope_13 = abs(point_list[0][1] - point_list[2][1]) / abs(point_list[0][0] - point_list[2][0])
constant_13 = point_list[0][1] - slope_13 * point_list[0][0]
slope_h2 = abs(point_list[1][1] - point_list[3][1]) / abs(point_list[1][0] - point_list[3][0])
constant_h2 = point_list[1][1] - slope_h2 * point_list[1][0]
constant_ip = (constant_h2 - constant_13) / (slope_13 - slope_h2)
intersect_point = [int(constant_ip), int(slope_13 * constant_ip + constant_13)]

point_list_y_ratio = math.sqrt((pow(intersect_point[0] - point_list[3][0], 2)) + (pow(intersect_point[1] - point_list[3][1], 2))) / \
                     math.sqrt((pow(intersect_point[0] - point_list[1][0], 2)) + (pow(intersect_point[1] - point_list[1][1], 2)))

print("비율: ", point_list_y_ratio)

frame_num = 3

# #######
class Player():
    def __init__(self, player_num):
      self.player_num = player_num
      self.fir_top = 0
      self.cur_time = 0 # 현재시간
      self.pre_time = 0
      self.start_time = 0 # 각 선수의 출발 시간 현재 개발 과정에서는 run_time 전역 변수로 통일되어 있음
      self.pre_top = 0
      self.right = 0
      self.bottom = 0
      self.center_x = 0
      self.left = 0
      self.top = 0
      self.w = 0
      self.h = 0
      self.f_t_h_cal = 0
      self.t_p_h_cal = 0
      self.adj_center_x = 0
      self.adj_center_y = 0
      self.route_pers_distance = 0
      self.pre_route_pers_distance = 0
      self.nowPoint = [0, 0]
      self.point_sum = [0, 0]
      self.point_mean = [0, 0]
      self.pointList = []
      self.route_pointList = []
      self.mean_avg_list = []
      self.line_count = 1

      self.length = 0.0
      self.pix_num_move = 0.0
      self.pre_route_pointList_index = 0

      self.now_speed = 0
      self.max_speed = 0
      self.avg_speed = 0

      self.now_base = []
      self.next_base = []
      self.impormation = {
          "베이스" : [],
          "시간" : [],
          "최고속도" : [],
          "속도" : [],
          "거리" : []
      }
    # 경로를 그리기 위한 변수들

    mean_avg_list_size = int(fps / 2)  # 이동평균 리스트 크기

    # for i in range(mean_avg_list_size):  # 개수만큼 만듬
    #     mean_avg_list.append([0, 0])


    def mean_avg_lis_init(self): # 이동평균 초기화
        for i in range(Player.mean_avg_list_size):  # 개수만큼 만듬
            self.mean_avg_list.append([0, 0])

    def box(self, box):
        self.left, self.top, self.w, self.h = [int(v) for v in box]
        self.right = self.left + self.w
        self.bottom = self.top + self.h
        self.center_x = int(self.left + self.w / 2)
        self.center_y = int(self.top + self.h)

    def draw_box(self, number):
        pt1 = (int(self.left), int(self.top))
        pt2 = (int(self.right), int(self.bottom))

        if number == 0:
            return cv2.rectangle(img, pt1, pt2, (0, 0, 255), 3)
        elif number == 1:
            return cv2.rectangle(img, pt1, pt2, (255, 0, 0), 3)
        elif number == 2:
            return cv2.rectangle(img, pt1, pt2, (0, 255, 0), 3)
        elif number == 3:
            return cv2.rectangle(img, pt1, pt2, (0, 255, 255), 3)

    def constant(self, slope_13, slope_h2, point_list_y_ratio):
        constant_b1 = self.center_y - slope_13 * self.center_x  # 1, 3루
        constant_b2 = self.center_y - slope_h2 * self.center_x  # h, 2루
        if (constant_b1 > 0 and constant_b2 < 0) or (constant_b1 < 0 and constant_b2 > 0) or (constant_b1 == 0 and constant_b2 >= 0):  # 2,4면이랑 각 선에 있을때
          self.f_t_h_cal = (self.h * (abs(self.fir_top - self.top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))  # 초기위치 - 현재위치
        if (constant_b1 > 0 and constant_b2 > 0) or (constant_b1 < 0 and constant_b2 < 0):  # 1,3면에 있을때
          self.f_t_h_cal = (self.h * (abs(self.fir_top - self.top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) * point_list_y_ratio)

    def positional_correction(self):  #위치에 따른 점의 보정을 위한 함수
        self.t_p_h_cal = (self.h * (abs(self.top - self.pre_top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        self.adj_center_x = int(self.left + self.w / 2)

        if self.fir_top > self.top:  # 초기위치보다 멀때
            if self.top < self.pre_top:  # 위쪽움직임
                self.adj_center_y = int(self.top + self.h - self.f_t_h_cal - self.t_p_h_cal)
            if self.top > self.pre_top:  # 아래쪽움직임
                self.adj_center_y = int(self.top + self.h - self.f_t_h_cal + self.t_p_h_cal)
            if self.top == self.pre_top:
                self.adj_center_y = int(self.top + self.h - self.f_t_h_cal)

        if self.fir_top < self.top:  # 초기위치보다 가까워질때
            if self.top < self.pre_top:
                self.adj_center_y = int(self.top + self.h + self.f_t_h_cal - self.t_p_h_cal)
            if self.top > self.pre_top:
                self.adj_center_y = int(self.top + self.h + self.f_t_h_cal + self.t_p_h_cal)
            if self.top == self.pre_top:
                self.adj_center_y = int(self.top + self.h + self.f_t_h_cal)

        if self.fir_top == self.top:
            if self.top < self.pre_top:
                self.adj_center_y = int(self.top + self.h - self.t_p_h_cal)
            if self.top > self.pre_top:
                self.adj_center_y = int(self.top + self.h + self.t_p_h_cal)
            if self.top == self.pre_top:
                self.adj_center_y = int(self.top + self.h)
        self.pre_top = self.top

    # 이동평균 계산하여 경로 그리기 보정 & 속도별 칼라추가 작업
    def mean_avg(self, start_a):
        self.nowPoint[0] = self.adj_center_x
        self.nowPoint[1] = self.adj_center_y
        if start_a == 1 or start_a == 2:
            self.point_sum[0] -= self.mean_avg_list[0][0]
            self.point_sum[1] -= self.mean_avg_list[0][1]

            self.mean_avg_list.pop(0)

            if start_a == 1:
                self.point_sum[0] += self.nowPoint[0]
                self.point_sum[1] += self.nowPoint[1]

            if start_a == 1:
                self.mean_avg_list.append(self.nowPoint[0:2])
            if start_a == 2:
                self.mean_avg_list.append([0, 0])

            if self.mean_avg_list.count([0, 0]) < Player.mean_avg_list_size:
                self.point_mean[0] = int(self.point_sum[0] / (Player.mean_avg_list_size - self.mean_avg_list.count([0, 0])))
                self.point_mean[1] = int(self.point_sum[1] / (Player.mean_avg_list_size - self.mean_avg_list.count([0, 0])))

                self.pointList.append(self.point_mean[0:2])
        cv2.line(img, (self.adj_center_x, self.adj_center_y), (self.adj_center_x, self.adj_center_y), (255, 0, 255), 3)

    def route_color(self, frame, frame1, perspect_map, onepixel): # 이동경로를 색상으로 표현하기 위하여 구간별 속도 계산
        if frame1 + 1 == frame:
            self.pre_route_pers_distance = self.route_pers_distance
            self.pre_time = self.cur_time

        self.cur_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        route_run_time = round(self.cur_time - self.pre_time, 2) # 현제시간과 직전시간을 뺀 시간 시간 간역 확인
        # print("시간 ", route_run_time)
        self.pre_time = self.cur_time
        # 총 달린거리
        self.route_pers_distance = round(perstpective(perspect_map, self.pointList, onepixel), 2)
        # print("거리", self.route_pers_distance)
        # 단위거리 = 총달린거리 - 직전달린거리
        route_v = round(abs(self.route_pers_distance - self.pre_route_pers_distance) / route_run_time * 3.6, 2)
        # print("속도 ", route_v)
        self.pre_route_pers_distance = self.route_pers_distance
        # 속도 변화 값??
        self.route_pointList.append(route_v)

    def draw_route(self):
        speed = 18
        temp_x = 0
        temp_y = 0
        color_cal = 0
        route_pointList_i = 0
        for [x, y] in self.pointList:
            # print("x: ",x,y)
            if temp_x != 0 and temp_y != 0:
                route_pointList_index = self.route_pointList[route_pointList_i]
                if self.line_count == 1:
                    self.pre_route_pointList_index = route_pointList_index
                    self.line_count += 1

                route_pointList_index_div = abs(route_pointList_index - self.pre_route_pointList_index) / 2
                self.pre_route_pointList_index = route_pointList_index

                color_cal1 = 0
                if route_pointList_index >= self.pre_route_pointList_index:
                    color_cal1 = abs(self.pre_route_pointList_index + route_pointList_index_div - speed) * 10
                if route_pointList_index < self.pre_route_pointList_index:
                    color_cal1 = abs(self.pre_route_pointList_index - route_pointList_index_div - speed) * 10
                color_cal2 = abs(route_pointList_index - speed) * 10

                if route_pointList_index - speed >= 0:
                    large_color1_255 = 127 - color_cal1
                    if large_color1_255 <= 0:
                        large_color1_255 = 0
                    large_color2_255 = 127 - color_cal2
                    if large_color2_255 <= 0:
                        large_color2_255 = 0
                    cv2.line(img, (x, y), (int((temp_x + x) / 2), int((temp_y + y) / 2)), (0, large_color1_255, 255), 4)
                    cv2.line(img, (int((temp_x + x) / 2), int((temp_y + y) / 2)), (temp_x, temp_y), (0, large_color2_255, 255), 4)
                if route_pointList_index - speed < 0:
                    little_color1_255 = 127 + color_cal1
                    if little_color1_255 >= 255:
                        little_color1_255 = 255
                    little_color2_255 = 127 + color_cal2
                    if little_color2_255 >= 255:
                        little_color2_255 = 255
                    cv2.line(img, (x, y), (int((temp_x + x) / 2), int((temp_y + y) / 2)), (0, little_color1_255, 255), 4)
                    cv2.line(img, (int((temp_x + x) / 2), int((temp_y + y) / 2)), (temp_x, temp_y), (0, little_color2_255, 255), 4)

                route_pointList_i += 1
            temp_x = x
            temp_y = y

        # cv2.line(img, (self.adj_center_x, self.adj_center_y), (self.adj_center_x, self.adj_center_y), (255, 0, 255), 3)

    def print_imformation(self, perspect_map, onepixel, run_time):
        total_time = sum(self.impormation["시간"]) # 총시간
        total_distance = sum(self.impormation["거리"]) # 총거리
        avg_speed = round(sum(self.impormation["거리"]) / sum(self.impormation["시간"]) * 3.6, 2)
        for i in range(0, len(self.impormation["베이스"])):
            print(i+1, "구간")
            print("시간: ", self.impormation["시간"][i])
            print("거리: ", self.impormation["거리"][i])
            print("속도: ", self.impormation["속도"][i])

        print("선수번호: ", self.player_num)
        print("변환된 물리적 거리는", total_distance, "M 입니다")
        # v = round(pers_distance / run_time * 3.6, 2)
        # a = round(v / run_time, 2)
        # print("최고 속력 " + + " 입니다.")
        print("평균 속도", avg_speed, " 입니다.")
        print("최고 속도", max(self.route_pointList), " 입니다")
        print("시간 "+ str(total_time) + " 입니다.")

        file = open("결과파일.txt", 'w')
        file.write("영상 이름: ")
        file.write(video_path)
        file.write("\n")
        file.write("선수 기록\n")
        file.write("뛴거리: %f M \n" % total_distance)
        file.write("속도: %f km/h\n" % avg_speed)
        file.write("시간: %f s\n" % total_time)
        file.close()

    # 베이스의 위치를 반환한다.
    def dase_check(self, now_base):
        if point_list.index(now_base) == 0:
            return 3
        elif point_list.index(now_base) == 1:
            return 2
        elif point_list.index(now_base) == 2:
            return 1
        elif point_list.index(now_base) == 3:
            return 0

    # 통과 후 정보 측정하기
    def measure(self):
        running_time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2) - self.start_time # 달린시간 = 현재시간 - 출발시간
        # self.impormation["경로"].append(self.pointList)
        running_route = round(perstpective(perspect_map, self.pointList, onepixel), 2)
        if not self.impormation["베이스"]: # 베이스를 첫번쨰 밟을 때
            self.impormation["베이스"].append(self.now_base)
            self.impormation["시간"].append(running_time)
            self.impormation["거리"].append(running_route)
            self.impormation["속도"].append(round(running_route / running_time*3.6,2))
            print("구간 시간: " + str(self.impormation["시간"][-1]))
            print("구간 거리: " + str(self.impormation["거리"][-1]))
            print("구간 속도: " + str(self.impormation["속도"][-1]))
            print("----------")
        else: # 베이스를 두번째 부터 밟을 때
            self.impormation["베이스"].append(self.now_base)
            self.impormation["시간"].append(running_time - sum(self.impormation["시간"]))
            self.impormation["거리"].append(running_route -sum(self.impormation["거리"]))
            self.impormation["속도"].append(round(self.impormation["거리"][-1] / self.impormation["시간"][-1] * 3.6, 2))
            print("구간 시간: " + str(self.impormation["시간"][-1]))
            print("구간 거리: " + str(self.impormation["거리"][-1]))
            print("구간 속도: " + str(self.impormation["속도"][-1]))
            print("----------")

        # self.impormation["속도"]
        # self.impormation["최고속도"]

    # 베이스와 거리를 계산하여 베이스의 반지름보다 작으면 베이스를 밟은 것으로 인식하고 다음 베이스를 설정한다.
    def calculation_between_base(self):
        if not self.now_base:
            self.set_base()
            self.set_next_base()

        if (math.sqrt(pow(self.next_base[0] - self.nowPoint[0], 2) + pow(self.next_base[1] - self.nowPoint[1], 2))) < 13.0:
            print("---------베이스 통과-----------")
            if point_list.index(self.now_base) - 1 == 0:
                print("3루 통과")
            elif point_list.index(self.now_base) - 1 == 1:
                print("2루 통과")
            elif point_list.index(self.now_base) - 1 == 2:
                print("1루 통과")
            elif point_list.index(self.now_base) - 1 == -1:
                print("홈 통과")

            self.set_next_base() # 현재 베이스와 다음 베이스를 설정
            self.measure() #베이스 설정 후 현재 베이스까지의 정보를 측정하여 저장

    # 현재 선수의 위치에서 가장 가까운 베이스를 now_base 에 설정한다.
    def set_base(self):
        base_length = {
            "거리" : [],
            "베이스": [],
        }

        for i in point_list:
            base_length["거리"].append(math.sqrt(pow(i[0] - self.nowPoint[0], 2) + pow(i[1] - self.nowPoint[1], 2)))
            base_length["베이스"].append(i)

        self.now_base = base_length["베이스"][base_length["거리"].index(min(base_length["거리"]))]
        if point_list.index(self.now_base) == 0:
            print("3루 시작")
        elif point_list.index(self.now_base) == 1:
            print("2루 시작")
        elif point_list.index(self.now_base) == 2:
            print("1루 시작")
        elif point_list.index(self.now_base) == 3:
             print("홈 시작")

    # now_base의 다음 베이스 좌표 세팅
    def set_next_base(self):
        self.set_base()
        self.next_base = point_list[point_list.index(self.now_base) - 1]
        if point_list.index(self.now_base) - 1 == 0:
            print("3루까지")
        elif point_list.index(self.now_base) - 1 == 1:
            print("2루 까지")
        elif point_list.index(self.now_base) - 1 == 2:
            print("1루 까지")
        elif point_list.index(self.now_base) - 1 == -1:
            print("홈 까지")

    def player_data_box(self):
        sum_pointList = 0
        if self.route_pointList != []:
            self.now_speed = self.route_pointList[-1]
            self.max_speed = max(self.route_pointList)
            self.avg_speed = round(sum(self.route_pointList) / len(self.route_pointList), 2)

            start_rect_point_num = self.player_num * 2 - 2
            end_rect_point_num = self.player_num * 2 - 1
            start_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * start_rect_point_num / 8)
            end_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * end_rect_point_num / 8)

            if self.player_num == 1:
                cv2.rectangle(img, (start_width_point, 0), (end_width_point+2, 92), (0, 0, 255), 2)
            elif self.player_num == 2:
                cv2.rectangle(img, (start_width_point, 0), (end_width_point + 2, 92), (255, 0, 0), 2)
            elif self.player_num == 3:
                cv2.rectangle(img, (start_width_point, 0), (end_width_point + 2, 92), (0, 255, 0), 2)
            elif self.player_num == 4:
                cv2.rectangle(img, (start_width_point, 0), (end_width_point + 2, 92), (0, 255, 255), 2)

            cv2.rectangle(img, (start_width_point, 0), (end_width_point, 90), (255, 255, 255), -1)

            cv2.putText(img, 'Player : ' + str(self.player_num), (start_width_point + 3, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
            cv2.putText(img, 'now_V : ' + str(self.now_speed), (start_width_point + 3, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
            cv2.putText(img, 'max_V : ' + str(self.max_speed), (start_width_point + 3, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
            cv2.putText(img, 'avg_V : ' + str(self.avg_speed), (start_width_point + 3, 80), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)


for i in range(0, select_player_num):
    player_list.append(Player(i + 1))
    player_list[i].mean_avg_lis_init()
    # player_list[i].set_base()
    # player_list[i].set_next_base()

time_num = 1

print("====================")
print("a: 시작시간 저장")
print("s: 도착시간 저장")
print("q: 영상 끝내기")
print("w: 영상 일시정지")

while True:
    # temp_time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000,2)
    # if temp_time == time_num:
    #     print(str(temp_time)+"초입니다.@@@@@@@@@@@@@@@@@@@@@@@@")
    #     time_num += 1
    #     # break
    #
    # print("시간이여::"+str(temp_time))
    k = cv2.waitKey(1)
    # if frame == 60:
    #     print("60")

    if k == ord('a'):
        frame1 = frame
        # print("시작 프레임: ", frame1)
        print("a")
        start_run_time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2)
        for i in range(0, select_player_num):
            player_list[i].start_time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2)
        start_a = 1
    # elif k == ord('s'):
    #     frame2 = frame
    #     # print("끝 프레임: ", frame2)
    #     end_run_time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2)
    #     run_time = end_run_time - start_run_time
    #     print("끝시간: ", run_time)
    #     start_a = 2
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

    for i in range(0, select_player_num):
        success, box = tracker[i].update(img)
        # success_list.append(success)
        # box_list.append(box)
        player_list[i].box(box)
        if frame == 2:
            player_list[i].fir_top = player_list[i].top
        player_list[i].constant(slope_13, slope_h2, point_list_y_ratio)
        player_list[i].positional_correction()

        if count % frame_num == 0:

            player_list[i].mean_avg(start_a)
            player_list[i].route_color(frame, frame1, perspect_map, onepixel)
            player_list[i].calculation_between_base()

        player_list[i].draw_route()

        rect_list[i] = player_list[i].draw_box(i)
        cv2.line(img, (player_list[i].adj_center_x, player_list[i].adj_center_y), (player_list[i].adj_center_x, player_list[i].adj_center_y), (255, 0, 255), 3)

        player_list[i].player_data_box()

    # circle = cv2.circle(img, (point_list[0][0], point_list[0][1]), 10, (255, 0, 0), 2)
    # circle2 = cv2.circle(img, (point_list[1][0], point_list[1][1]), 10, (255, 0, 0), 2)
    # circle3 = cv2.circle(img, (point_list[2][0], point_list[2][1]), 10, (255, 0, 0), 2)
    # circle4 = cv2.circle(img, (point_list[3][0], point_list[3][1]), 10, (255, 0, 0), 2)

    # print("ㅡㅡㅡㅡㅡㅡㅡ")

    cv2.imshow('img', img)
    out.write(img)

cap.release()
out.release()
cv2.destroyAllWindows()
# player2.print_imformation(perspect_map, onepixel, run_time)
for i in range(0, select_player_num):
    player_list[i].print_imformation(perspect_map, onepixel, run_time)