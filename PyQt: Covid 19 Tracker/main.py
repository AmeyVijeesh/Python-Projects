from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from data import (
    get_live_data_country,
    get_latest_no,
    is_connected,
    data_extract,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(617, 486)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(size_policy)
        MainWindow.setMaximumSize(QtCore.QSize(1091, 487))
        self.central_widget = QtWidgets.QWidget(MainWindow)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.central_widget.sizePolicy().hasHeightForWidth()
        )
        self.central_widget.setSizePolicy(size_policy)
        self.central_widget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.central_widget)
        self.label.setGeometry(QtCore.QRect(10, 20, 751, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(16)
        font.setUnderline(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.central_widget)
        self.label_2.setGeometry(QtCore.QRect(10, 460, 31, 16))
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(self.central_widget)
        self.line.setGeometry(QtCore.QRect(0, 450, 631, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.central_widget)
        self.line_2.setGeometry(QtCore.QRect(0, 40, 621, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.groupBox = QtWidgets.QGroupBox(self.central_widget)
        self.groupBox.setGeometry(QtCore.QRect(20, 60, 221, 111))
        self.groupBox.setObjectName("groupBox")
        self.rocover_label = QtWidgets.QLabel(self.groupBox)
        self.rocover_label.setGeometry(QtCore.QRect(10, 20, 191, 16))
        self.rocover_label.setObjectName("recover_label")
        self.confirmed_label = QtWidgets.QLabel(self.groupBox)
        self.confirmed_label.setGeometry(QtCore.QRect(10, 40, 191, 16))
        self.confirmed_label.setObjectName("cnfrm_label")
        self.death_label = QtWidgets.QLabel(self.groupBox)
        self.death_label.setGeometry(QtCore.QRect(10, 60, 191, 16))
        self.death_label.setObjectName("death_label")
        self.date_label = QtWidgets.QLabel(self.groupBox)
        self.date_label.setGeometry(QtCore.QRect(10, 80, 191, 16))
        self.date_label.setObjectName("date_label")
        self.groupBox_2 = QtWidgets.QGroupBox(self.central_widget)
        self.groupBox_2.setGeometry(QtCore.QRect(270, 60, 221, 111))
        self.groupBox_2.setObjectName("groupBox_2")
        self.recover2_label = QtWidgets.QLabel(self.groupBox_2)
        self.recover2_label.setGeometry(QtCore.QRect(10, 20, 191, 16))
        self.recover2_label.setObjectName("recover_label_2")
        self.cnfrm_label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.cnfrm_label_2.setGeometry(QtCore.QRect(10, 40, 191, 16))
        self.cnfrm_label_2.setObjectName("confirm_label_2")
        self.death_label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.death_label_2.setGeometry(QtCore.QRect(10, 60, 191, 16))
        self.death_label_2.setObjectName("death_label_2")
        self.date_label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.date_label_2.setGeometry(QtCore.QRect(10, 80, 191, 16))
        self.date_label_2.setObjectName("date_label_2")
        self.refreshbtn = QtWidgets.QPushButton(self.central_widget)
        self.refreshbtn.setGeometry(QtCore.QRect(500, 100, 91, 23))
        self.refreshbtn.setObjectName("refreshbtn")
        self.refreshbtn.clicked.connect(self.refresh)
        self.groupBox_3 = QtWidgets.QGroupBox(self.central_widget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 180, 571, 251))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(10, 30, 191, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit.setGeometry(QtCore.QRect(140, 30, 241, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(400, 30, 121, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.retrieve_country_data)
        self.country_name_lbl = QtWidgets.QLabel(self.groupBox_3)
        self.country_name_lbl.setGeometry(QtCore.QRect(30, 90, 231, 16))
        self.country_name_lbl.setObjectName("country_name_lbl")
        self.recv_coun_label = QtWidgets.QLabel(self.groupBox_3)
        self.recv_coun_label.setGeometry(QtCore.QRect(30, 110, 191, 16))
        self.recv_coun_label.setObjectName("recv_coun_label")
        self.cnfirm_country_label = QtWidgets.QLabel(self.groupBox_3)
        self.cnfirm_country_label.setGeometry(QtCore.QRect(30, 130, 191, 16))
        self.cnfirm_country_label.setObjectName("cnfirm_country_label")
        self.death_country_label = QtWidgets.QLabel(self.groupBox_3)
        self.death_country_label.setGeometry(QtCore.QRect(30, 150, 181, 16))
        self.death_country_label.setObjectName("death_country_label")
        self.active_cases_label = QtWidgets.QLabel(self.groupBox_3)
        self.active_cases_label.setGeometry(QtCore.QRect(30, 170, 201, 16))
        self.active_cases_label.setObjectName("active_cases_label")
        self.pie_chart = QtWidgets.QPushButton(self.groupBox_3)
        self.pie_chart.setGeometry(QtCore.QRect(400, 60, 121, 23))
        self.pie_chart.setObjectName("pie_chart")
        self.pie_chart.setEnabled(False)
        self.pie_chart.clicked.connect(self.generate_pie_chart)
        self.date_label_country = QtWidgets.QLabel(self.groupBox_3)
        self.date_label_country.setGeometry(QtCore.QRect(30, 190, 331, 16))
        self.date_label_country.setObjectName("date_label_country")
        self.label_5 = QtWidgets.QLabel(self.central_widget)
        self.label_5.setGeometry(QtCore.QRect(140, 460, 491, 20))
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(self.central_widget)
        self.label_3.setGeometry(QtCore.QRect(200, 440, 281, 16))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CoronaVirus Tracker"))
        self.label.setText(_translate("MainWindow", "COVID 19 tracker"))
        self.label_2.setText(_translate("MainWindow", "v 1.0"))
        self.groupBox.setTitle(_translate("MainWindow", "World Data"))
        self.rocover_label.setText(_translate("MainWindow", "Recovered :"))
        self.confirmed_label.setText(_translate("MainWindow", "Confirmed :"))
        self.death_label.setText(_translate("MainWindow", "Deaths :"))
        self.date_label.setText(_translate("MainWindow", "Data Last Refreshed On:"))
        self.groupBox_2.setTitle(_translate("MainWindow", "USA data"))
        self.recover2_label.setText(_translate("MainWindow", "Recovered :"))
        self.cnfrm_label_2.setText(_translate("MainWindow", "Confirmed :"))
        self.death_label_2.setText(_translate("MainWindow", "Deaths :"))
        self.date_label_2.setText(_translate("MainWindow", "Data Last Refreshed On :"))
        self.refreshbtn.setText(_translate("MainWindow", "Refresh Data"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Other Countries"))
        self.label_4.setText(_translate("MainWindow", "Enter the Country Name"))
        self.pushButton.setText(_translate("MainWindow", "Get Data"))
        self.country_name_lbl.setText(_translate("MainWindow", "Country Name:"))
        self.recv_coun_label.setText(_translate("MainWindow", "Recovered:"))
        self.cnfirm_country_label.setText(_translate("MainWindow", "Confirmed:"))
        self.death_country_label.setText(_translate("MainWindow", "Deaths:"))
        self.active_cases_label.setText(_translate("MainWindow", "Active Cases:"))
        self.pie_chart.setText(_translate("MainWindow", "Show Pie Chart"))
        self.date_label_country.setText(
            _translate("MainWindow", "Database Last Update On :")
        )
        self.label_5.setText(
            _translate(
                "MainWindow",
                "Retrieves data from https://api.covid19api.com/ ",
            )
        )
        self.label_3.setText(
            _translate("MainWindow", "By: Amey")
        )

    def refresh(self):
        global data
        msg = QMessageBox()
        network_check = is_connected()
        if network_check is False:
            msg.setIcon(QMessageBox.Information)
            msg.setText("No Internet! Please do check your network connection and try again!")
            msg.setWindowTitle("Connection Check")
            msg.exec_()
        else:
            data_refresh = get_latest_no()
            usa_data = get_live_data_country("usa")
            date = datetime.now()
            for x in data_refresh.items():
                data = {"Data": data_refresh["Global"]}

            for k, v in data.items():

                recovered_data = "Recovered : {}".format(v["TotalRecovered"])
                confirmed_data = "Confirmed : {}".format(v["TotalConfirmed"])
                death_data = "Deaths : {}".format(v["TotalDeaths"])
                date_data = "Last Refreshed On : {}".format(
                    date.strftime("%m/%d/%Y, %H:%M")
                )
            self.rocover_label.setText(recovered_data)
            self.confirmed_label.setText(confirmed_data)
            self.death_label.setText(death_data)
            self.date_label.setText(date_data)
            for a in usa_data.items():
                data = {
                    "Confirmed": usa_data["Confirmed"],
                    "Recovered": usa_data["Recovered"],
                    "Deaths": usa_data["Deaths"],
                    "Date": usa_data["Date"],
                }
            for i in data.items():
                fin = {"Data": data}
            for k, v in fin.items():
                recovered_data = "Recovered : {}".format(v["Recovered"])
                confirmed_data = "Confirmed : {}".format(v["Confirmed"])
                death_data = "Deaths : {}".format(v["Deaths"])
                date_data = "Last Refreshed On : {}".format(
                    date.strftime("%m/%d/%Y, %H:%M")
                )
            self.recover2_label.setText(recovered_data)
            self.cnfrm_label_2.setText(confirmed_data)
            self.death_label_2.setText(death_data)
            self.date_label_2.setText(date_data)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Data Updated Successfully. ")
            msg.setWindowTitle("Refresh Done")
            msg.exec_()

    def retrieve_country_data(self):
        country_name = self.lineEdit.text()
        country_data_retrieve = get_live_data_country(country_name)
        if country_data_retrieve is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Invalid Country! Please try again! ")
            msg.setWindowTitle("Error")
            msg.exec_()
        else:

            for b in country_data_retrieve.items():

                data = {
                    "Country": country_data_retrieve["Country"],
                    "Confirmed": country_data_retrieve["Confirmed"],
                    "Recovered": country_data_retrieve["Recovered"],
                    "Deaths": country_data_retrieve["Deaths"],
                    "Active": country_data_retrieve["Active"],
                    "Date": country_data_retrieve["Date"],
                }

            for i, j in data.items():
                final_data = {"Data": data}
            for k, v in final_data.items():
                country = "Country Name : {}".format(v["Country"])
                recovered_data_country = "Recovered : {}".format(v["Recovered"])
                confirmed_data_country = "Confirmed : {}".format(v["Confirmed"])
                death_data_country = "Deaths : {}".format(v["Deaths"])
                active_data_country = "Active : {}".format(v["Active"])
                date_data_country = "Database Last Updated On : {}".format(v["Date"])
            self.country_name_lbl.setText(country)
            self.recv_coun_label.setText(recovered_data_country)
            self.death_country_label.setText(death_data_country)
            self.date_label_country.setText(date_data_country)
            self.active_cases_label.setText(active_data_country)
            self.cnfirm_country_label.setText(confirmed_data_country)
            self.pie_chart.setEnabled(True)

    def generate_pie_chart(self):
        country_name = self.lineEdit.text()
        country_data_retrieve = get_live_data_country(country_name)
        data_to_plot = data_extract(country_data_retrieve)
        labels = ["Confirmed", "Deaths", "Recovered", "Active"]
        pie_chart = generate_pie_chart(data=data_to_plot, labels=labels)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())