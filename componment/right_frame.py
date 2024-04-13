# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QTextEdit, QSplitter, \
    QTextBrowser, QToolBar, QAction, QFileDialog, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown2 as markdown
import mistune
import datetime

from tools.config import Const, GlobalContext
from tools.signal import SignalManager


class RightFrame(QFrame):

    def __init__(self):
        super(RightFrame, self).__init__()

        self.md_ui = False
        self.tittle = ""

        self.setFrameShape(QFrame.StyledPanel)
        self.resize(Const.right_frame_width, Const.default_window_height)
        self.setMinimumWidth(Const.right_frame_width)

        self.signal = SignalManager()
        self.signal.left_page_signal.connect(self.update_content)
        self.setObjectName("RightFrame")
        self.mdlayout = QVBoxLayout()                  # 垂直布局，工具栏保存+编辑预览
        self.setLayout(self.mdlayout)
        self.init_ui()
        

    def init_ui(self):
        if self.md_ui:                                 # 删除markdown布局
            # 清除布局1中的部件
            while self.layout1.count():
                item = self.layout1.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            # 清除布局2中的部件
            while self.layout2.count():
                item = self.layout2.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            # 清除主布局中的布局1和布局2
            while self.mdlayout.count():
                item = self.mdlayout.takeAt(0)
                if item.layout():
                    while item.layout().count():
                        nested_item = item.layout().takeAt(0)
                        if nested_item.widget():
                            nested_item.widget().deleteLater()
                elif item.widget():
                    item.widget().deleteLater()

            del self.layout1
            del self.layout2

            self.md_ui = False
        self.setStyleSheet("#RightFrame{border-image:url(:assets/3.png);}")


    def update_content(self, icon_index):
        if icon_index == 1:
            self.editor.show()
        elif icon_index == 2:
            pass

            
    def save_markdown(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = os.path.join(Const.notes_path, self.tittle + '.md')
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(self.editor.toPlainText())

        # 修改最后更新时间
        with open(Const.knowledge_folder_path, mode='r+', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                parts = line.strip().split("&&")
                if parts[0] == self.tittle:
                    parts[3] = current_time
                    lines[i] = "&&".join(parts) + "\n"
                    lines.insert(0, lines.pop(i))           # 最近编辑文件优先
                    break
            f.seek(0)
            f.truncate(0)
            f.writelines(lines)
        
        # 置于最近编辑文件的最前面
        card = GlobalContext.get_instance(self.tittle)
        index = GlobalContext.middle_frame().q_v_layout.indexOf(card)
        if index != -1:
            GlobalContext.middle_frame().q_v_layout.removeWidget(card)
            GlobalContext.middle_frame().q_v_layout.insertWidget(0, card)

        # 更新列表时间
        card.update_edit_time(current_time)
        


    def preview_markdown(self):
        '''
        渲染Markdown文本
        '''
        markdown_text = self.editor.toPlainText()
        html = markdown.markdown(markdown_text)
        self.viewer.setHtml(html)


    def choose_markdown(self, name):
        self.markdown_ui()
        self.tittle = name
        file_path = os.path.join(Const.notes_path, name + '.md')

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        self.editor.setPlainText(content)                       # 将内容加载到 编辑框 中

        self.editor.textChanged.connect(self.preview_markdown)  # 实时预览Markdown


    def markdown_ui(self):
        if self.md_ui:
            return
    
        self.layout1 = QHBoxLayout()   # 水平布局，工具栏+保存等
        self.layout2 = QHBoxLayout()   # 水平布局，编辑+预览

        # Markdown编辑框
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Arial", 12))   # 设置字体大小

        # 渲染Markdown结果
        self.viewer = QTextBrowser()
        self.viewer.setFont(QFont("Arial", 12))   # 设置字体大小
        self.viewer.setStyleSheet("QTextBrowser { line-height: 1.5; }")   # 设置行高

        # 拖动调整大小
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.viewer)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        self.layout2.addWidget(splitter)

        # 创建工具栏
        toolbar = QToolBar()
        self.layout1.addWidget(toolbar)
        toolbar.setStyleSheet("QToolButton { padding: 6px; }")

        # 创建动作（加粗、斜体、插入图片）
        undo_action = QAction(QIcon(Const.undo_icon_path), "Undo", self)
        undo_action.setToolTip("撤销")
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.editor.undo)
        toolbar.addAction(undo_action)

        redo_action = QAction(QIcon(Const.redo_icon_path), "重做", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.editor.redo)
        toolbar.addAction(redo_action)

        separator_action = QAction(self)
        separator_action.setSeparator(True)
        toolbar.addAction(separator_action)

        bold_action = QAction(QIcon(Const.bold_icon_path), "加粗", self)
        bold_action.setShortcut("Ctrl+B")
        bold_action.triggered.connect(self.make_bold)
        toolbar.addAction(bold_action)

        italic_action = QAction(QIcon(Const.italic_icon_path), "倾斜", self)
        italic_action.setShortcut("Ctrl+I")
        italic_action.triggered.connect(self.make_italic)
        toolbar.addAction(italic_action)

        delete_action = QAction(QIcon(Const.strikethrough_icon_path), "删除线", self)
        delete_action.triggered.connect(self.make_delete)
        toolbar.addAction(delete_action)

        quote_action = QAction(QIcon(Const.quote_icon_path), "引用", self)
        quote_action.triggered.connect(self.make_quote)
        toolbar.addAction(quote_action)

        separator_action2 = QAction(self)
        separator_action2.setSeparator(True)
        toolbar.addAction(separator_action2)

        bl_action = QAction(QIcon(Const.bl_icon_path), "无序列表", self)
        bl_action.triggered.connect(lambda: self.editor.insertPlainText("- "))
        toolbar.addAction(bl_action)

        ol_action = QAction(QIcon(Const.ol_icon_path), "有序列表", self)
        ol_action.triggered.connect(lambda: self.editor.insertPlainText("1. "))
        toolbar.addAction(ol_action)

        cl_action = QAction(QIcon(Const.checklist_icon_path), "清单", self)
        cl_action.triggered.connect(lambda: self.editor.insertPlainText("- [ ] "))
        toolbar.addAction(cl_action)

        separator_action3 = QAction(self)
        separator_action3.setSeparator(True)
        toolbar.addAction(separator_action3)

        link_action = QAction(QIcon(Const.link_icon_path), "链接", self)
        link_action.triggered.connect(lambda: self.editor.insertPlainText("[链接](url)"))
        toolbar.addAction(link_action)

        insert_image_action = QAction(QIcon(Const.image_icon_path), "插入图片", self)
        insert_image_action.triggered.connect(self.insert_image)
        toolbar.addAction(insert_image_action)

        code_action = QAction(QIcon(Const.code_icon_path), "代码", self)
        code_action.triggered.connect(lambda: self.editor.insertPlainText("```python\n\n```"))
        toolbar.addAction(code_action)

        table_action = QAction(QIcon(Const.table_icon_path), "表格", self)
        table_action.triggered.connect \
            (lambda: self.editor.insertPlainText \
             ("| Column 1 | Column 2 | Column 3 |\n| -------- | -------- | -------- |\n| Text     | Text     | Text     |"))
        toolbar.addAction(table_action)

        # 添加保存按钮
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer.setStyleSheet("background-color: #455364;")
        toolbar.addWidget(spacer)

        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_markdown)
        save_action.setFont(QFont("Arial", weight=QFont.Bold))
        toolbar.addAction(save_action)

        self.mdlayout.addLayout(self.layout1)
        self.mdlayout.addLayout(self.layout2)

        # 实时预览Markdown
        self.editor.textChanged.connect(self.preview_markdown)

        self.md_ui = True



    ########################################################
    ####                 工具栏相关函数                  ####
    ########################################################
        
    def make_bold(self):
        '''
        加粗
        '''
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            return
        selected_text = cursor.selectedText()
        # 若未加粗，则加粗；若已加粗，则取消加粗
        if selected_text.startswith("**") and selected_text.endswith("**"):
            cursor.insertText(selected_text[2:-2])
        else:
            cursor.insertText(f"**{selected_text}**")


    def make_italic(self):
        '''
        斜体
        '''
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            return
        selected_text = cursor.selectedText()
        # 若未斜体，则斜体；若已斜体，则取消斜体
        if selected_text.startswith("*") and selected_text.endswith("*"):
            cursor.insertText(selected_text[1:-1])
        else:
            cursor.insertText(f"*{selected_text}*")


    def insert_image(self):
        '''
        插入图片
        '''
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.gif)")
        if fileName:
            image_name = os.path.basename(fileName)
            image_path = os.path.join(os.getcwd(), image_name)
            os.rename(fileName, image_path)  # 将图片移动到代码目录下
            markdown_image = f"![{image_name}]({image_name})"
            cursor = self.editor.textCursor()
            cursor.insertText(markdown_image)


    def make_delete(self):
        '''
        删除线
        '''
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            return
        selected_text = cursor.selectedText()
        # 若未删除线，则删除线；若已删除线，则取消删除线
        if selected_text.startswith("~~") and selected_text.endswith("~~"):
            cursor.insertText(selected_text[2:-2])
        else:
            cursor.insertText(f"~~{selected_text}~~")


    def make_quote(self):
        '''
        引用
        '''
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.insertText("> ")
            return
        selected_text = cursor.selectedText()
        # 若未引用，则引用；若已引用，则取消引用
        if selected_text.startswith("> "):
            cursor.insertText(selected_text[2:])
        else:
            cursor.insertText(f"> {selected_text}")
