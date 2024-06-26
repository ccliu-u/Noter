# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp, QApplication
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget

from componment.lmr_mgr import LmrManager
from componment.log_view import LogView
from componment.middle_add_widget import MiddleAddDialog
from componment.tray_view import TrayView
from tools.config import Const, GlobalContext


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # 全局上下文
        self.context = GlobalContext()

        # 日志窗口
        self.log_view = LogView()
        self.context.setup(Const.key_log_view, self.log_view)

        self.log_view.info('[*] 初始化窗口')
        self.init_window()

        # 系统托盘
        self.tray_view = TrayView()
        self.context.setup(Const.key_tray_view, self.tray_view)

        self.log_view.info('[*] 初始化菜单栏')
        self.init_menu()

        self.log_view.info('[*] 初始化状态栏')
        self.init_status_bar()

        self.log_view.info('[*] 初始化中心区域')
        self.init_central_area()

    def init_window(self):
        """
        初始化窗口
        """
        self.resize(Const.default_window_width, Const.default_window_height)
        self.setMinimumSize(Const.min_window_width, Const.min_window_height)
        self.setWindowTitle('Noter')
        self.center()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        QApplication.setQuitOnLastWindowClosed(True)           # 最后一个窗口点击关闭后不退出程序
        self.context.setup(Const.key_main_window, self)

    def closeEvent(self, event):
        """
        点击X时隐藏主面板并显示系统托盘
        """
        self.hide()
        self.tray_view.show()
        event.ignore()

    def init_menu(self):
        """
        初始化菜单栏
        """
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&文件')

        log_act = QAction(QIcon(Const.log_img_path), '&查看日志', self)
        log_act.setStatusTip('查看日志')
        log_act.triggered.connect(lambda: self.log_view.show())
        file_menu.addAction(log_act)

        exit_act = QAction(QIcon(Const.exit_img_path), '&退出', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('退出')
        exit_act.triggered.connect(qApp.quit)
        file_menu.addAction(exit_act)

    def init_status_bar(self):
        """
        初始化状态栏
        """
        pass

    def init_central_area(self):
        """
        初始化中心区域
        """
        lmr_manager = LmrManager()
        self.setCentralWidget(lmr_manager)
        self.context.setup(Const.key_lmr_manager, lmr_manager)
        self.context.setup(Const.key_left_frame, lmr_manager.left_frame)
        self.context.setup(Const.key_middle_frame, lmr_manager.middle_frame)
        self.context.setup(Const.key_right_frame, lmr_manager.right_frame)

        lmr_manager.middle_frame.signal.connect_signals(lmr_manager.left_frame.signal)
        lmr_manager.right_frame.signal.connect_signals(lmr_manager.left_frame.signal)
        # 加号点击后出现的面板
        middle_add_dialog = MiddleAddDialog(lmr_manager)
        self.context.setup(Const.key_add_dialog, middle_add_dialog)

    def center(self):
        """
        居中窗口
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
