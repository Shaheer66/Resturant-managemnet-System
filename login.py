from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QApplication, QLabel, QLineEdit, QVBoxLayout,
                             QHBoxLayout, QWidget, QFrame, QPushButton)
from PyQt5.QtCore import (QRect, Qt)
from PyQt5.QtCore import Qt

from Admin import Admin
from appname import AppName
# from sidebar import Sidebar
from footer import Footer

import sidebar

from classes2.db import DB

import functools


class Login(QMainWindow):

    def __init__(self):
        super().__init__()

        self.db = DB()

        self.initUI()

    def initUI(self):

        # sidebar = Sidebar(self)
        #self.addDockWidget(Qt.LeftDockWidgetArea, sidebar)

        header = AppName("RSM")
        footer = Footer()

        layout = QVBoxLayout()

        username_row = QHBoxLayout()
        password_row = QHBoxLayout()
        login_btn = QHBoxLayout()
        errorMsg = QHBoxLayout()

        self.labelUsername = QLabel("Username")
        self.usernameInput = QLineEdit()
        self.usernameInput.setFixedWidth(300)

        self.labelPassword = QLabel("Password")
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)

        self.passwordInput.setFixedWidth(300)

        self.loginBtn = QPushButton("Login")
        self.loginBtn.setFixedWidth(200)
        self.loginBtn.setFocusPolicy(Qt.StrongFocus)
        self.loginBtn.setShortcut("Return")
        self.loginBtn.clicked.connect(self.loginBtnClicked)

        self.loginErrorMsg = QLabel("")

        username_row.addStretch()
        username_row.addWidget(self.labelUsername)
        username_row.addWidget(self.usernameInput)
        username_row.addStretch()

        password_row.addStretch()
        password_row.addWidget(self.labelPassword)
        password_row.addWidget(self.passwordInput)
        password_row.addStretch()

        login_btn.addStretch()
        login_btn.addWidget(self.loginBtn)
        login_btn.addStretch()

        errorMsg.addStretch()
        errorMsg.addWidget(self.loginErrorMsg)
        errorMsg.addStretch()

        layout.addWidget(header)
        # layout.addWidget(frame)
        layout.addStretch()
        layout.addLayout(username_row)
        layout.addLayout(password_row)
        layout.addLayout(login_btn)
        layout.addLayout(errorMsg)
        layout.addStretch()
        layout.addWidget(footer)

        layout.setContentsMargins(0, 0, 0, 0)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)
        self.setContentsMargins(0, 0, 0, 0)

        self.resize(800, 600)
        self.setWindowTitle("RSM")
        self.show()

        self.center()

    def loginBtnClicked(self):
        admin = Admin()

        checkLogin = admin.login(self.usernameInput.text(), self.passwordInput.text())

        if checkLogin:
            if admin.is_admin == 'yes':  # Check if the user is an admin
                query = "update user set logged_in='yes' where user_name=%s"
                values = (self.usernameInput.text(),)
                data = self.db.execute(query, values)

                self.hide()
                loggedin = sidebar.Dashboard(self)
            else:
                query = "update user set logged_in='yes' where user_name=%s"
                values = (self.usernameInput.text(),)
                data = self.db.execute(query, values)

                self.hide()
                loggedin = sidebar.Dashboard(self)  # Create a UserDashboard class for regular users
        else:
            self.loginErrorMsg.setText("Incorrect Combination")



    def center(self):
        '''centers the window on the screen'''
        #print ("Center reported")
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
          int((screen.height() - size.height()) / 2))
