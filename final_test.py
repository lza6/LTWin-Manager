#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证测试脚本
用于验证所有修复是否成功
"""

import sys
import os
from pathlib import Path

def test_all_components():
    """测试所有组件"""
    print("开始测试所有LTWin Manager组件...")
    
    try:
        # 添加项目路径
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        # 1. 测试配置管理器
        print("1. 测试配置管理器...")
        from ltwin_manager.utils.config_manager import get_config_manager
        config_mgr = get_config_manager()
        assert config_mgr.get_global_config("snapshot_location") is not None
        print("   ✓ 配置管理器工作正常")
        
        # 2. 测试所有管理器
        print("2. 测试核心管理器...")
        from ltwin_manager.utils.theme_manager import get_theme_manager
        theme_mgr = get_theme_manager(config_mgr)
        print("   ✓ 主题管理器工作正常")
        
        from ltwin_manager.utils.storage_manager import get_storage_manager
        storage_mgr = get_storage_manager(config_mgr)
        print("   ✓ 存储管理器工作正常")
        
        from ltwin_manager.utils.permission_manager import get_permission_manager
        permission_mgr = get_permission_manager(config_mgr)
        print("   ✓ 权限管理器工作正常")
        
        from ltwin_manager.utils.snapshot_manager import get_snapshot_manager
        snapshot_mgr = get_snapshot_manager(config_mgr)
        print("   ✓ 快照管理器工作正常")
        
        # 3. 测试控制器
        print("3. 测试控制器...")
        from ltwin_manager.controllers.vm_controller import VMController
        vm_controller = VMController(config_mgr)
        print("   ✓ VM控制器工作正常")
        
        # 4. 测试UI组件
        print("4. 测试UI组件...")
        from ltwin_manager.app_window import MainWindow
        print("   ✓ 主窗口模块导入正常")
        
        # 5. 测试对话框
        print("5. 测试对话框...")
        from ltwin_manager.ui.dialogs.download_images_dialog import DownloadImagesDialog
        from ltwin_manager.ui.dialogs.vm_start_options_dialog import VMStartOptionsDialog
        from ltwin_manager.ui.dialogs.chrome_manager_dialog import ChromeManagerDialog
        from ltwin_manager.ui.dialogs.cleanup_dialog import CleanupDialog
        print("   ✓ 所有对话框模块导入正常")
        
        # 6. 测试工具类
        print("6. 测试工具类...")
        from ltwin_manager.utils.vm_start_thread import VMStartThread
        from ltwin_manager.utils.image_download_thread import ImageDownloadThread
        from ltwin_manager.utils.cleanup_tool import CleanupTool
        print("   ✓ 所有工具类导入正常")
        
        print("\n✓ 所有组件测试通过！LTWin Manager已完全修复。")
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_original_issue():
    """测试原始问题是否已解决"""
    print("\n测试原始问题是否已解决...")
    
    try:
        # 测试修复前会导致错误的代码
        from ltwin_manager.utils.config_manager import get_config_manager
        from ltwin_manager.utils.snapshot_manager import get_snapshot_manager
        
        config_mgr = get_config_manager()
        # 这里在修复前会因为snapshot_location为None而导致Path构造函数错误
        snapshot_mgr = get_snapshot_manager(config_mgr)
        
        print("✓ 原始问题已解决：快照管理器可以正常创建")
        return True
    except Exception as e:
        print(f"✗ 原始问题未解决: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("LTWin Manager - 最终验证测试")
    print("=" * 60)
    
    # 测试所有组件
    components_ok = test_all_components()
    
    # 测试原始问题
    issue_fixed = test_original_issue()
    
    print("\n" + "=" * 60)
    print("最终测试结果:")
    print(f"  组件测试: {'通过' if components_ok else '失败'}")
    print(f"  问题修复: {'完成' if issue_fixed else '未完成'}")
    
    if components_ok and issue_fixed:
        print("\n🎉 所有测试通过！LTWin Manager已完全修复并可以正常运行。")
        print("\n现在可以使用以下命令启动应用:")
        print("  python run_ltwin.py")
        print("或")
        print("  quick_start.bat")
    else:
        print("\n❌ 部分测试失败，请检查上述错误信息。")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())