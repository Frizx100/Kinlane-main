# Form implementation generated from reading ui file 'c:\Users\Frizx\Desktop\Kinlane-main\client\app\ui/forms\playlist.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 366)
        Form.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        Form.setWindowOpacity(1.0)
        Form.setAutoFillBackground(False)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layout = QtWidgets.QWidget(parent=Form)
        self.layout.setAutoFillBackground(False)
        self.layout.setStyleSheet("")
        self.layout.setObjectName("layout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layout)
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalWidget = QtWidgets.QWidget(parent=self.layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.verticalWidget.setMinimumSize(QtCore.QSize(310, 173))
        self.verticalWidget.setAutoFillBackground(True)
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 15, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dop = QtWidgets.QLabel(parent=self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dop.sizePolicy().hasHeightForWidth())
        self.dop.setSizePolicy(sizePolicy)
        self.dop.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.dop.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing)
        self.dop.setObjectName("dop")
        self.verticalLayout.addWidget(self.dop)
        self.verticalLayout_3.addWidget(self.verticalWidget)
        self.title = QtWidgets.QLabel(parent=self.layout)
        self.title.setObjectName("title")
        self.verticalLayout_3.addWidget(self.title)
        self.description = QtWidgets.QLabel(parent=self.layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy)
        self.description.setObjectName("description")
        self.verticalLayout_3.addWidget(self.description)
        self.verticalLayout_2.addWidget(self.layout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.dop.setText(_translate("Form", "Time"))
        self.title.setText(_translate("Form", "TextLabel"))
        self.description.setText(_translate("Form", "TextLabel"))
