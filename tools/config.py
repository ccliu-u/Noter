# -*- coding: utf-8 -*-

import importlib
from collections import OrderedDict

# 动态导入，不然格式化会删掉没有显式调用的代码
try:
    importlib.import_module('tools.assets')
except ImportError as e:
    from tools import assets


class Const(object):
    # 默认窗口宽度
    default_window_width = 1275
    # 默认窗口高度
    default_window_height = 685
    # 最小窗口宽度
    min_window_width = 1150
    # 最小窗口高度
    min_window_height = 550
    # 左侧固定宽度
    left_frame_width = 55
    # 中部宽度
    middle_frame_width = 465
    # 右侧宽度
    right_frame_width = default_window_width - left_frame_width - middle_frame_width

    # 工程名
    project_name = 'Notes'
    # 启动图
    window_start_path = ':assets/window_start.jpeg'
    # 窗口图
    window_icon_path = ':assets/window_icon.png'
    # 退出图
    exit_img_path = ':assets/exit.svg'
    # 日志图
    log_img_path = ':assets/log.svg'
    # 系统托盘图
    tray_icon_path = ':assets/window_icon.png'
    # 左侧窗体图标
    book_icon_path = ':assets/book2.png'
    # 左侧设置图标
    setting_icon_path = ':assets/setting2.svg'
    # 左侧文件夹图标
    folder_icon_path = ':assets/folder.png'
    # 中部增加图标
    add_icon_path = ':assets/add.svg'

    right_bg_path = ':assets/right_bg.png'

    # 主窗口
    key_main_window = 'main_window'
    # 中心区域
    key_lmr_manager = 'lmr_manager'
    # 日志窗口
    key_log_view = 'log_view'
    # 系统托盘
    key_tray_view = 'tray_view'
    # 中心区域添加
    key_add_dialog = 'add_dialog'
    # 左部
    key_left_frame = 'left_frame'
    # 中部
    key_middle_frame = 'middle_frame'
    # 右部
    key_right_frame = 'right_frame'

    # 笔记列表存储
    knowledge_folder_path = ':/../notes/notes_list.txt'
    # 笔记存储
    notes_path = ':/../notes/'

    '''工具栏图标'''
    # 加粗
    bold_icon_path = ':assets/bold.png'
    # 斜体
    italic_icon_path = ':assets/italic.png'
    # 插入图片
    image_icon_path = ':assets/picture.png'
    # 撤回
    undo_icon_path = ':assets/undo.png'
    # 重做 
    redo_icon_path = ':assets/redo.png'
    # 删除线
    strikethrough_icon_path = ':assets/strikethrough.png'
    # 引用
    quote_icon_path = ':assets/quote.png'
    # 无序列表
    bl_icon_path = ':assets/bullet-list.png'
    # 有序列表
    ol_icon_path = ':assets/number.png'
    # 链接
    link_icon_path = ':assets/url.png'
    # 代码
    code_icon_path = ':assets/code.png'
    # 清单
    checklist_icon_path = ':assets/checklist.png'
    # 表格
    table_icon_path = ':assets/calendar.png'
    # 分割线
    line_icon_path = ':assets/line.png'

    # 保存
    save_icon_path = ':assets/save.png'


class GlobalContext(object):
    _dict = OrderedDict()

    def __init__(self):
        super().__init__()

    @staticmethod
    def setup(key: str, value: object):
        GlobalContext._dict[key] = value

    @staticmethod
    def get_instance(key: str) -> object: 
        return GlobalContext._dict.get(key)
    
    def remove_instance(key: str):
        if key in GlobalContext._dict:
            del GlobalContext._dict[key]

    @staticmethod
    def main_window():
        return GlobalContext.get_instance(Const.key_main_window)

    @staticmethod
    def lmr_manager():
        return GlobalContext.get_instance(Const.key_lmr_manager)

    @staticmethod
    def log_view():
        return GlobalContext.get_instance(Const.key_log_view)

    @staticmethod
    def tray_view():
        return GlobalContext.get_instance(Const.key_tray_view)

    @staticmethod
    def add_dialog():
        return GlobalContext.get_instance(Const.key_add_dialog)

    @staticmethod
    def middle_frame():
        return GlobalContext.get_instance(Const.key_middle_frame)

    @staticmethod
    def right_frame():
        return GlobalContext.get_instance(Const.key_right_frame)
