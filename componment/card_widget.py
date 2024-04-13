# -*- coding: utf-8 -*-
# 中间栏的笔记卡片，显示名称、描述信息、最近修改时间，并具有点击事件的功能

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QFrame, \
    QMenu, QAction, QMessageBox, QInputDialog, QFileDialog
    
from PyQt5.QtCore import Qt, pyqtSignal
import os
import shutil
import markdown2
# from weasyprint import HTML

from tools.config import GlobalContext, Const

# GTK_FOLDER = r'C:\Program Files\GTK3-Runtime Win64\bin'
# os.environ['PATH'] = GTK_FOLDER + os.pathsep + os.environ.get('PATH', '')


class CardWidget(QFrame):
    middle_page_signal = pyqtSignal(str)                            # 中间栏笔记选择信号

    def __init__(self, name: str, desc: str, time: str):
        super(CardWidget, self).__init__()

        self.middle_page_signal.connect(self.show_note_content)
        self.chosen = False

        self.setFixedHeight(120)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.grid_layout = QGridLayout()

        self.name = name

        if len(name) > 8:
            name = name[:8-3] + '…'
        if len(desc) > 18:
            desc = desc[:18-3] + '…'
        
        self.name_label = QLabel(name)
        self.name_label.setFont(QFont("Arial", 11, QFont.Bold))    # 设置标题字体、大小和加粗

        self.desc_label = QLabel(desc)
        self.desc_label.setFont(QFont("Arial", 9))

        self.time_label = QLabel(time)
        self.time_label.setStyleSheet("color: #808080;")           # 设置字体颜色为灰色
        
        # 名称
        self.grid_layout.addWidget(self.name_label, 0, 0)
        # 简介
        self.grid_layout.addWidget(self.desc_label, 1, 0)
        # 时间
        self.grid_layout.addWidget(self.time_label, 2, 0)

        self.setLayout(self.grid_layout)

        self.setObjectName("CardWidgetFrame")
        self.setStyleSheet("#CardWidgetFrame{border:1px solid #9b7576;border-radius:10px;;margin-top:2cm;}")

        # 创建右键菜单
        self.menu = QMenu(self)
        self.rename_action = QAction("重命名", self)
        self.delete_action = QAction("删除", self)
        self.export_action = QAction("导出", self)
        self.menu.addAction(self.rename_action)
        self.menu.addAction(self.delete_action)
        self.menu.addAction(self.export_action)

        # 连接右键菜单的动作
        self.rename_action.triggered.connect(self.rename)
        self.delete_action.triggered.connect(self.delete)
        self.export_action.triggered.connect(self.export)


    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(a0)
        self.middle_page_signal.emit(self.name)                # 发送信号

    def show_note_content(self, name):
        GlobalContext.right_frame().choose_markdown(name)
        GlobalContext.middle_frame().choose_card(name)

    
    def update_edit_time(self, time):
        self.time_label.setText(time)
    
    def updateStyle(self, flag):
        '''
        根据选中是否突出显示
        '''
        if flag:
            self.chosen = True
            self.setStyleSheet("#CardWidgetFrame{background-color: #353F4D;border:1px solid #9b7576;border-radius:10px;;margin-top:2cm;}")  # 突出
            self.name_label.setStyleSheet("background-color: #353F4D;")
            self.desc_label.setStyleSheet("background-color: #353F4D;")
            self.time_label.setStyleSheet("background-color: #353F4D;")
        else:
            self.chosen = False
            self.setStyleSheet("#CardWidgetFrame{border:1px solid #9b7576;border-radius:10px;;margin-top:2cm;}")                        # 取消突出
            self.name_label.setStyleSheet("background-color: #19232D;")
            self.desc_label.setStyleSheet("background-color: #19232D;")
            self.time_label.setStyleSheet("background-color: #19232D;color: #808080;")

    def enterEvent(self, event):
        '''
        鼠标悬停
        '''
        self.setStyleSheet("#CardWidgetFrame{background-color: #353F4D;border:1px solid #9b7576;border-radius:10px;;margin-top:2cm;}")     # 突出
        self.name_label.setStyleSheet("background-color: #353F4D;")
        self.desc_label.setStyleSheet("background-color: #353F4D;")
        self.time_label.setStyleSheet("background-color: #353F4D;")


    def leaveEvent(self, event):
        '''
        鼠标离开
        '''
        if self.chosen is not True:
            self.setStyleSheet("#CardWidgetFrame{border:1px solid #9b7576;border-radius:10px;;margin-top:2cm;}")                        # 取消突出
            self.name_label.setStyleSheet("background-color: #19232D;")
            self.desc_label.setStyleSheet("background-color: #19232D;")
            self.time_label.setStyleSheet("background-color: #19232D;color: #808080;")


    def contextMenuEvent(self, event):
        # 在鼠标右键点击时显示菜单
        self.menu.exec_(event.globalPos())


    ########################################################
    ####                右键菜单功能函数                 ####
    ########################################################
        
    def rename(self):
        new_name, ok_pressed = QInputDialog.getText(self, "重命名", f"输入新的笔记名:")
        if ok_pressed and new_name:
            old_name = self.name
            self.name_label.setText(new_name)
            self.name = new_name

            # 修改本地文件名
            old_file_path = os.path.join(Const.notes_path, old_name + '.md')
            new_file_path = os.path.join(Const.notes_path, new_name + '.md')
            os.rename(old_file_path, new_file_path)

            # 修改notes_list中的文件
            with open(Const.knowledge_folder_path, mode='r+', encoding='utf-8') as f:
                # 笔记名称&&笔记简介&&创建时间&&最后修改时间
                lines = f.readlines()
                for i, line in enumerate(lines):
                    parts = line.strip().split("&&")
                    if parts[0] == old_name:
                        parts[0] = new_name
                        lines[i] = "&&".join(parts) + "\n"
                        break
                f.seek(0)
                f.truncate(0)
                f.writelines(lines)

            # 修改全局变量
            GlobalContext.remove_instance(old_name)
            GlobalContext.setup(new_name, self)

            # 修改middle_fram的cur_choose
            GlobalContext.middle_frame().update_cur_choose(new_name)

            QMessageBox.information(self, '提示', '重命名成功！', QMessageBox.Ok)


    def delete(self):
        reply = QMessageBox.question(self, "删除", "确认删除这个笔记？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 删除本地文件
            file_path = os.path.join(Const.notes_path, self.name + '.md')
            os.remove(file_path)

            # 删除notes_list中的文件
            with open(Const.knowledge_folder_path, mode='r+', encoding='utf-8') as f:
                lines = f.readlines()
                f.seek(0)
                f.truncate(0)
                for line in lines:
                    parts = line.strip().split("&&")
                    if parts[0] != self.name:
                        f.write(line)
            
            GlobalContext.remove_instance(self.name)             # 删除全局变量
            GlobalContext.right_frame().init_ui()                # 关闭右侧面板的markdown页面
            GlobalContext.middle_frame().update_cur_choose("")   # 修改middle_fram的cur_choose
            QMessageBox.information(self, '提示', '删除成功！', QMessageBox.Ok)
            self.deleteLater()                                   # 删除这个 CardWidget 实例


    def export(self):
        '''
        导出为markdown、pdf、html、原始html
        '''
        file_path, _ = QFileDialog.getSaveFileName(self, "导出文件", "", "Markdown Files (*.md);;PDF Files (*.pdf);;HTML Files (*.html)")

        if not file_path:
            return
        
        cur = os.path.join(Const.notes_path, self.name + '.md')
        if file_path.endswith('.md'):
            shutil.copyfile(cur, file_path)
            '''
        elif file_path.endswith('.pdf'):
            try:
                html = markdown2.markdown_path(cur)
                os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
                HTML(string=html).write_pdf(file_path)
            except Exception as e:
                QMessageBox.information(self, '提示', '导出失败！', QMessageBox.Ok)
                '''
        elif file_path.endswith('.html'):
            html_content = markdown2.markdown_path(cur)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        else:
            QMessageBox.information(self, '提示', '不支持的文件类型！', QMessageBox.Ok)
            return
        QMessageBox.information(self, '提示', '导出成功！', QMessageBox.Ok)
        