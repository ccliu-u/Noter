from PyQt5.QtCore import QObject, pyqtSignal

class SignalManager(QObject):
    left_page_signal = pyqtSignal(int)  # 左栏图标点击信号，切换: 1最近笔记 - 2文件夹

    def __init__(self):
        super(SignalManager, self).__init__()
        self.left_page_signal.emit(1)

    def connect_signals(self, signal: 'SignalManager'):
        self.left_page_signal.connect(signal.left_page_signal)