"""
镜像下载管理器
"""

import os
import urllib.request
from PyQt6.QtCore import QThread, pyqtSignal


class ImageDownloadThread(QThread):
    """
    用于下载镜像文件的后台线程
    """
    # 信号定义
    started = pyqtSignal(str)          # 开始下载通知
    progress = pyqtSignal(int, str)    # 进度更新 (percentage, message)
    finished = pyqtSignal(str, bool)   # 完成通知 (message, success)
    
    def __init__(self, download_items):
        """
        初始化下载线程
        :param download_items: 下载项列表，每个元素为 (type, url, path) 的元组
        """
        super().__init__()
        self.download_items = download_items
        
    def run(self):
        """执行下载任务"""
        for item_type, url, path in self.download_items:
            try:
                self.started.emit(f'开始下载 {item_type}...')
                
                # 确保目标目录存在
                os.makedirs(os.path.dirname(path), exist_ok=True)
                
                # 下载文件并监控进度
                urllib.request.urlretrieve(url, path, self._progress_hook)
                
                self.finished.emit(f'{item_type} 下载完成: {path}', True)
                
            except Exception as e:
                self.finished.emit(f'下载 {item_type} 失败: {str(e)}', False)
                return  # 停止后续下载
    
    def _progress_hook(self, block_num, block_size, total_size):
        """下载进度回调函数"""
        if total_size > 0:
            downloaded = block_num * block_size
            percentage = int(downloaded * 100 / total_size)
            self.progress.emit(percentage, f'已下载: {downloaded}/{total_size} bytes')