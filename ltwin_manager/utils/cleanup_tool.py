"""
环境清理工具
"""

import os
import shutil
import glob


class CleanupTool:
    """环境清理工具类"""
    
    @staticmethod
    def clear_user_directories(home_path: str = None) -> bool:
        """
        清除用户目录中的特定文件
        :param home_path: 用户主目录路径
        :return: 是否成功
        """
        if not home_path:
            home_path = os.path.expanduser('~')
        
        try:
            # 查找并删除以.开头的隐藏文件/目录
            hidden_paths = glob.glob(os.path.join(home_path, '.*'))
            for path in hidden_paths:
                if os.path.isdir(path) and os.path.basename(path) not in ['.', '..']:
                    # 跳过重要的系统隐藏目录
                    if os.path.basename(path) not in ['.ssh', '.config', '.cache', '.local']:
                        shutil.rmtree(path)
                elif os.path.isfile(path):
                    os.remove(path)
            return True
        except Exception as e:
            print(f"清除用户目录失败: {e}")
            return False

    @staticmethod
    def clear_application_dirs(base_path: str = None) -> bool:
        """
        清除应用程序目录
        :param base_path: 基础路径
        :return: 是否成功
        """
        if not base_path:
            base_path = os.path.expanduser('~')
        
        try:
            app_path = os.path.join(base_path, 'myapp')
            if os.path.exists(app_path) and os.path.isdir(app_path):
                shutil.rmtree(app_path)
            return True
        except Exception as e:
            print(f"清除应用程序目录失败: {e}")
            return False

    @staticmethod
    def clear_flutter_dirs(base_path: str = None) -> bool:
        """
        清除Flutter相关文件
        :param base_path: 基础路径
        :return: 是否成功
        """
        if not base_path:
            base_path = os.path.expanduser('~')
        
        try:
            flutter_path = os.path.join(base_path, 'flutter')
            if os.path.exists(flutter_path) and os.path.isdir(flutter_path):
                shutil.rmtree(flutter_path)
            return True
        except Exception as e:
            print(f"清除Flutter目录失败: {e}")
            return False

    @staticmethod
    def reset_vm_snapshots(config_manager) -> bool:
        """
        重置虚拟机快照
        :param config_manager: 配置管理器
        :return: 是否成功
        """
        try:
            # TODO: 实现虚拟机快照重置逻辑
            print("重置虚拟机快照...")
            return True
        except Exception as e:
            print(f"重置虚拟机快照失败: {e}")
            return False

    @staticmethod
    def reset_configuration_files(config_manager) -> bool:
        """
        重置配置文件
        :param config_manager: 配置管理器
        :return: 是否成功
        """
        try:
            # TODO: 实现配置文件重置逻辑
            print("重置配置文件...")
            return True
        except Exception as e:
            print(f"重置配置文件失败: {e}")
            return False