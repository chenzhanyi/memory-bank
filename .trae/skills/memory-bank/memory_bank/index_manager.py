"""
索引管理器模块

负责维护分类目录.md文件，提供索引生成和更新功能。
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any


class IndexManager:
    """索引管理器"""

    INDEX_FILENAME = "分类目录.md"

    def __init__(self, root_path: str, file_manager):
        self.root_path = root_path
        self.file_manager = file_manager
        self.index_cache: Dict[str, Dict] = {}

    def get_index_path(self, directory: str) -> str:
        """获取索引文件路径"""
        if directory:
            return os.path.join(directory, self.INDEX_FILENAME)
        return self.INDEX_FILENAME

    def generate_index(self, directory: str = "") -> bool:
        """
        生成目录索引

        Args:
            directory: 目录路径（相对根目录）

        Returns:
            bool: 是否成功
        """
        # 获取目录内容
        dir_content = self.file_manager.list_directory(directory)

        # 生成索引内容
        index_content = self._build_index_content(
            directory,
            dir_content['directories'],
            dir_content['files']
        )

        # 写入索引文件
        index_path = self.get_index_path(directory)
        result = self.file_manager.create_file(index_path, index_content)

        # 如果文件已存在，尝试更新
        if not result:
            result = self.file_manager.update_file(index_path, index_content)

        # 更新缓存
        self.index_cache[directory] = self._parse_index_content(index_content)

        # 递归处理子目录
        for subdir in dir_content['directories']:
            subdir_path = os.path.join(directory, subdir) if directory else subdir
            self.generate_index(subdir_path)

        return result

    def _build_index_content(self, directory: str, directories: List[str], files: List[str]) -> str:
        """
        构建索引文件内容

        Args:
            directory: 目录路径
            directories: 子目录列表
            files: 文件列表

        Returns:
            str: Markdown格式的索引内容
        """
        dir_name = os.path.basename(directory) if directory else "记忆库"

        # 构建子目录表格
        subdir_table = self._build_subdir_table(directory, directories)

        # 构建文件表格
        file_table = self._build_file_table(directory, files)

        # 统计信息
        total_files = len([f for f in files if f != self.INDEX_FILENAME])
        total_dirs = len(directories)

        content = f"""# {dir_name} - 分类目录

## 📋 目录说明
本目录用于存储{dir_name}相关的记忆内容。

## 📂 子目录列表
| 目录名 | 说明 | 包含文件数 | 创建时间 |
|--------|------|-----------|----------|
{subdir_table}

## 📄 文件索引
| 文件名 | 简介 | 标签 | 重要程度 | 更新时间 |
|--------|------|------|----------|----------|
{file_table}

## 🔍 快速查找
- 按标签: #标签名
- 按类型: 文件类型
- 按时间: 时间范围

## 📊 统计信息
- 总文件数: {total_files}
- 总目录数: {total_dirs}
- 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return content

    def _build_subdir_table(self, directory: str, directories: List[str]) -> str:
        """构建子目录表格"""
        if not directories:
            return "| - | 暂无子目录 | - | - |"

        rows = []
        for dir_name in directories:
            subdir_path = os.path.join(directory, dir_name) if directory else dir_name
            content = self.file_manager.list_directory(subdir_path)
            file_count = len([f for f in content['files'] if f != self.INDEX_FILENAME])
            rows.append(f"| {dir_name} | - | {file_count} | - |")

        return '\n'.join(rows)

    def _build_file_table(self, directory: str, files: List[str]) -> str:
        """构建文件表格"""
        md_files = [f for f in files if f != self.INDEX_FILENAME and f.endswith('.md')]

        if not md_files:
            return "| - | 暂无文件 | - | - | - |"

        rows = []
        for filename in md_files:
            file_path = os.path.join(directory, filename) if directory else filename
            file_data = self.file_manager.read_file(file_path)

            if file_data:
                content = file_data['content']
                title = self.file_manager.extract_title_from_content(content)
                summary = self.file_manager.extract_summary_from_content(content, max_length=30)
                tags = self.file_manager.extract_tags_from_content(content)
                tags_str = ' '.join([f'#{t}' for t in tags[:3]]) if tags else '-'
                importance = self._extract_importance(content)
                updated_at = file_data['updated_at'][:10] if file_data['updated_at'] else '-'

                rows.append(f"| {filename} | {summary} | {tags_str} | {importance} | {updated_at} |")
            else:
                rows.append(f"| {filename} | - | - | - | - |")

        return '\n'.join(rows)

    def _extract_importance(self, content: str) -> str:
        """从内容中提取重要程度"""
        import re
        match = re.search(r'\*\*重要程度\*\*:\s*(\*+)', content)
        if match:
            return match.group(1)
        return "⭐⭐⭐"

    def _parse_index_content(self, content: str) -> Dict[str, Any]:
        """解析索引内容为结构化数据"""
        return {
            'files': [],
            'directories': [],
            'raw_content': content
        }

    def update_index(self, directory: str, file_path: str, action: str) -> bool:
        """
        更新索引信息

        Args:
            directory: 分类路径
            file_path: 文件路径
            action: 操作类型 (create/update/delete)

        Returns:
            bool: 是否成功
        """
        # 重新生成该目录的索引
        return self.generate_index(directory)

    def rebuild_index(self, root_path: str = "") -> bool:
        """
        重建整个索引系统

        Args:
            root_path: 根路径

        Returns:
            bool: 是否成功
        """
        self.index_cache.clear()
        return self.generate_index(root_path)

    def search_by_tag(self, tag: str, directory: str = "") -> List[Dict]:
        """
        按标签搜索

        Args:
            tag: 标签名
            directory: 搜索起始目录

        Returns:
            list: 匹配的文件列表
        """
        results = []
        self._search_by_tag_recursive(tag, directory, results)
        return results

    def _search_by_tag_recursive(self, tag: str, directory: str, results: List[Dict]):
        """递归按标签搜索"""
        # 读取当前目录索引
        index_path = self.get_index_path(directory)
        index_data = self.file_manager.read_file(index_path)

        if index_data:
            content = index_data['content']
            # 在索引中查找标签
            lines = content.split('\n')
            in_file_table = False
            for line in lines:
                if line.startswith('## 📄 文件索引'):
                    in_file_table = True
                    continue
                if in_file_table and line.startswith('##'):
                    break
                if in_file_table and line.startswith('|') and '|' in line[1:]:
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 5:
                        filename = parts[0]
                        tags_part = parts[2]
                        if f'#{tag}' in tags_part or tag in tags_part:
                            file_path = os.path.join(directory, filename) if directory else filename
                            results.append({
                                'filename': filename,
                                'path': file_path,
                                'summary': parts[1],
                                'tags': tags_part,
                                'directory': directory
                            })

        # 递归搜索子目录
        dir_content = self.file_manager.list_directory(directory)
        for subdir in dir_content['directories']:
            subdir_path = os.path.join(directory, subdir) if directory else subdir
            self._search_by_tag_recursive(tag, subdir_path, results)

    def search_by_keyword(self, keyword: str, directory: str = "") -> List[Dict]:
        """
        按关键词搜索

        Args:
            keyword: 关键词
            directory: 搜索起始目录

        Returns:
            list: 匹配的文件列表
        """
        results = []
        keyword_lower = keyword.lower()
        self._search_by_keyword_recursive(keyword_lower, directory, results)
        return results

    def _search_by_keyword_recursive(self, keyword: str, directory: str, results: List[Dict]):
        """递归按关键词搜索"""
        dir_content = self.file_manager.list_directory(directory)

        # 搜索当前目录的文件
        for filename in dir_content['files']:
            if filename == self.INDEX_FILENAME:
                continue
            file_path = os.path.join(directory, filename) if directory else filename
            file_data = self.file_manager.read_file(file_path)

            if file_data:
                content_lower = file_data['content'].lower()
                if keyword in content_lower:
                    summary = self.file_manager.extract_summary_from_content(file_data['content'])
                    results.append({
                        'filename': filename,
                        'path': file_path,
                        'summary': summary,
                        'directory': directory,
                        'relevance': self._calculate_relevance(keyword, file_data['content'])
                    })

        # 递归搜索子目录
        for subdir in dir_content['directories']:
            subdir_path = os.path.join(directory, subdir) if directory else subdir
            self._search_by_keyword_recursive(keyword, subdir_path, results)

    def _calculate_relevance(self, keyword: str, content: str) -> float:
        """计算相关性分数"""
        content_lower = content.lower()
        keyword_count = content_lower.count(keyword)
        # 简单的相关性计算：关键词出现次数
        return min(1.0, keyword_count * 0.1)

    def read_index(self, directory: str = "") -> Optional[Dict]:
        """
        读取目录索引

        Args:
            directory: 目录路径

        Returns:
            dict: 索引数据
        """
        if directory in self.index_cache:
            return self.index_cache[directory]

        index_path = self.get_index_path(directory)
        index_data = self.file_manager.read_file(index_path)

        if index_data:
            parsed = self._parse_index_content(index_data['content'])
            self.index_cache[directory] = parsed
            return parsed

        return None
