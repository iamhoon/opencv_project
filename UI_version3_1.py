import easygui
import cv2
import threading
import os
import sys
import numpy as np
import math

from PyQt5 import QtCore, QtGui, QtWidgets

#############
number = 1
point_list = []
point_list_bool = False
mouse_mod = 0
count = 0

i = 0

location = [[], []]
perspect_map = None

point_temp = [[0, 0], [1024, 0]]
onepixel = 0

video_path = ""

img_original = None
img_result = None
img = None

rect_list = []
tracker = []
player_list = []

roi_i = 0

frame = 1
frame_check = 0

run_time = 0
start_check = 0
num = 255

slope_13 = None
slope_h2 = None
point_list_y_ratio = None

frame_num = 3
fps = 0
cap = None
out = None

tracker_x = 0
tracker_y = 0
tracker_w = 0
tracker_h = 0

mouse_callback_thead_mode = 0
click = False
####################

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

player_create_count = 0
# 플레이어 기록 키

# 플레이어 순서
player_ = [0, 0, 0, 0]


class Ui_Form(object):
    running = False

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(954, 415)
        Form.setMinimumSize(QtCore.QSize(954, 415))
        Form.setMaximumSize(QtCore.QSize(954, 415))
        self.openVideo_pushButton = QtWidgets.QPushButton(Form)
        self.openVideo_pushButton.setGeometry(QtCore.QRect(30, 30, 100, 40))
        self.openVideo_pushButton.setObjectName("openVideo_pushButton")
        self.trans_pushButton = QtWidgets.QPushButton(Form)
        self.trans_pushButton.setGeometry(QtCore.QRect(140, 30, 100, 40))
        self.trans_pushButton.setObjectName("trans_pushButton")
        self.addTracker_pushButton = QtWidgets.QPushButton(Form)
        self.addTracker_pushButton.setGeometry(QtCore.QRect(30, 100, 100, 40))
        self.addTracker_pushButton.setObjectName("addTracker_pushButton")
        self.routeDraw_pushButton = QtWidgets.QPushButton(Form)
        self.routeDraw_pushButton.setGeometry(QtCore.QRect(140, 100, 100, 40))
        self.routeDraw_pushButton.setObjectName("routeDraw_pushButton")
        self.routeCancel_pushButton = QtWidgets.QPushButton(Form)
        self.routeCancel_pushButton.setGeometry(QtCore.QRect(250, 100, 100, 40))
        self.routeCancel_pushButton.setObjectName("routeCancel_pushButton")
        self.start_pushButton = QtWidgets.QPushButton(Form)
        self.start_pushButton.setGeometry(QtCore.QRect(250, 30, 100, 40))
        self.start_pushButton.setObjectName("start_pushButton")
        self.stop_pushButton = QtWidgets.QPushButton(Form)
        self.stop_pushButton.setGeometry(QtCore.QRect(360, 30, 100, 40))
        self.stop_pushButton.setObjectName("stop_pushButton")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(30, 160, 901, 235))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.second_maxspeed_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.second_maxspeed_label.setFont(font)
        self.second_maxspeed_label.setText("")
        self.second_maxspeed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.second_maxspeed_label.setObjectName("second_maxspeed_label")
        self.gridLayout.addWidget(self.second_maxspeed_label, 3, 5, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_31.setFont(font)
        self.label_31.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_31.setObjectName("label_31")
        self.gridLayout.addWidget(self.label_31, 3, 6, 1, 1)
        self.third_maxspeed_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.third_maxspeed_label.setFont(font)
        self.third_maxspeed_label.setText("")
        self.third_maxspeed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.third_maxspeed_label.setObjectName("third_maxspeed_label")
        self.gridLayout.addWidget(self.third_maxspeed_label, 3, 7, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_30.setFont(font)
        self.label_30.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_30.setObjectName("label_30")
        self.gridLayout.addWidget(self.label_30, 3, 4, 1, 1)
        self.positions_first_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("HY궁서B")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.positions_first_label.setFont(font)
        self.positions_first_label.setAlignment(QtCore.Qt.AlignCenter)
        self.positions_first_label.setObjectName("positions_first_label")
        self.gridLayout.addWidget(self.positions_first_label, 0, 2, 1, 2)
        self.second_speed_llabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.second_speed_llabel.setFont(font)
        self.second_speed_llabel.setText("")
        self.second_speed_llabel.setAlignment(QtCore.Qt.AlignCenter)
        self.second_speed_llabel.setObjectName("second_speed_llabel")
        self.gridLayout.addWidget(self.second_speed_llabel, 2, 5, 1, 1)
        self.third_speed_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.third_speed_label.setFont(font)
        self.third_speed_label.setText("")
        self.third_speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.third_speed_label.setObjectName("third_speed_label")
        self.gridLayout.addWidget(self.third_speed_label, 2, 7, 1, 1)
        self.label_38 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_38.setFont(font)
        self.label_38.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_38.setObjectName("label_38")
        self.gridLayout.addWidget(self.label_38, 2, 6, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 2, 4, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_1.setFont(font)
        self.label_1.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 4, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.hitter_maxspeed_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.hitter_maxspeed_label.setFont(font)
        self.hitter_maxspeed_label.setText("")
        self.hitter_maxspeed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.hitter_maxspeed_label.setObjectName("hitter_maxspeed_label")
        self.gridLayout.addWidget(self.hitter_maxspeed_label, 3, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 3, 2, 1, 1)
        self.first_maxspeed_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.first_maxspeed_label.setFont(font)
        self.first_maxspeed_label.setText("")
        self.first_maxspeed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.first_maxspeed_label.setObjectName("first_maxspeed_label")
        self.gridLayout.addWidget(self.first_maxspeed_label, 3, 3, 1, 1)
        self.positions_hitter_label = QtWidgets.QLabel(self.widget)
        self.positions_hitter_label.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("HY궁서B")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.positions_hitter_label.setFont(font)
        self.positions_hitter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.positions_hitter_label.setObjectName("positions_hitter_label")
        self.gridLayout.addWidget(self.positions_hitter_label, 0, 0, 1, 2)
        self.label_33 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_33.setFont(font)
        self.label_33.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_33.setObjectName("label_33")
        self.gridLayout.addWidget(self.label_33, 4, 6, 1, 1)
        self.third_lead_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.third_lead_label.setFont(font)
        self.third_lead_label.setText("")
        self.third_lead_label.setAlignment(QtCore.Qt.AlignCenter)
        self.third_lead_label.setObjectName("third_lead_label")
        self.gridLayout.addWidget(self.third_lead_label, 4, 7, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_40.setFont(font)
        self.label_40.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_40.setObjectName("label_40")
        self.gridLayout.addWidget(self.label_40, 1, 6, 1, 1)
        self.second_distance_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.second_distance_label.setFont(font)
        self.second_distance_label.setText("")
        self.second_distance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.second_distance_label.setObjectName("second_distance_label")
        self.gridLayout.addWidget(self.second_distance_label, 1, 5, 1, 1)
        self.hitter_distance_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.hitter_distance_label.setFont(font)
        self.hitter_distance_label.setText("")
        self.hitter_distance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.hitter_distance_label.setObjectName("hitter_distance_label")
        self.gridLayout.addWidget(self.hitter_distance_label, 1, 1, 1, 1)
        self.first_distance_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.first_distance_label.setFont(font)
        self.first_distance_label.setText("")
        self.first_distance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.first_distance_label.setObjectName("first_distance_label")
        self.gridLayout.addWidget(self.first_distance_label, 1, 3, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 1, 2, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_27.setFont(font)
        self.label_27.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.gridLayout.addWidget(self.label_27, 1, 4, 1, 1)
        self.positions_second_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("HY궁서B")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.positions_second_label.setFont(font)
        self.positions_second_label.setAlignment(QtCore.Qt.AlignCenter)
        self.positions_second_label.setObjectName("positions_second_label")
        self.gridLayout.addWidget(self.positions_second_label, 0, 4, 1, 2)
        self.positions_third_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("HY궁서B")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.positions_third_label.setFont(font)
        self.positions_third_label.setAlignment(QtCore.Qt.AlignCenter)
        self.positions_third_label.setObjectName("positions_third_label")
        self.gridLayout.addWidget(self.positions_third_label, 0, 6, 1, 2)
        self.second_lead_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.second_lead_label.setFont(font)
        self.second_lead_label.setText("")
        self.second_lead_label.setAlignment(QtCore.Qt.AlignCenter)
        self.second_lead_label.setObjectName("second_lead_label")
        self.gridLayout.addWidget(self.second_lead_label, 4, 5, 1, 1)
        self.first_lead_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.first_lead_label.setFont(font)
        self.first_lead_label.setText("")
        self.first_lead_label.setAlignment(QtCore.Qt.AlignCenter)
        self.first_lead_label.setObjectName("first_lead_label")
        self.gridLayout.addWidget(self.first_lead_label, 4, 3, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_22.setFont(font)
        self.label_22.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 4, 4, 1, 1)
        self.third_distance_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.third_distance_label.setFont(font)
        self.third_distance_label.setText("")
        self.third_distance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.third_distance_label.setObjectName("third_distance_label")
        self.gridLayout.addWidget(self.third_distance_label, 1, 7, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.hitter_speed_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.hitter_speed_label.setFont(font)
        self.hitter_speed_label.setText("")
        self.hitter_speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.hitter_speed_label.setObjectName("hitter_speed_label")
        self.gridLayout.addWidget(self.hitter_speed_label, 2, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 2, 2, 1, 1)
        self.first_speed_llabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.first_speed_llabel.setFont(font)
        self.first_speed_llabel.setText("")
        self.first_speed_llabel.setAlignment(QtCore.Qt.AlignCenter)
        self.first_speed_llabel.setObjectName("first_speed_llabel")
        self.gridLayout.addWidget(self.first_speed_llabel, 2, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        # 버튼 이벤트 처리 부분
        self.openVideo_pushButton.clicked.connect(self.openVideo)
        self.trans_pushButton.clicked.connect(self.transform)
        self.start_pushButton.clicked.connect(self.start)
        self.stop_pushButton.clicked.connect(self.stop)

        self.addTracker_pushButton.clicked.connect(self.player_Roi)
        self.routeDraw_pushButton.clicked.connect(self.player_Draw)
        self.routeCancel_pushButton.clicked.connect(self.player_Cancel)
        self.player_Roi_bool = [False, False, False, False]  # 선수의 박스를 그렸는지 판단
        self.player_Roi_draw = False
        self.player_Draw_bool = False
        self.player_Cancel_bool = False

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.openVideo_pushButton.setText(_translate("Form", "영상 열기"))
        self.trans_pushButton.setText(_translate("Form", "변환"))
        self.addTracker_pushButton.setText(_translate("Form", "추적"))
        self.routeDraw_pushButton.setText(_translate("Form", "경로 그리기"))
        self.routeCancel_pushButton.setText(_translate("Form", "경로 종료"))
        self.start_pushButton.setText(_translate("Form", "재생"))
        self.stop_pushButton.setText(_translate("Form", "멈춤"))
        self.label_31.setText(_translate("Form", "최고속도"))
        self.label_30.setText(_translate("Form", "최고속도"))
        self.positions_first_label.setText(_translate("Form", "1루 주자"))
        self.label_38.setText(_translate("Form", "순간속도"))
        self.label_24.setText(_translate("Form", "순간속도"))
        self.label_1.setText(_translate("Form", "리드거리"))
        self.label_4.setText(_translate("Form", "최고속도"))
        self.label_15.setText(_translate("Form", "최고속도"))
        self.positions_hitter_label.setText(_translate("Form", "타자"))
        self.label_33.setText(_translate("Form", "리드거리"))
        self.label_40.setText(_translate("Form", "이동거리"))
        self.label_17.setText(_translate("Form", "이동거리"))
        self.label_27.setText(_translate("Form", "이동거리"))
        self.positions_second_label.setText(_translate("Form", "2루 주자"))
        self.positions_third_label.setText(_translate("Form", "3루 주자"))
        self.label_22.setText(_translate("Form", "리드거리"))
        self.label_3.setText(_translate("Form", "순간속도"))
        self.label_12.setText(_translate("Form", "순간속도"))
        self.label_2.setText(_translate("Form", "이동거리"))

    def openVideo(self):
        global video_path, labelm, img, img_original, fps, cap, out
        video_path = easygui.fileopenbox()
        cap = cv2.VideoCapture(video_path)

        output_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # (width, height)
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print("fps1", fps)

        if not cap.isOpened():
            print("영상 파일이 실행되지 않았습니다.")

        createFolder('perspect_map')

        ret, img = cap.read()

        img_original = img

        check()

        cv2.namedWindow('original')
        cv2.imshow("original", img)

    def transform(self):
        cv2.setMouseCallback('original', mouse_callback)

    def run(self):
        global running, img, frame, count, player_, player_create_count, frame_check, start_check, roi_i, out

        # cap = cv2.VideoCapture(video_path)

        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        while running:

            # k = cv2.waitKey(1)
            # control_key = cv2.waitKey(2)
            ret, img = cap.read()

            if self.player_Roi_draw:
                global roi_i
                print("선수 그리기")
                player_create()

                self.player_Roi_bool[roi_i] = True
                print(self.player_Roi_bool[0])
                self.player_Roi_draw = False

                roi_i += 1

            if self.player_Draw_bool:

                for j in range(0, player_create_count):
                    player_list[j].start_time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2)

                frame_check = frame
                start_check = 1
                self.player_Draw_bool = False

            if self.player_Cancel_bool:
                frame_check = 0
                start_check = 0

                for j in range(0, player_create_count):
                    player_delete(0)
                    self.player_Roi_bool[j] = False

                self.player_Cancel_bool = False

                player_create_count = 0

                roi_i = 0

            if self.player_Roi_bool[0]:
                player_tracking(1, frame_check, start_check)
            if self.player_Roi_bool[1]:
                player_tracking(2, frame_check, start_check)
            if self.player_Roi_bool[2]:
                player_tracking(3, frame_check, start_check)
            if self.player_Roi_bool[3]:
                player_tracking(4, frame_check, start_check)

            frame += 1
            count += 1

            cv2.imshow('original', img)

            if ret:

                if (cv2.waitKey(20) == 27):
                    break

            else:  # 마지막 프레임이 들어가도 걸리게 된다. 캠 화면을 들어오게 만들어서 계속진행되게 만들어짐
                # QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break

            out.write(img)

        cap.release()
        out.release()
        print("Thread end.")

    def start(self):
        global running
        running = True
        th = threading.Thread(target=self.run)
        th.start()
        print("started..")

    def stop(self):
        global running
        running = False
        print("stoped..")

    def player_Roi(self):
        self.player_Roi_draw = True

    def player_Draw(self):
        print("경로 그리기")
        self.player_Draw_bool = True

    def player_Cancel(self):
        print("경로 종료")
        self.player_Cancel_bool = True


def mouse_callback(event, x, y, flags, param):
    global point_list, mouse_mod

    # 마우스 왼쪽 버튼 누를 때마다 좌표를 리스트에 저장
    if len(point_list) < 4:
        if event == cv2.EVENT_LBUTTONDOWN:
            point_list.append((x, y))
            print(point_list)
            cv2.circle(img_original, (x, y), 3, (0, 0, 255), -1)
            cv2.imshow("original", img_original)
            print(len(point_list))

    if len(point_list) == 4 and mouse_mod == 0:
        calculator_point_list_y_ratio()
        mouse_mod += 1


def calculator_point_list_y_ratio():
    global slope_13, slope_h2, point_list_y_ratio, img_result, perspect_map

    pts1 = np.float32([list(point_list[0]), list(point_list[1]), list(point_list[2]), list(point_list[3])])
    # 목적 좌표
    pts2 = np.float32([[0, 0], [1024, 0], [1024, 1024], [0, 1024]])

    if not point_list_bool:
        save_pointList()

    # 원근 변환 행렬
    perspect_map = cv2.getPerspectiveTransform(pts1, pts2)
    print(perspect_map)

    print("img_original", img_original)

    img_result = cv2.warpPerspective(img_original, perspect_map, (1024, 1024))
    # cv2.imshow("변환 결괴", img_result)

    # print(perspect_map)
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
    ui.trans_pushButton.setDisabled(True)  # 버튼 비활성화


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("만들기 에러" + directory)


def save_pointList():
    fileNum = 0

    for i in os.listdir('perspect_map'):
        str1 = i.split(".")[0]
        fileNum = int(str1)
        print(fileNum)
    fileNum += 1

    fileName = open('perspect_map/' + str(fileNum) + ".txt", 'w')
    fileName.write(video_path + "\n")
    fileName.write(str(point_list))

    print("변환 좌표가 저장되었습니다.")
    fileName.close()


def check():
    global point_list, point_list_bool

    for name in os.listdir('perspect_map'):
        # print("file name", name)
        file = open('perspect_map\\' + name, 'r')
        # str = file.readline().splitlines()
        file_str = file.readline()
        remove_str = file_str.rstrip('\n')

        if remove_str == video_path:
            file_str = file.readline()  # 두번째 줄 읽어와 저장
            print("file_str", file_str)

            change_list(file_str)

            point_list_bool = True
            calculator_point_list_y_ratio()

            ui.trans_pushButton.setDisabled(True)  # 버튼 비활성화
            file.close()
            break
        else:
            print("변환좌표 없음")


def change_list(file_str):
    global point_list

    str_replace = file_str.replace('[', "").replace(']', "").replace('(', "").replace(')', "")
    str_split = str_replace.split(', ')

    num = 0
    for i in range(0, int(len(str_split) / 2)):
        tmep = []
        tmep.append(int(str_split[num]))
        tmep.append(int(str_split[num + 1]))
        point_list.append(tmep)
        num += 2


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


def player_create():
    global player_create_count
    # global player_create_count, tracker_x, tracker_y, tracker_w, tracker_h
    # 선수의 수만큼 tracker와 추적 ROI를 만듬
    tracker.append(OPENCV_OBJECT_TRACKERS['csrt']())
    cv2.destroyWindow('original')
    rect_list.append(cv2.selectROI('original', img, False))
    # rect_list.append(cv2.selectROI('original', img, fromCenter=False, showCrosshair=True))
    print("선수 순서: " + str(player_create_count + 1))

    tracker[player_create_count].init(img, rect_list[player_create_count])

    player_list.append(Player())
    player_list[player_create_count].mean_avg_list_init()

    player_create_count += 1


def player_tracking(player_order, frame_key, start):
    success, box = tracker[player_order - 1].update(img)
    # success_list.append(success)
    # box_list.append(box)
    player_list[player_order - 1].box(box)

    if frame_key + 1 == frame:
        player_list[player_order - 1].fir_top = player_list[player_order - 1].top
    player_list[player_order - 1].constant(slope_13, slope_h2, point_list_y_ratio)
    player_list[player_order - 1].positional_correction()

    if count % frame_num == 0:
        player_list[player_order - 1].mean_avg(start)
        player_list[player_order - 1].route_color(frame, frame_key, perspect_map, onepixel)
        player_list[player_order - 1].calculation_between_base()

    player_list[player_order - 1].draw_route()

    rect_list[player_order - 1] = player_list[player_order - 1].draw_box(player_list[player_order - 1].player_position)
    cv2.line(img, (player_list[player_order - 1].adj_center_x, player_list[player_order - 1].adj_center_y),
             (player_list[player_order - 1].adj_center_x, player_list[player_order - 1].adj_center_y), (255, 0, 255), 3)

    player_list[player_order - 1].player_data_box()


def player_delete(player_create_count):
    del tracker[player_create_count]
    del rect_list[player_create_count]
    del player_list[player_create_count]


class Player():
    def __init__(self):
        self.fir_top = 0
        self.cur_time = 0  # 현재시간
        self.pre_time = 0
        self.start_time = 0  # 각 선수의 출발 시간 현재 개발 과정에서는 run_time 전역 변수로 통일되어 있음
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

        self.player_position = 0  # 1번: 2루, 2번: 1루, 3번: 홈, 0번: 3루 플레이어의 초기 베이스 위치
        self.player_position_check = 0
        self.impormation = {
            "베이스": [],
            "시간": [],
            "최고속도": [],
            "속도": [],
            "거리": []
        }

    # 경로를 그리기 위한 변수들

    # 이동평균 리스트 크기

    def mean_avg_list_init(self):  # 이동평균 초기화
        self.mean_avg_list_size = int(fps / 2)
        for i in range(self.mean_avg_list_size):  # 개수만큼 만듬
            self.mean_avg_list.append([0, 0])

    def box(self, box):
        self.left, self.top, self.w, self.h = [int(v) for v in box]

        if self.fir_top == 0:
            self.fir_top = self.top
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

    def positional_correction(self):  # 위치에 따른 점의 보정을 위한 함수
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
    def mean_avg(self, start):
        self.nowPoint[0] = self.adj_center_x
        self.nowPoint[1] = self.adj_center_y
        if start == 1:
            self.point_sum[0] -= self.mean_avg_list[0][0]
            self.point_sum[1] -= self.mean_avg_list[0][1]

            self.mean_avg_list.pop(0)

            if start == 1:
                self.point_sum[0] += self.nowPoint[0]
                self.point_sum[1] += self.nowPoint[1]

            if start == 1:
                self.mean_avg_list.append(self.nowPoint[0:2])

            if self.mean_avg_list.count([0, 0]) < self.mean_avg_list_size:
                self.point_mean[0] = int(
                    self.point_sum[0] / (self.mean_avg_list_size - self.mean_avg_list.count([0, 0])))
                self.point_mean[1] = int(
                    self.point_sum[1] / (self.mean_avg_list_size - self.mean_avg_list.count([0, 0])))

                self.pointList.append(self.point_mean[0:2])
        cv2.line(img, (self.adj_center_x, self.adj_center_y), (self.adj_center_x, self.adj_center_y), (255, 0, 255), 3)

    def route_color(self, frame, frame_key, perspect_map, onepixel):  # 이동경로를 색상으로 표현하기 위하여 구간별 속도 계산
        if frame_key + 1 == frame:
            self.pre_route_pers_distance = self.route_pers_distance
            self.pre_time = self.cur_time

        self.cur_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        route_run_time = round(self.cur_time - self.pre_time, 2)  # 현재시간과 직전시간을 뺀 시간 시간 간격 확인
        # print("시간 ", route_run_time)
        self.pre_time = self.cur_time
        # 총 달린거리
        self.route_pers_distance = round(perstpective(perspect_map, self.pointList, onepixel), 2)
        # print("거리", self.route_pers_distance)
        # 단위거리 = 총달린거리 - 직전달린거리
        if route_run_time != 0:
            route_v = round(abs(self.route_pers_distance - self.pre_route_pers_distance) / route_run_time * 3.6, 2)

            self.route_pointList.append(route_v)
        # print("속도 ", route_v)
        self.pre_route_pers_distance = self.route_pers_distance
        # 속도 변화 값??

    def draw_route(self):
        speed = 18
        temp_x = 0
        temp_y = 0
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
                    cv2.line(img, (int((temp_x + x) / 2), int((temp_y + y) / 2)), (temp_x, temp_y),
                             (0, large_color2_255, 255), 4)
                if route_pointList_index - speed < 0:
                    little_color1_255 = 127 + color_cal1
                    if little_color1_255 >= 255:
                        little_color1_255 = 255
                    little_color2_255 = 127 + color_cal2
                    if little_color2_255 >= 255:
                        little_color2_255 = 255
                    cv2.line(img, (x, y), (int((temp_x + x) / 2), int((temp_y + y) / 2)), (0, little_color1_255, 255),
                             4)
                    cv2.line(img, (int((temp_x + x) / 2), int((temp_y + y) / 2)), (temp_x, temp_y),
                             (0, little_color2_255, 255), 4)

                route_pointList_i += 1
            temp_x = x
            temp_y = y

        # cv2.line(img, (self.adj_center_x, self.adj_center_y), (self.adj_center_x, self.adj_center_y), (255, 0, 255), 3)

    def print_imformation(self, perspect_map, onepixel, run_time):
        total_time = sum(self.impormation["시간"])  # 총시간
        total_distance = sum(self.impormation["거리"])  # 총거리
        avg_speed = round(sum(self.impormation["거리"]) / sum(self.impormation["시간"]) * 3.6, 2)
        for i in range(0, len(self.impormation["베이스"])):
            print(i + 1, "구간")
            print("시간: ", self.impormation["시간"][i])
            print("거리: ", self.impormation["거리"][i])
            print("속도: ", self.impormation["속도"][i])

        print("선수번호: ", self.player_position)
        print("변환된 물리적 거리는", total_distance, "M 입니다")
        # v = round(pers_distance / run_time * 3.6, 2)
        # a = round(v / run_time, 2)
        # print("최고 속력 " + + " 입니다.")
        print("평균 속도", avg_speed, " 입니다.")
        print("최고 속도", max(self.route_pointList), " 입니다")
        print("시간 " + str(total_time) + " 입니다.")

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
        running_time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2) - self.start_time  # 달린시간 = 현재시간 - 출발시간
        # self.impormation["경로"].append(self.pointList)
        running_route = round(perstpective(perspect_map, self.pointList, onepixel), 2)
        if not self.impormation["베이스"]:  # 베이스를 첫번쨰 밟을 때
            self.impormation["베이스"].append(self.now_base)
            self.impormation["시간"].append(running_time)
            self.impormation["거리"].append(running_route)
            self.impormation["속도"].append(round(running_route / running_time * 3.6, 2))
            print("구간 시간: " + str(self.impormation["시간"][-1]))
            print("구간 거리: " + str(self.impormation["거리"][-1]))
            print("구간 속도: " + str(self.impormation["속도"][-1]))
            print("----------")
        else:  # 베이스를 두번째 부터 밟을 때
            self.impormation["베이스"].append(self.now_base)
            self.impormation["시간"].append(running_time - sum(self.impormation["시간"]))
            self.impormation["거리"].append(running_route - sum(self.impormation["거리"]))
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

        if (
        math.sqrt(pow(self.next_base[0] - self.nowPoint[0], 2) + pow(self.next_base[1] - self.nowPoint[1], 2))) < 13.0:
            print("---------베이스 통과-----------")
            if point_list.index(self.now_base) - 1 == 0:
                print("3루 통과")
            elif point_list.index(self.now_base) - 1 == 1:
                print("2루 통과")
            elif point_list.index(self.now_base) - 1 == 2:
                print("1루 통과")
            elif point_list.index(self.now_base) - 1 == -1:
                print("홈 통과")

            self.set_next_base()  # 현재 베이스와 다음 베이스를 설정
            self.measure()  # 베이스 설정 후 현재 베이스까지의 정보를 측정하여 저장

    # 현재 선수의 위치에서 가장 가까운 베이스를 now_base 에 설정한다.
    def set_base(self):
        base_length = {
            "거리": [],
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

        if self.player_position_check == 0:
            self.player_position = point_list.index((self.now_base))
            self.player_position_check = 1

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
        if self.route_pointList != []:
            self.now_speed = self.route_pointList[-1]
            self.max_speed = max(self.route_pointList)
            self.avg_speed = round(sum(self.route_pointList) / len(self.route_pointList), 2)

            start_width_point = 0
            end_width_point = 0

            if self.player_position == 3:
                start_rect_point_num = 0
                end_rect_point_num = 1
                start_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * start_rect_point_num / 8)
                end_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * end_rect_point_num / 8)
                cv2.rectangle(img, (start_width_point, 0), (end_width_point + 2, 92), (0, 0, 255), 2)
            elif self.player_position == 2:
                start_rect_point_num = 2
                end_rect_point_num = 3
                start_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * start_rect_point_num / 8)
                end_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * end_rect_point_num / 8)
                cv2.rectangle(img, (start_width_point, 0), (end_width_point + 2, 92), (255, 0, 0), 2)
            elif self.player_position == 1:
                start_rect_point_num = 4
                end_rect_point_num = 5
                start_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * start_rect_point_num / 8)
                end_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * end_rect_point_num / 8)
                cv2.rectangle(img, (start_width_point, 0), (end_width_point + 2, 92), (0, 255, 0), 2)
            elif self.player_position == 0:
                start_rect_point_num = 6
                end_rect_point_num = 7
                start_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * start_rect_point_num / 8)
                end_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * end_rect_point_num / 8)
                cv2.rectangle(img, (start_width_point, 0), (end_width_point + 2, 92), (0, 255, 255), 2)

            cv2.rectangle(img, (start_width_point, 0), (end_width_point, 90), (255, 255, 255), -1)

            cv2.putText(img, 'Player : ' + str(self.player_position), (start_width_point + 3, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 0, 0), 1)
            cv2.putText(img, 'now_V : ' + str(self.now_speed), (start_width_point + 3, 40), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 0, 0), 1)
            cv2.putText(img, 'max_V : ' + str(self.max_speed), (start_width_point + 3, 60), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 0, 0), 1)
            cv2.putText(img, 'avg_V : ' + str(self.avg_speed), (start_width_point + 3, 80), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 0, 0), 1)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())