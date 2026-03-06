#!/usr/bin/env python3
"""
带操作记录的 Memory Bank 封装

在原有的 Memory Bank 基础上增加操作记录功能。
"""

import sys
import os

# 添加 Skill 路径
skill_path = os.path.join(os.path.dirname(__file__), "..", ".trae", "skills", "memory-bank")
sys.path.insert(0, skill_path)

from memory_bank import MemoryBankSkill
from operation_logger import log_operation


class MemoryBankWithLogging:
    """带操作记录的记忆库"""

    def __init__(self, memory_path: str = None, agent_id: str = "agent_001"):
        if memory_path is None:
            memory_path = os.path.join(os.path.dirname(__file__), "..", "记忆库")

        self.mb = MemoryBankSkill(memory_path, agent_id)
        self.agent_id = agent_id

    def auto_store_memory(self, content: str, context: dict = None) -> dict:
        """存储记忆（带记录）"""
        result = self.mb.auto_store_memory(content, context)

        # 记录操作
        content_preview = content[:50] if len(content) > 50 else content
        log_operation(
            "store",
            content_preview,
            result.get('file_path', ''),
            "success" if result.get('success') else "failed",
            {"category": result.get('category'), "encrypted": result.get('encrypted')}
        )

        return result

    def auto_retrieve_memory(self, query: str, agent_id: str = None) -> list:
        """检索记忆（带记录）"""
        agent_id = agent_id or self.agent_id
        results = self.mb.auto_retrieve_memory(query, agent_id)

        # 记录操作
        log_operation(
            "search",
            query,
            "",
            "success",
            {"result_count": len(results)}
        )

        return results

    def auto_update_memory(self, file_path: str, new_content: str, agent_id: str = None) -> dict:
        """更新记忆（带记录）"""
        agent_id = agent_id or self.agent_id
        result = self.mb.auto_update_memory(file_path, new_content, agent_id)

        # 记录操作
        content_preview = new_content[:50] if len(new_content) > 50 else new_content
        log_operation(
            "update",
            content_preview,
            file_path,
            "success" if result.get('success') else "failed"
        )

        return result

    def auto_delete_memory(self, file_path: str, agent_id: str = None) -> dict:
        """删除记忆（带记录）"""
        agent_id = agent_id or self.agent_id
        result = self.mb.auto_delete_memory(file_path, agent_id)

        # 记录操作
        log_operation(
            "delete",
            f"删除文件: {file_path}",
            file_path,
            "success" if result.get('success') else "failed"
        )

        return result

    def search_by_tag(self, tag: str, agent_id: str = None) -> list:
        """按标签搜索（带记录）"""
        results = self.mb.search_by_tag(tag)

        log_operation(
            "search",
            f"标签搜索: #{tag}",
            "",
            "success",
            {"result_count": len(results), "tag": tag}
        )

        return results

    # 代理其他方法
    def list_directory(self, path: str = ""):
        return self.mb.list_directory(path)

    def read_file(self, path: str, agent_id: str = None):
        return self.mb.read_file(path, agent_id or self.agent_id)

    def create_file(self, path: str, content: str, metadata: dict = None):
        return self.mb.create_file(path, content, metadata)

    def rebuild_index(self):
        return self.mb.rebuild_index()

    def get_statistics(self):
        return self.mb.get_statistics()


# 便捷函数
def get_memory_bank() -> MemoryBankWithLogging:
    """获取记忆库实例"""
    return MemoryBankWithLogging()


if __name__ == "__main__":
    print("带操作记录的 Memory Bank")
    print("=" * 50)
    mb = get_memory_bank()
    stats = mb.get_statistics()
    print(f"总文件数: {stats['total_files']}")
    print(f"总目录数: {stats['total_directories']}")
