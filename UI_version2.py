# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\test_qt5\remote_temp.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!
import easygui
import cv2
import threading
import sys
import numpy as np
import math

from PyQt5 import QtCore, QtGui, QtWidgets

point_list = []
mouse_mod =1

location = [[],[]]
perspect_map = None

point_temp = [[0, 0], [1024, 0]]
onepixel = None

video_path = ""

img_original=None
img_result = None
img = None

class Ui_Form(object):
    running = False

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(345, 234)
        Form.setMinimumSize(QtCore.QSize(345, 234))
        Form.setMaximumSize(QtCore.QSize(345, 234))
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.player2_pushButton = QtWidgets.QPushButton(Form)
        self.player2_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.player2_pushButton.setObjectName("player2_pushButton")
        self.gridLayout.addWidget(self.player2_pushButton, 3, 1, 1, 1)
        self.player3_pushButton = QtWidgets.QPushButton(Form)
        self.player3_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.player3_pushButton.setObjectName("player3_pushButton")
        self.gridLayout.addWidget(self.player3_pushButton, 3, 2, 1, 1)
        self.player1_pushButton = QtWidgets.QPushButton(Form)
        self.player1_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.player1_pushButton.setObjectName("player1_pushButton")
        self.gridLayout.addWidget(self.player1_pushButton, 3, 0, 1, 1)
        self.player4_pushButton = QtWidgets.QPushButton(Form)
        self.player4_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.player4_pushButton.setIconSize(QtCore.QSize(8, 16))
        self.player4_pushButton.setObjectName("player4_pushButton")
        self.gridLayout.addWidget(self.player4_pushButton, 3, 3, 1, 1)
        self.player3_cancel_pushButton = QtWidgets.QPushButton(Form)
        self.player3_cancel_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.player3_cancel_pushButton.setObjectName("player3_cancel_pushButton")
        self.gridLayout.addWidget(self.player3_cancel_pushButton, 5, 2, 1, 1)
        self.player4_cancel_pushButton = QtWidgets.QPushButton(Form)
        self.player4_cancel_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.player4_cancel_pushButton.setObjectName("player4_cancel_pushButton")
        self.gridLayout.addWidget(self.player4_cancel_pushButton, 5, 3, 1, 1)
        self.player2_cancel_pushButton = QtWidgets.QPushButton(Form)
        self.player2_cancel_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.player2_cancel_pushButton.setObjectName("player2_cancel_pushButton")
        self.gridLayout.addWidget(self.player2_cancel_pushButton, 5, 1, 1, 1)
        self.player1_draw_pushButton = QtWidgets.QPushButton(Form)
        self.player1_draw_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.player1_draw_pushButton.setObjectName("player1_draw_pushButton")
        self.gridLayout.addWidget(self.player1_draw_pushButton, 4, 0, 1, 1)
        self.player1_cancel_pushButton = QtWidgets.QPushButton(Form)
        self.player1_cancel_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.player1_cancel_pushButton.setObjectName("player1_cancel_pushButton")
        self.gridLayout.addWidget(self.player1_cancel_pushButton, 5, 0, 1, 1)
        self.player2_draw_pushButton = QtWidgets.QPushButton(Form)
        self.player2_draw_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.player2_draw_pushButton.setObjectName("player2_draw_pushButton")
        self.gridLayout.addWidget(self.player2_draw_pushButton, 4, 1, 1, 1)
        self.player3_draw_pushButton = QtWidgets.QPushButton(Form)
        self.player3_draw_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.player3_draw_pushButton.setObjectName("player3_draw_pushButton")
        self.gridLayout.addWidget(self.player3_draw_pushButton, 4, 2, 1, 1)
        self.player3_draw_pushButton_2 = QtWidgets.QPushButton(Form)
        self.player3_draw_pushButton_2.setMinimumSize(QtCore.QSize(0, 30))
        self.player3_draw_pushButton_2.setObjectName("player3_draw_pushButton_2")
        self.gridLayout.addWidget(self.player3_draw_pushButton_2, 4, 3, 1, 1)
        self.stop_pushButton = QtWidgets.QPushButton(Form)
        self.stop_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.stop_pushButton.setObjectName("Stop_pushButton")
        self.gridLayout.addWidget(self.stop_pushButton, 2, 2, 1, 2)
        self.start_pushButton = QtWidgets.QPushButton(Form)
        self.start_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.start_pushButton.setObjectName("start_pushButton")
        self.gridLayout.addWidget(self.start_pushButton, 2, 0, 1, 2)
        self.openVideo_pushButton = QtWidgets.QPushButton(Form)
        self.openVideo_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.openVideo_pushButton.setObjectName("openVideo_pushButton")
        self.gridLayout.addWidget(self.openVideo_pushButton, 0, 0, 1, 2)
        self.trans_pushButton = QtWidgets.QPushButton(Form)
        self.trans_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.trans_pushButton.setObjectName("trans_pushButton")
        self.gridLayout.addWidget(self.trans_pushButton, 0, 2, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        # 버튼에 이번트 연결하는 부분
        self.openVideo_pushButton.clicked.connect(self.openVideo)
        self.trans_pushButton.clicked.connect(self.transform)
        self.start_pushButton.clicked.connect(self.start)
        self.stop_pushButton.clicked.connect(self.stop)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.player2_pushButton.setText(_translate("Form", "2번 선수"))
        self.player3_pushButton.setText(_translate("Form", "3번 선수"))
        self.player1_pushButton.setText(_translate("Form", "1번 선수"))
        self.player4_pushButton.setText(_translate("Form", "4번 선수"))
        self.player3_cancel_pushButton.setText(_translate("Form", "경로 종료"))
        self.player4_cancel_pushButton.setText(_translate("Form", "경로 종료"))
        self.player2_cancel_pushButton.setText(_translate("Form", "경로 종료"))
        self.player1_draw_pushButton.setText(_translate("Form", "경로 그리기"))
        self.player1_cancel_pushButton.setText(_translate("Form", "경로 종료"))
        self.player2_draw_pushButton.setText(_translate("Form", "경로 그리기"))
        self.player3_draw_pushButton.setText(_translate("Form", "경로 그리기"))
        self.player3_draw_pushButton_2.setText(_translate("Form", "경로 그리기"))
        self.stop_pushButton.setText(_translate("Form", "Stop"))
        self.start_pushButton.setText(_translate("Form", "Start"))
        self.openVideo_pushButton.setText(_translate("Form", "영상 열기"))
        self.trans_pushButton.setText(_translate("Form", "변환"))

    def openVideo(self):
        global video_path, labelm, img, img_original
        video_path = easygui.fileopenbox()
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("영상 파일이 실행되지 않았습니다.")

        ret, img = cap.read()

        img_original = img
        cv2.namedWindow('original')
        cv2.imshow("original", img_original)

        # 쓰레드 없으면 안되는 부분
        # while True:
        #     ret, img = cap.read()
        #     cv2.imshow("img", img)

        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # label.resize(width, height)
        # ret, img = cap.read()
        # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # label.resize(width, height)
        #
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # h, w, c = img.shape
        # qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        # pixmap = QtGui.QPixmap.fromImage(qImg)
        # label.setPixmap(pixmap)
        # label.setMouseTracking(True)

    def transform(self):
        global img_original, perspect_map, img_result, img

        cv2.setMouseCallback('original', mouse_callback)

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

    def videoRun(self):
        global running
        cap = cv2.VideoCapture(video_path)

        while running:
            ret, img = cap.read()

            if ret:
                cv2.imshow('original',img)
                if (cv2.waitKey(20) == 27):
                    break

            else:  # 마지막 프레임이 들어가도 걸리게 된다. 캠 화면을 들어오게 만들어서 계속진행되게 만들어짐
                # QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break
        cap.release()
        print("Thread end.")

    def start(self):
        global running
        running = True
        th = threading.Thread(target=self.videoRun)
        th.start()
        print("started..")

    def stop(self):
        global running
        running = False
        print("stoped..")


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
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())