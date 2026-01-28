"""
下载镜像对话框
"""

import sys
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QProgressBar,
                             QGroupBox, QFormLayout, QApplication, QWidget, QCheckBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont


class DownloadImagesDialog(QDialog):
    def __init__(self, config_manager=None, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle('下载镜像')
        self.setModal(True)
        self.resize(600, 500)
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel('下载镜像文件')
        title_label.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # 镜像类型选择
        group_box = QGroupBox('选择要下载的镜像')
        group_layout = QFormLayout()
        
        self.download_win_checkbox = QCheckBox('下载Tiny10镜像 (tiny10b4x64.iso)')
        self.download_win_checkbox.setChecked(True)
        group_layout.addRow(self.download_win_checkbox)
        
        self.download_virtio_checkbox = QCheckBox('下载VirtIO驱动镜像 (virtio-win.iso)')
        self.download_virtio_checkbox.setChecked(True)
        group_layout.addRow(self.download_virtio_checkbox)
        
        self.download_chrome_checkbox = QCheckBox('下载Chrome安装镜像 (Chrome.iso)')
        self.download_chrome_checkbox.setChecked(False)
        group_layout.addRow(self.download_chrome_checkbox)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        # 下载路径设置
        path_group = QGroupBox('下载路径')
        path_layout = QFormLayout()
        
        self.win_iso_path = QLineEdit(os.path.join(os.getcwd(), 'downloads', 'tiny10b4x64.iso'))
        self.virtio_iso_path = QLineEdit(os.path.join(os.getcwd(), 'downloads', 'virtio-win.iso'))
        self.chrome_iso_path = QLineEdit(os.path.join(os.getcwd(), 'downloads', 'Chrome.iso'))
        
        path_layout.addRow('Tiny10镜像:', self.win_iso_path)
        path_layout.addRow('VirtIO驱动:', self.virtio_iso_path)
        path_layout.addRow('Chrome镜像:', self.chrome_iso_path)
        
        path_group.setLayout(path_layout)
        layout.addWidget(path_group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 状态显示
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(150)
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.download_btn = QPushButton('开始下载')
        self.download_btn.clicked.connect(self.start_download)
        
        self.cancel_btn = QPushButton('取消')
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.download_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def start_download(self):
        """开始下载进程"""
        self.download_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        
        # 获取选中的下载项
        downloads = []
        if self.download_win_checkbox.isChecked():
            # Tiny10镜像下载链接
            win_url = "http://7.b.0.5.0.7.4.0.1.0.0.2.ip6.arpa/dl/iso/tiny10b4x64.iso"
            downloads.append(('tiny10', win_url, self.win_iso_path.text()))
        if self.download_virtio_checkbox.isChecked():
            # VirtIO驱动下载链接
            virtio_url = "http://7.b.0.5.0.7.4.0.1.0.0.2.ip6.arpa/dl/iso/virtio-win.iso"
            downloads.append(('virtio', virtio_url, self.virtio_iso_path.text()))
        if self.download_chrome_checkbox.isChecked():
            # Chrome安装镜像下载链接
            chrome_url = "https://archive.org/download/chrome_20240526/Chrome.iso"
            downloads.append(('chrome', chrome_url, self.chrome_iso_path.text()))
            
        if not downloads:
            self.status_text.append('请至少选择一个要下载的镜像')
            self.download_btn.setEnabled(True)
            self.progress_bar.setVisible(False)
            return
            
        # 导入下载线程
        from ..utils.image_download_thread import ImageDownloadThread
        
        # 创建并启动下载线程
        self.download_thread = ImageDownloadThread(downloads)
        self.download_thread.started.connect(self.on_download_start)
        self.download_thread.progress.connect(self.on_download_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        
        self.download_thread.start()
    
    def on_download_start(self, message):
        """下载开始回调"""
        self.status_text.append(message)
    
    def on_download_progress(self, percentage, message):
        """下载进度回调"""
        self.progress_bar.setValue(int(percentage))
        self.status_text.append(message)
    
    def on_download_finished(self, message, success):
        """下载完成回调"""
        if success:
            self.status_text.append(f'✓ {message}')
        else:
            self.status_text.append(f'✗ {message}')
        
        # 检查是否所有下载都已完成
        # 简单起见，在这里重新启用按钮
        self.download_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        if success:
            self.progress_bar.setValue(100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DownloadImagesDialog()
    dialog.exec()
    sys.exit(app.exec())