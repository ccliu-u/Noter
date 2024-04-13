# -*- coding: utf-8 -*-
# 创建一个用于添加新条目的对话框,依附于中心窗口布局

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QTextEdit, QDialog, QHBoxLayout, QMessageBox
import datetime
import os

from componment.card_widget import CardWidget
from tools.config import GlobalContext, Const


class MiddleAddDialog(QDialog):

    def __init__(self, parent):
        super(MiddleAddDialog, self).__init__()

        self.setFixedSize(425, 325)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        # 设置窗口为模态，用户只有关闭弹窗后，才能关闭主界面
        self.setWindowModality(Qt.ApplicationModal)
        self.setParent(parent)

        self.name_label = QLabel('名称:')
        self.name_line = QLineEdit()

        self.desc_label = QLabel('简介:')
        self.desc_line = QTextEdit()

        self.h_layout = QHBoxLayout()
        self.add_btn = QPushButton('新建')
        self.add_btn.clicked.connect(lambda: self.add_slot())
        self.cancel_btn = QPushButton('取消')
        self.cancel_btn.clicked.connect(lambda: self.cancel_slot())
        self.h_layout.addWidget(self.cancel_btn)
        self.h_layout.addWidget(self.add_btn)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.name_label)
        self.v_layout.addWidget(self.name_line)
        self.v_layout.addWidget(self.desc_label)
        self.v_layout.addWidget(self.desc_line)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

        # 父窗体中心位置
        lmr_manager_center = parent.frameGeometry().center()

        self.move(QPoint(lmr_manager_center.x(), 0))
        # 设置了父窗体后此组件默认会显示，这里隐藏下
        self.close()

    def cancel_slot(self):
        self.name_line.setText('')
        self.desc_line.setText('')
        self.close()

    def add_slot(self):
        current_time = datetime.datetime.now()
        create_time = current_time.strftime("%Y-%m-%d %H:%M:%S")        # 格式化当前时间作为创建时间
        modify_time = create_time                                       # 初始创建时间即为最后修改时间

        # 检查笔记名称是否重复
        new_note_name = self.check_repetition()

        with open(Const.knowledge_folder_path, mode='a', encoding='utf-8') as f:
            # 笔记名称&&笔记简介&&创建时间&&最后修改时间
            note_info = f"{new_note_name}&&{self.desc_line.toPlainText()}&&{create_time}&&{modify_time}\n"
            f.write(note_info)

        filepath = os.path.join(Const.notes_path, new_note_name + '.md')
        with open(filepath, 'w', encoding='utf-8'):                     # 创建笔记文件
            pass
        
        QMessageBox.information(self, 'information', '新建成功！', QMessageBox.Ok)

        card = CardWidget(new_note_name, self.desc_line.toPlainText(), modify_time)
        GlobalContext.middle_frame().q_v_layout.insertWidget(0, card)
        GlobalContext.setup(new_note_name, card)
        self.name_line.setText('')
        self.desc_line.setText('')

        self.close()

    def check_repetition(self):
        """
        检查笔记名称是否重复
        """
        existing_notes = []
        with open(Const.knowledge_folder_path, 'r', encoding='utf-8') as f:
            for line in f:
                note_info = line.strip().split('&&')
                existing_notes.append(note_info[0])                     # 笔记名称在每行的第一个位置

        counter = 1
        new_note_name = self.name_line.text()
        while new_note_name in existing_notes:
            new_note_name = f"{self.name_line.text()}({counter})"
            counter += 1

        return new_note_name