from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    finished = pyqtSignal()

    def run(self):
        # 在这里编写需要在后台线程执行的任务
        for i in range(5):
            print(f"Working... {i}")
            self.sleep(1)  # 模拟耗时任务
        self.finished.emit()  # 发送任务完成的信号

# 使用示例
worker = Worker()
worker.finished.connect(lambda: print("Task completed!"))  # 连接任务完成信号
worker.start()  # 启动线程执行任务
