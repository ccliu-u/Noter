# -*- coding: utf-8 -*-
# 左侧面板

from PyQt5.QtWidgets import QFrame, QVBoxLayout

from helper.qlabel_img import QLabelImg
from tools.config import Const
from tools.signal import SignalManager


class LeftFrame(QFrame):

    def __init__(self):
        super(LeftFrame, self).__init__()

        v_layout = QVBoxLayout()

        self.signal = SignalManager()

        label_img_book = QLabelImg(Const.book_icon_path, press_event_fn=lambda: self.icon_clicked(1))
        label_img_folder = QLabelImg(Const.folder_icon_path, press_event_fn=lambda: self.icon_clicked(2))

        v_layout.addStretch(1)
        v_layout.addWidget(label_img_book)
        v_layout.addSpacing(30)
        v_layout.addWidget(label_img_folder)
        v_layout.addStretch(30)

        self.setLayout(v_layout)

    def icon_clicked(self, icon_index):
        # 发出信号，传递图标索引
        self.signal.left_page_signal.emit(icon_index)
