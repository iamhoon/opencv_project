# 버튼에 이벤트 처리하기
import easygui
import cv2
import sys
import numpy as np
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, Qt # 클릭 이벤트를 만들기 위해 필요
from PyQt5 import QtCore
from PyQt5 import QtGui

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

running = False
video_path = ""
point_list = []
mouse_mod =1
img_original=[]
location = [[],[]]
perspect_map = None

point_temp = [[0, 0], [1024, 0]]
onepixel = None

img_result = None

img = None



class Main_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.statusbar = self.statusBar()

        self.setMouseTracking(True)

        global label
        label = QLabel()
        vbox = QVBoxLayout()

        btn_step2 = QPushButton("step1")  # 비디오 변환 하는 버튼 (예정)
        btn_readVideo = QPushButton("openVideo")
        btn_start = QPushButton("Camera On")
        btn_stop = QPushButton("Camera Off")

        vbox.addWidget(label)
        vbox.addWidget(btn_readVideo)
        vbox.addWidget(btn_step2)
        vbox.addWidget(btn_start)
        vbox.addWidget(btn_stop)
        # vbox.addWidget(self.statusbar)
        self.setLayout(vbox)

        btn_readVideo.clicked.connect(self.openVideo)
        btn_step2.clicked.connect(self.step1)
        btn_start.clicked.connect(self.start)
        btn_stop.clicked.connect(self.stop)

        self.setGeometry(300,200,400,200)

        self.setWindowTitle("test")
        self.show()

    def mouseMoveEvent(self, event):
        txt = "Mouse 위치 ; x={0},y={1}, global={2},{3}".format(event.x(), event.y(),event.globalX(),event.globalY())

        # self.statusbar.showMessage(txt)
        location[0] = event.x()
        location[1] = event.y()

    def mouseButtonKind(self, button):
        if button & Qt.LeftButton:
            print(location)

    def mousePressEvent(self, e):
            self.mouseButtonKind(e.button())

    def openVideo(self):
        global video_path, labelm, img
        video_path = easygui.fileopenbox()
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("영상 파일이 실행되지 않았습니다.")

        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        label.resize(width, height)
        ret, img = cap.read()
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        label.resize(width, height)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        label.setPixmap(pixmap)
        label.setMouseTracking(True)

    def step1(self):

        global img_original, perspect_map, img_result, img
        # cap = cv2.VideoCapture(video_path)
        # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # label.resize(width, height)
        # ret, img = cap.read()
        img_original = img
        cv2.namedWindow('original')
        cv2.imshow("original", img_original)

        cv2.setMouseCallback('original', mouse_callback)

        # 좌표 순서 - 상단왼쪽 끝, 상단오른쪽 끝, 하단왼쪽 끝, 하단오른쪽 끝
        # 원본 좌표
        if len(point_list) == 4:
            pts1 = np.float32([list(point_list[0]), list(point_list[1]), list(point_list[2]), list(point_list[3])])
            # 목적 좌표
            pts2 = np.float32([[0, 0], [1024, 0], [1024, 1024], [0, 1024]])

            # 원근 변환 행렬
            perspect_map = cv2.getPerspectiveTransform(pts1, pts2)

            img_result = cv2.warpPerspective(img_original, perspect_map, (1024, 1024))

            print(perspect_map)
            arg_length = math.sqrt(
                pow(point_temp[0][0] - point_temp[1][0], 2) + pow(point_temp[0][1] - point_temp[1][1], 2))
            # real_length = float(input("거리를 입력하세요: "))
            real_length = 27.432

            onepixel = real_length / arg_length
            print("onepixel의 값: ", onepixel)

            # 홈과 2루 비율
            slope_13 = abs(point_list[0][1] - point_list[2][1]) / abs(point_list[0][0] - point_list[2][0])
            constant_13 = point_list[0][1] - slope_13 * point_list[0][0]
            slope_h2 = abs(point_list[1][1] - point_list[3][1]) / abs(point_list[1][0] - point_list[3][0])
            constant_h2 = point_list[1][1] - slope_h2 * point_list[1][0]
            constant_ip = (constant_h2 - constant_13) / (slope_13 - slope_h2)
            intersect_point = [int(constant_ip), int(slope_13 * constant_ip + constant_13)]

            point_list_y_ratio = math.sqrt(
                (pow(intersect_point[0] - point_list[3][0], 2)) + (pow(intersect_point[1] - point_list[3][1], 2))) / \
                                 math.sqrt((pow(intersect_point[0] - point_list[1][0], 2)) + (
                                     pow(intersect_point[1] - point_list[1][1], 2)))

            print("비율: ", point_list_y_ratio)

            frame_num = 3

    def step2(self):
        return 0

    def start(self):
        return 3
    def stop(self):
        return 4

def mouse_callback(event, x, y, flags, param):
    global point_list, count, img_original, mouse_mod, img_result, start_xy, end_xy

    # 마우스 왼쪽 버튼 누를 때마다 좌표를 리스트에 저장
    if len(point_list) < 4:
        if event == cv2.EVENT_LBUTTONDOWN and mouse_mod == 1:
            point_list.append((x, y))
            print(point_list)
            cv2.circle(img_original, (x, y), 3, (0, 0, 255), -1)
            cv2.imshow("original",img_original)
            print(len(point_list))

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Main_Window()
    sys.exit(app.exec_())