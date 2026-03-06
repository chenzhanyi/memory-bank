#!/usr/bin/env python3
"""
Memory Bank 操作记录器

用于记录所有Memory Bank的使用操作，便于后续评估。
"""

import os
import json
from datetime import datetime
from pathlib import Path


class OperationLogger:
    """操作记录器"""

    def __init__(self, log_dir: str = None):
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(__file__), "操作记录")
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # 创建按日期的子目录
        self.date_dir = self.log_dir / "按日期记录"
        self.date_dir.mkdir(exist_ok=True)

        # 创建按操作类型的子目录
        self.type_dir = self.log_dir / "按操作类型"
        self.type_dir.mkdir(exist_ok=True)
        for op_type in ["存储", "检索", "更新", "删除"]:
            (self.type_dir / op_type).mkdir(exist_ok=True)

    def log(self, operation_type: str, content: str, file_path: str = "",
            result: str = "success", metadata: dict = None) -> dict:
        """
        记录操作

        Args:
            operation_type: 操作类型 (store/search/update/delete)
            content: 操作内容简述
            file_path: 相关文件路径
            result: 操作结果 (success/failed)
            metadata: 附加元数据

        Returns:
            dict: 记录的日志条目
        """
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # 操作类型映射
        type_map = {
            "store": "存储",
            "search": "检索",
            "update": "更新",
            "delete": "删除",
            "install": "安装"
        }
        op_type_cn = type_map.get(operation_type, operation_type)

        log_entry = {
            "timestamp": time_str,
            "operation_type": operation_type,
            "operation_type_cn": op_type_cn,
            "content": content,
            "file_path": file_path,
            "result": result,
            "metadata": metadata or {}
        }

        # 1. 更新总览
        self._update_overview(log_entry)

        # 2. 按日期记录
        self._append_to_date_log(date_str, log_entry)

        # 3. 按操作类型记录
        self._append_to_type_log(op_type_cn, log_entry)

        return log_entry

    def _update_overview(self, entry: dict):
        """更新总览文件"""
        overview_file = self.log_dir / "操作记录总览.md"

        if not overview_file.exists():
            return

        content = overview_file.read_text(encoding="utf-8")

        # 更新统计信息
        content = self._update_stats(content, entry["operation_type"])

        # 添加操作记录
        content = self._append_operation_to_table(content, entry)

        overview_file.write_text(content, encoding="utf-8")

    def _update_stats(self, content: str, op_type: str) -> str:
        """更新统计信息"""
        import re

        # 更新总操作次数
        def increment_total(match):
            current = int(match.group(1))
            return f"| 总操作次数 | {current + 1} |"

        content = re.sub(r"\| 总操作次数 \| (\d+) \|", increment_total, content)

        # 更新特定操作类型
        type_map = {
            "store": "存储操作",
            "search": "检索操作",
            "update": "更新操作",
            "delete": "删除操作"
        }

        if op_type in type_map:
            label = type_map[op_type]

            def increment_op(match):
                current = int(match.group(1))
                return f"| {label} | {current + 1} |"

            content = re.sub(rf"\| {label} \| (\d+) \|", increment_op, content)

        return content

    def _append_operation_to_table(self, content: str, entry: dict) -> str:
        """添加操作记录到表格"""
        result_emoji = "✅" if entry["result"] == "success" else "❌"
        new_row = (
            f"| {entry['timestamp']} | {entry['operation_type_cn']} | "
            f"{entry['content'][:30]}... | {entry['file_path']} | {result_emoji} |"
        )

        # 找到表格位置并插入
        marker = "|------|---------|---------|---------|------|"
        if marker in content:
            parts = content.split(marker, 1)
            content = parts[0] + marker + "\n" + new_row + parts[1]

        return content

    def _append_to_date_log(self, date_str: str, entry: dict):
        """追加到日期日志"""
        date_file = self.date_dir / f"{date_str}.md"

        if not date_file.exists():
            date_file.write_text(f"# {date_str} 操作记录\n\n## 操作列表\n\n", encoding="utf-8")

        with date_file.open("a", encoding="utf-8") as f:
            f.write(f"\n### {entry['timestamp']}\n")
            f.write(f"- **操作**: {entry['operation_type_cn']}\n")
            f.write(f"- **内容**: {entry['content']}\n")
            if entry['file_path']:
                f.write(f"- **文件**: {entry['file_path']}\n")
            f.write(f"- **结果**: {'✅ 成功' if entry['result'] == 'success' else '❌ 失败'}\n")

    def _append_to_type_log(self, op_type_cn: str, entry: dict):
        """追加到操作类型日志"""
        type_file = self.type_dir / op_type_cn / "记录.md"

        if not type_file.exists():
            type_file.parent.mkdir(exist_ok=True)
            type_file.write_text(f"# {op_type_cn}操作记录\n\n## 记录列表\n\n", encoding="utf-8")

        with type_file.open("a", encoding="utf-8") as f:
            f.write(f"- [{entry['timestamp']}] {entry['content']}")
            if entry['file_path']:
                f.write(f" → {entry['file_path']}")
            f.write("\n")


# 全局记录器实例
_logger = None


def get_logger() -> OperationLogger:
    """获取全局记录器实例"""
    global _logger
    if _logger is None:
        _logger = OperationLogger()
    return _logger


def log_operation(operation_type: str, content: str, file_path: str = "",
                  result: str = "success", metadata: dict = None) -> dict:
    """
    便捷函数：记录操作

    Args:
        operation_type: 操作类型
        content: 内容简述
        file_path: 文件路径
        result: 结果
        metadata: 元数据

    Returns:
        dict: 日志条目
    """
    logger = get_logger()
    return logger.log(operation_type, content, file_path, result, metadata)


if __name__ == "__main__":
    # 测试记录器
    logger = OperationLogger()
    logger.log("store", "测试存储操作", "test/path.md", "success")
    print("✓ 测试记录完成")
