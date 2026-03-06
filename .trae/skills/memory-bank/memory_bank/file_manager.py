"""
文件管理器模块

负责文件的创建、读取、更新、删除等操作。
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import shutil


class FileManager:
    """文件管理器"""

    def __init__(self, root_path: str):
        self.root_path = root_path
        self.ensure_root_directory()

    def ensure_root_directory(self):
        """确保根目录存在"""
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path, exist_ok=True)

    def get_full_path(self, relative_path: str) -> str:
        """获取完整路径"""
        if relative_path.startswith('/'):
            relative_path = relative_path[1:]
        return os.path.join(self.root_path, relative_path)

    def create_file(self, path: str, content: str, metadata: Optional[Dict] = None) -> bool:
        """
        创建新文件

        Args:
            path: 文件相对路径
            content: 文件内容
            metadata: 元数据

        Returns:
            bool: 是否成功
        """
        full_path = self.get_full_path(path)
        directory = os.path.dirname(full_path)

        # 确保目录存在
        os.makedirs(directory, exist_ok=True)

        # 检查文件是否已存在
        if os.path.exists(full_path):
            return False

        # 写入文件
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False

    def read_file(self, path: str, agent_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        读取文件内容

        Args:
            path: 文件相对路径
            agent_id: 智能体ID

        Returns:
            dict: 包含文件内容和元数据的字典
        """
        full_path = self.get_full_path(path)

        if not os.path.exists(full_path):
            return None

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            stat = os.stat(full_path)
            return {
                'content': content,
                'path': path,
                'size': stat.st_size,
                'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'updated_at': datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
        except Exception:
            return None

    def update_file(self, path: str, content: str, agent_id: Optional[str] = None) -> bool:
        """
        更新文件内容

        Args:
            path: 文件相对路径
            content: 新内容
            agent_id: 智能体ID

        Returns:
            bool: 是否成功
        """
        full_path = self.get_full_path(path)

        if not os.path.exists(full_path):
            return False

        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False

    def delete_file(self, path: str, agent_id: Optional[str] = None) -> bool:
        """
        删除文件

        Args:
            path: 文件相对路径
            agent_id: 智能体ID

        Returns:
            bool: 是否成功
        """
        full_path = self.get_full_path(path)

        if not os.path.exists(full_path):
            return False

        try:
            os.remove(full_path)
            return True
        except Exception:
            return False

    def move_file(self, old_path: str, new_path: str, agent_id: Optional[str] = None) -> bool:
        """
        移动文件

        Args:
            old_path: 原路径
            new_path: 新路径
            agent_id: 智能体ID

        Returns:
            bool: 是否成功
        """
        old_full_path = self.get_full_path(old_path)
        new_full_path = self.get_full_path(new_path)

        if not os.path.exists(old_full_path):
            return False

        new_dir = os.path.dirname(new_full_path)
        os.makedirs(new_dir, exist_ok=True)

        try:
            shutil.move(old_full_path, new_full_path)
            return True
        except Exception:
            return False

    def file_exists(self, path: str) -> bool:
        """检查文件是否存在"""
        full_path = self.get_full_path(path)
        return os.path.exists(full_path)

    def list_directory(self, path: str) -> Dict[str, List[str]]:
        """
        列出目录内容

        Args:
            path: 目录路径

        Returns:
            dict: 包含目录和文件列表
        """
        full_path = self.get_full_path(path)

        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            return {'directories': [], 'files': []}

        directories = []
        files = []

        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            if os.path.isdir(item_path):
                directories.append(item)
            elif item.endswith('.md'):
                files.append(item)

        return {
            'directories': sorted(directories),
            'files': sorted(files)
        }

    def create_directory(self, path: str) -> bool:
        """创建目录"""
        full_path = self.get_full_path(path)
        try:
            os.makedirs(full_path, exist_ok=True)
            return True
        except Exception:
            return False

    def extract_title_from_content(self, content: str) -> str:
        """从内容中提取标题"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return "未命名文件"

    def extract_tags_from_content(self, content: str) -> List[str]:
        """从内容中提取标签"""
        tags = []
        # 查找 #标签名 格式
        tag_matches = re.findall(r'#(\w+)', content)
        tags.extend(tag_matches)
        # 查找标签列表
        label_match = re.search(r'\*\*标签\*\*:\s*(.+)$', content, re.MULTILINE)
        if label_match:
            tag_str = label_match.group(1)
            tag_str = tag_str.replace('#', '')
            tags.extend([t.strip() for t in tag_str.split() if t.strip()])
        return list(set(tags))

    def extract_summary_from_content(self, content: str, max_length: int = 100) -> str:
        """从内容中提取摘要"""
        # 跳过标题和元数据部分，查找核心内容
        lines = content.split('\n')
        content_start = 0
        for i, line in enumerate(lines):
            if '##' in line and ('核心内容' in line or '内容' in line):
                content_start = i + 1
                break

        summary_lines = []
        for line in lines[content_start:]:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('##'):
                summary_lines.append(line)
            if len(' '.join(summary_lines)) >= max_length:
                break

        summary = ' '.join(summary_lines)
        if len(summary) > max_length:
            summary = summary[:max_length] + '...'
        return summary or "暂无摘要"
