# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui1.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(954, 415)
        Form.setMinimumSize(QtCore.QSize(954, 415))
        Form.setMaximumSize(QtCore.QSize(954, 415))
        self.openVideo_pushButton = QtWidgets.QPushButton(Form)
        self.openVideo_pushButton.setGeometry(QtCore.QRect(30, 30, 100, 40))
        self.openVideo_pushButton.setObjectName("openVideo_pushButton")
        self.tarns_pushButton = QtWidgets.QPushButton(Form)
        self.tarns_pushButton.setGeometry(QtCore.QRect(140, 30, 100, 40))
        self.tarns_pushButton.setObjectName("tarns_pushButton")
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
        self.label_31.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
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
        self.label_30.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
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
        self.label_38.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_38.setObjectName("label_38")
        self.gridLayout.addWidget(self.label_38, 2, 6, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 2, 4, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_1.setFont(font)
        self.label_1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 4, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
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
        self.label_15.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
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
        self.label_33.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
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
        self.label_40.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
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
        self.label_17.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 1, 2, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_27.setFont(font)
        self.label_27.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
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
        self.label_22.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
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
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
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
        self.label_12.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
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
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.openVideo_pushButton.setText(_translate("Form", "영상 열기"))
        self.tarns_pushButton.setText(_translate("Form", "변환"))
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())