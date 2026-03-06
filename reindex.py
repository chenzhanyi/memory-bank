#!/usr/bin/env python3
"""
重建记忆库索引
"""

import sys
import os

skill_path = os.path.join(os.path.dirname(__file__), ".trae", "skills", "memory-bank")
sys.path.insert(0, skill_path)

from memory_bank import MemoryBankSkill

memory_path = os.path.join(os.path.dirname(__file__), "记忆库")
mb = MemoryBankSkill(memory_path, "agent_001")

print("重建索引中...")
success = mb.rebuild_index()

if success:
    print("✓ 索引重建完成！")

    # 显示统计
    stats = mb.get_statistics()
    print(f"\n统计信息:")
    print(f"  总文件数: {stats['total_files']}")
    print(f"  总目录数: {stats['total_directories']}")
else:
    print("✗ 索引重建失败")
