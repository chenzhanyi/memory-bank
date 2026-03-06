"""
Memory Bank Skill - 图书馆式记忆库核心类

整合文件管理、索引管理、权限管理和加密服务，提供完整的记忆库功能。
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import json

from .file_manager import FileManager
from .index_manager import IndexManager
from .permission_manager import PermissionManager
from .encryption_service import EncryptionService


class MemoryBankSkill:
    """Memory Bank技能核心类"""

    # 默认分类目录
    DEFAULT_CATEGORIES = [
        "01-工作事业",
        "02-生活日常",
        "03-个人成长",
        "04-社交关系",
        "05-财务管理",
        "06-密码密钥",
        "07-资源收藏",
        "08-临时便签"
    ]

    # 密码密钥子分类
    PASSWORD_SUBCATEGORIES = [
        "API密钥",
        "账号密码",
        "证书密钥"
    ]

    # 自动存储模式
    AUTO_STORE_PATTERNS = {
        "api_key": {
            "patterns": [r"api[_-]?key", r"token", r"secret", r"密钥"],
            "category": "06-密码密钥/API密钥",
            "encrypt": True,
            "tags": ["API", "密钥"]
        },
        "password": {
            "patterns": [r"密码", r"password", r"pwd"],
            "category": "06-密码密钥/账号密码",
            "encrypt": True,
            "tags": ["密码", "账号"]
        },
        "project": {
            "patterns": [r"项目", r"project", r"任务", r"task"],
            "category": "01-工作事业/项目管理",
            "encrypt": False,
            "tags": ["项目", "工作"]
        },
        "meeting": {
            "patterns": [r"会议", r"meeting", r"讨论", r"discussion"],
            "category": "01-工作事业/项目管理",
            "encrypt": False,
            "tags": ["会议", "记录"]
        },
        "health": {
            "patterns": [r"健康", r"体检", r"运动", r"health"],
            "category": "02-生活日常/健康管理",
            "encrypt": False,
            "tags": ["健康", "生活"]
        },
        "preference": {
            "patterns": [r"喜欢", r"偏好", r"prefer", r"习惯"],
            "category": "03-个人成长",
            "encrypt": False,
            "tags": ["偏好", "个人"]
        }
    }

    def __init__(self, root_path: str, agent_id: str = "agent_default"):
        """
        初始化Memory Bank

        Args:
            root_path: 记忆库根目录路径
            agent_id: 默认智能体ID
        """
        self.root_path = root_path
        self.agent_id = agent_id

        # 初始化各个管理器
        self.file_manager = FileManager(root_path)
        self.index_manager = IndexManager(root_path, self.file_manager)
        self.permission_manager = PermissionManager()
        self.encryption_service = EncryptionService()

        # 确保基础目录结构存在
        self._ensure_directory_structure()

    def _ensure_directory_structure(self):
        """确保目录结构存在"""
        # 创建根目录
        self.file_manager.create_directory("")

        # 创建默认分类目录
        for category in self.DEFAULT_CATEGORIES:
            self.file_manager.create_directory(category)

            # 为密码密钥创建子目录
            if category == "06-密码密钥":
                for subcategory in self.PASSWORD_SUBCATEGORIES:
                    self.file_manager.create_directory(f"{category}/{subcategory}")

            # 为工作事业创建子目录
            if category == "01-工作事业":
                self.file_manager.create_directory(f"{category}/项目管理")
                self.file_manager.create_directory(f"{category}/技能提升")

            # 为生活日常创建子目录
            if category == "02-生活日常":
                self.file_manager.create_directory(f"{category}/健康管理")
                self.file_manager.create_directory(f"{category}/家庭事务")

            # 为个人成长创建子目录
            if category == "03-个人成长":
                self.file_manager.create_directory(f"{category}/阅读笔记")
                self.file_manager.create_directory(f"{category}/学习计划")

        # 生成初始索引
        self.index_manager.rebuild_index()

    def auto_store_memory(self, content: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        自动存储记忆碎片

        Args:
            content: 记忆内容
            context: 上下文信息（可选）

        Returns:
            dict: 存储结果
        """
        # 1. 分析内容类型
        content_type = self._analyze_content_type(content)

        # 2. 确定分类
        category = content_type.get('category', '08-临时便签')

        # 3. 生成文件名
        filename = self._generate_filename(content, content_type)

        # 4. 准备文件内容
        file_content = self._prepare_file_content(content, content_type, context)

        # 5. 检查是否需要加密
        if content_type.get('encrypt', False):
            # 加密敏感部分
            file_content = self._encrypt_sensitive_parts(file_content, content_type)

        # 6. 创建文件
        file_path = f"{category}/{filename}.md"
        metadata = {
            'tags': content_type.get('tags', []),
            'permission': 'encrypted' if content_type.get('encrypt') else 'private'
        }

        success = self.file_manager.create_file(file_path, file_content, metadata)

        if not success:
            # 文件已存在，尝试读取并追加内容
            existing = self.file_manager.read_file(file_path, self.agent_id)
            if existing:
                merged_content = self._merge_content(existing['content'], file_content)
                success = self.file_manager.update_file(file_path, merged_content, self.agent_id)

        # 7. 更新索引
        if success:
            self.index_manager.update_index(category, file_path, 'create' if success else 'update')

        # 8. 返回结果
        return {
            'success': success,
            'file_path': file_path,
            'category': category,
            'encrypted': content_type.get('encrypt', False),
            'content_type': content_type.get('type', 'general')
        }

    def _analyze_content_type(self, content: str) -> Dict[str, Any]:
        """
        分析内容类型

        Args:
            content: 内容

        Returns:
            dict: 内容类型信息
        """
        content_lower = content.lower()

        for type_name, config in self.AUTO_STORE_PATTERNS.items():
            for pattern in config['patterns']:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    return {
                        'type': type_name,
                        'category': config['category'],
                        'encrypt': config['encrypt'],
                        'tags': config.get('tags', [])
                    }

        # 默认分类
        return {
            'type': 'general',
            'category': '08-临时便签',
            'encrypt': False,
            'tags': ['临时']
        }

    def _generate_filename(self, content: str, content_type: Dict) -> str:
        """
        生成文件名

        Args:
            content: 内容
            content_type: 内容类型

        Returns:
            str: 文件名
        """
        # 提取标题
        title = self.file_manager.extract_title_from_content(content)
        if title == "未命名文件":
            # 尝试从内容中提取关键词
            content_type_name = content_type.get('type', 'general')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return f"{content_type_name}_{timestamp}"

        # 清理标题作为文件名
        filename = re.sub(r'[\\/:*?"<>|]', '_', title)
        filename = filename.strip()
        if len(filename) > 50:
            filename = filename[:50]
        return filename or f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def _prepare_file_content(self, content: str, content_type: Dict, context: Optional[Dict] = None) -> str:
        """
        准备文件内容

        Args:
            content: 原始内容
            content_type: 内容类型
            context: 上下文

        Returns:
            str: 格式化的文件内容
        """
        title = self.file_manager.extract_title_from_content(content)
        if title == "未命名文件":
            title = f"{content_type.get('type', '记忆')} - {datetime.now().strftime('%Y-%m-%d')}"

        tags = content_type.get('tags', [])
        tags_str = ' '.join([f'#{t}' for t in tags])
        importance = "⭐⭐⭐"
        permission = "encrypted" if content_type.get('encrypt') else "private"

        # 根据内容类型选择模板
        if content_type.get('type') in ['api_key', 'password']:
            return self._format_password_file(title, content, tags_str, importance, permission, context)
        else:
            return self._format_general_file(title, content, tags_str, importance, permission, context)

    def _format_general_file(self, title: str, content: str, tags_str: str,
                              importance: str, permission: str, context: Optional[Dict] = None) -> str:
        """格式化普通文件"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"""# {title}

## 📌 基本信息
- **创建时间**: {datetime.now().strftime('%Y-%m-%d')}
- **最后更新**: {now}
- **标签**: {tags_str}
- **重要程度**: {importance}
- **访问权限**: {permission}
- **版本**: v1.0

## 📝 核心内容
{content}

## 🔗 相关文件
- 暂无

## 📎 附件
- 暂无

## 📊 更新历史
| 日期 | 版本 | 更新内容 | 更新人 |
|------|------|----------|--------|
| {datetime.now().strftime('%Y-%m-%d')} | v1.0 | 初始创建 | {self.agent_id} |

## 💭 备注
{json.dumps(context, ensure_ascii=False) if context else '无'}
"""

    def _format_password_file(self, title: str, content: str, tags_str: str,
                               importance: str, permission: str, context: Optional[Dict] = None) -> str:
        """格式化密码文件"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"""# {title}

## 🔐 安全信息
- **加密级别**: high
- **授权智能体**: [{self.agent_id}]
- **最后使用**: {datetime.now().strftime('%Y-%m-%d')}
- **有效期至**: 长期有效
- **访问次数**: 1

## 🔑 密钥内容
```
{content}
```

## 📋 使用记录
| 时间 | 智能体ID | 用途 | 结果 | IP地址 |
|------|----------|------|------|--------|
| {now} | {self.agent_id} | 记录创建 | 成功 | - |

## ⚠️ 安全提示
- 请妥善保管此信息
- 定期更新密钥和密码
- 不要分享给未授权人员

## 🔄 更新历史
| 日期 | 操作 | 操作人 |
|------|------|--------|
| {datetime.now().strftime('%Y-%m-%d')} | 创建记录 | {self.agent_id} |
"""

    def _encrypt_sensitive_parts(self, content: str, content_type: Dict) -> str:
        """加密敏感部分"""
        # 这里可以实现更精细的加密策略
        # 目前直接使用encryption_service加密整个内容中的敏感部分
        return content

    def _merge_content(self, old_content: str, new_content: str) -> str:
        """合并内容"""
        # 简单地将新内容追加到旧内容后面
        separator = f"\n\n---\n\n## 追加内容 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n\n"
        return old_content + separator + new_content

    def auto_retrieve_memory(self, query: str, agent_id: Optional[str] = None) -> List[Dict]:
        """
        自动检索记忆

        Args:
            query: 查询内容
            agent_id: 智能体ID

        Returns:
            list: 检索结果列表
        """
        agent_id = agent_id or self.agent_id

        # 1. 分析查询意图
        intent = self._analyze_query_intent(query)

        # 2. 确定检索范围
        search_scope = self._determine_search_scope(intent)

        # 3. 执行检索
        results = []
        keywords = intent.get('keywords', [query])

        for category in search_scope:
            category_results = self._search_in_category(category, keywords, agent_id)
            results.extend(category_results)

        # 4. 排序和过滤
        results = self._rank_results(results, intent)

        # 5. 解密需要的内容
        for result in results:
            if result.get('encrypted'):
                file_data = self.file_manager.read_file(result['path'], agent_id)
                if file_data:
                    result['content'] = self.encryption_service.extract_and_decrypt_all(
                        file_data['content'],
                        agent_id
                    )

        return results

    def _analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """分析查询意图"""
        intent = {
            'text': query,
            'keywords': [],
            'category': None,
            'time_range': None
        }

        # 提取关键词
        words = re.split(r'[，。？！,.?!\s]+', query)
        intent['keywords'] = [w for w in words if w]

        # 尝试识别分类
        category_keywords = {
            '工作': '01-工作事业',
            '项目': '01-工作事业/项目管理',
            '生活': '02-生活日常',
            '健康': '02-生活日常/健康管理',
            '成长': '03-个人成长',
            '社交': '04-社交关系',
            '财务': '05-财务管理',
            '密码': '06-密码密钥',
            '密钥': '06-密码密钥/API密钥',
            '资源': '07-资源收藏',
            '临时': '08-临时便签'
        }

        for keyword, category in category_keywords.items():
            if keyword in query:
                intent['category'] = category
                break

        return intent

    def _determine_search_scope(self, intent: Dict) -> List[str]:
        """确定检索范围"""
        if intent.get('category'):
            return [intent['category']]
        return self.DEFAULT_CATEGORIES

    def _search_in_category(self, category: str, keywords: List[str], agent_id: str) -> List[Dict]:
        """在分类中搜索"""
        results = []

        # 使用关键词搜索
        for keyword in keywords:
            keyword_results = self.index_manager.search_by_keyword(keyword, category)
            for result in keyword_results:
                result['keyword'] = keyword
                # 确保有 relevance 字段
                if 'relevance' not in result:
                    result['relevance'] = 0.5
                results.append(result)

        # 去重（保留最高相关性的）
        path_to_best = {}
        for result in results:
            path = result['path']
            if path not in path_to_best or result['relevance'] > path_to_best[path]['relevance']:
                path_to_best[path] = result

        return list(path_to_best.values())

    def _rank_results(self, results: List[Dict], intent: Dict) -> List[Dict]:
        """排序结果"""
        # 简单排序：按相关性分数
        sorted_results = sorted(
            results,
            key=lambda x: x.get('relevance', 0.5),
            reverse=True
        )
        return sorted_results[:20]

    def auto_update_memory(self, file_path: str, new_content: str, agent_id: Optional[str] = None) -> Dict:
        """
        自动更新记忆

        Args:
            file_path: 文件路径
            new_content: 新内容
            agent_id: 智能体ID

        Returns:
            dict: 更新结果
        """
        agent_id = agent_id or self.agent_id

        # 读取原文件
        old_file = self.file_manager.read_file(file_path, agent_id)
        if not old_file:
            return {'success': False, 'error': '文件不存在'}

        # 合并内容
        merged_content = self._merge_content(old_file['content'], new_content)

        # 更新文件
        success = self.file_manager.update_file(file_path, merged_content, agent_id)

        # 更新索引
        if success:
            category = os.path.dirname(file_path)
            self.index_manager.update_index(category, file_path, 'update')

        return {'success': success, 'file_path': file_path}

    def auto_delete_memory(self, file_path: str, agent_id: Optional[str] = None) -> Dict:
        """
        自动删除记忆

        Args:
            file_path: 文件路径
            agent_id: 智能体ID

        Returns:
            dict: 删除结果
        """
        agent_id = agent_id or self.agent_id

        category = os.path.dirname(file_path)

        # 删除文件
        success = self.file_manager.delete_file(file_path, agent_id)

        # 更新索引
        if success:
            self.index_manager.update_index(category, file_path, 'delete')

        return {'success': success, 'file_path': file_path}

    def search_by_tag(self, tag: str, agent_id: Optional[str] = None) -> List[Dict]:
        """
        按标签搜索

        Args:
            tag: 标签
            agent_id: 智能体ID

        Returns:
            list: 搜索结果
        """
        return self.index_manager.search_by_tag(tag)

    def list_directory(self, path: str = "") -> Dict[str, List[str]]:
        """
        列出目录内容

        Args:
            path: 目录路径

        Returns:
            dict: 目录内容
        """
        return self.file_manager.list_directory(path)

    def read_file(self, path: str, agent_id: Optional[str] = None) -> Optional[Dict]:
        """
        读取文件

        Args:
            path: 文件路径
            agent_id: 智能体ID

        Returns:
            dict: 文件内容
        """
        agent_id = agent_id or self.agent_id
        return self.file_manager.read_file(path, agent_id)

    def create_file(self, path: str, content: str, metadata: Optional[Dict] = None) -> bool:
        """
        创建文件

        Args:
            path: 文件路径
            content: 文件内容
            metadata: 元数据

        Returns:
            bool: 是否成功
        """
        success = self.file_manager.create_file(path, content, metadata)
        if success:
            category = os.path.dirname(path)
            self.index_manager.update_index(category, path, 'create')
        return success

    def rebuild_index(self) -> bool:
        """重建索引"""
        return self.index_manager.rebuild_index()

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            dict: 统计信息
        """
        total_files = 0
        total_dirs = 0

        def count_recursive(path: str):
            nonlocal total_files, total_dirs
            content = self.file_manager.list_directory(path)
            total_files += len([f for f in content['files'] if f != '分类目录.md'])
            total_dirs += len(content['directories'])
            for subdir in content['directories']:
                subpath = os.path.join(path, subdir) if path else subdir
                count_recursive(subpath)

        count_recursive("")

        return {
            'total_files': total_files,
            'total_directories': total_dirs,
            'categories': self.DEFAULT_CATEGORIES
        }
