# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QWidget

from componment.card_widget import CardWidget
from componment.cards_qthread import CardsThread
from helper.qlabel_img import QLabelImg
from tools.config import Const, GlobalContext
from tools.signal import SignalManager


class MiddleFrame(QFrame):
    card_fill_result_signal = pyqtSignal(str, str, str)   # 名称、描述、时间

    def __init__(self):
        super(MiddleFrame, self).__init__()

        self.signal = SignalManager()
        self.signal.left_page_signal.connect(self.update_content)
        self.setFrameShape(QFrame.StyledPanel)
        self.resize(Const.middle_frame_width, Const.default_window_height)
        self.setMinimumWidth(Const.middle_frame_width - 100)

        self.cur_choose = ""                             # 当前显示的笔记卡片

        # 垂直布局，h_layout标题和新建 + card_area滚动条
        v_layout = QVBoxLayout()

        # 水平布局，最上面
        h_layout = QHBoxLayout()
        self.label_title = QLabel('最近笔记')
        self.label_title.setObjectName('MiddleFrame_label_title')
        self.label_title.setStyleSheet("#MiddleFrame_label_title{font-size: 26px; font-weight: bold;}")

        # 新建笔记
        label_img = QLabelImg(img_path=Const.add_icon_path, press_event_fn=lambda: self.add_btn_fn())

        h_layout.addWidget(self.label_title)
        h_layout.addStretch(1)
        h_layout.addWidget(label_img)

        # 滚动条区域指定一个父面板，然后往这个父面板上添加子面板
        parent_card_widget = QWidget()
        card_area = QScrollArea()
        card_area.setWidget(parent_card_widget)                        # 绑定滚动条和父面板
        card_area.setWidgetResizable(True)
        card_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭横向

        # 网格布局
        self.q_v_layout = QVBoxLayout(parent_card_widget)
        self.q_v_layout.setAlignment(Qt.AlignTop)
        self.q_v_layout.setSpacing(10)

        self.fill_cards_1()

        v_layout.addLayout(h_layout)
        v_layout.addWidget(card_area)

        self.setLayout(v_layout)

    def fill_cards_1(self):
        """
        异步加载最近笔记区域的内容
        """
        self.card_fill_result_signal.connect(self.fill_cards_callback)
        self.fill_card_thread = CardsThread(self.card_fill_result_signal)
        self.fill_card_thread.start()

    def fill_cards_callback(self, title, desc, time):
        card = CardWidget(title, desc, time)
        self.q_v_layout.addWidget(card)
        GlobalContext.setup(title, card)

    def add_btn_fn(self):
        """
        显示增加弹出框
        """
        GlobalContext.add_dialog().show()

    def update_content(self, icon_index):
        """
        更新中部区域内容
        """
        if icon_index == 1:
            self.label_title.setText('最近笔记')
            self.fill_cards_1()
        elif icon_index == 2:
            self.label_title.setText('笔记库')
            self.fill_cards_2()
        else:
            pass

    def fill_cards_2(self):
        """
        异步加载文件夹区域的内容
        """
        '''
        self.card_fill_result_signal.connect(self.fill_cards_callback)
        self.fill_card_thread = CardsThread(self.card_fill_result_signal)
        self.fill_card_thread.start()
        '''

    def choose_card(self, name):
        if(name != self.cur_choose):
            GlobalContext.get_instance(name).updateStyle(True)
            if self.cur_choose != "":
                GlobalContext.get_instance(self.cur_choose).updateStyle(False)
            self.cur_choose = name


    def update_cur_choose(self, name):
        self.cur_choose = name