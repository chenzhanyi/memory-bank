"""
权限管理器模块

负责管理智能体的访问权限。
"""

from typing import Dict, List, Optional, Set
from datetime import datetime


class PermissionManager:
    """权限管理器"""

    # 权限级别定义
    PERMISSION_PUBLIC = "public"
    PERMISSION_INTERNAL = "internal"
    PERMISSION_PRIVATE = "private"
    PERMISSION_ENCRYPTED = "encrypted"

    # 角色定义
    ROLE_SUPER_ADMIN = "super_admin"
    ROLE_ADMIN = "admin"
    ROLE_ADVANCED = "advanced"
    ROLE_USER = "user"
    ROLE_GUEST = "guest"

    # 操作类型
    ACTION_READ = "read"
    ACTION_WRITE = "write"
    ACTION_CREATE = "create"
    ACTION_DELETE = "delete"
    ACTION_ADMIN = "admin"

    def __init__(self):
        self.agents: Dict[str, Dict] = {}
        self.permissions: Dict[str, Dict[str, Set[str]]] = {}  # file_path -> {agent_id -> {actions}}
        self.access_logs: List[Dict] = []

        # 初始化默认智能体
        self._init_default_agents()

    def _init_default_agents(self):
        """初始化默认智能体"""
        self.register_agent("agent_001", self.ROLE_SUPER_ADMIN, "超级管理员")
        self.register_agent("agent_002", self.ROLE_ADMIN, "管理员")
        self.register_agent("agent_003", self.ROLE_ADVANCED, "高级用户")
        self.register_agent("agent_default", self.ROLE_USER, "默认用户")

    def register_agent(self, agent_id: str, role: str, name: str = "") -> bool:
        """
        注册智能体

        Args:
            agent_id: 智能体ID
            role: 角色
            name: 名称

        Returns:
            bool: 是否成功
        """
        self.agents[agent_id] = {
            'id': agent_id,
            'role': role,
            'name': name or agent_id,
            'registered_at': datetime.now().isoformat()
        }
        return True

    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """
        获取智能体信息

        Args:
            agent_id: 智能体ID

        Returns:
            dict: 智能体信息
        """
        return self.agents.get(agent_id)

    def grant_permission(self, agent_id: str, file_path: str, permission: str,
                         expires_at: Optional[str] = None) -> bool:
        """
        授予权限

        Args:
            agent_id: 智能体ID
            file_path: 文件路径
            permission: 权限类型
            expires_at: 过期时间

        Returns:
            bool: 是否成功
        """
        if file_path not in self.permissions:
            self.permissions[file_path] = {}
        if agent_id not in self.permissions[file_path]:
            self.permissions[file_path][agent_id] = set()
        self.permissions[file_path][agent_id].add(permission)
        return True

    def revoke_permission(self, agent_id: str, file_path: str, permission: Optional[str] = None) -> bool:
        """
        回收权限

        Args:
            agent_id: 智能体ID
            file_path: 文件路径
            permission: 权限类型（None表示回收所有权限）

        Returns:
            bool: 是否成功
        """
        if file_path not in self.permissions:
            return False
        if agent_id not in self.permissions[file_path]:
            return False

        if permission:
            self.permissions[file_path][agent_id].discard(permission)
        else:
            del self.permissions[file_path][agent_id]

        return True

    def check_permission(self, agent_id: str, file_path: str, action: str,
                         file_permission: str = PERMISSION_PUBLIC) -> bool:
        """
        检查权限

        Args:
            agent_id: 智能体ID
            file_path: 文件路径
            action: 操作类型
            file_permission: 文件的权限级别

        Returns:
            bool: 是否有权限
        """
        agent = self.get_agent(agent_id)
        if not agent:
            agent = self.get_agent("agent_default")
            if not agent:
                return False

        role = agent['role']

        # 超级管理员拥有所有权限
        if role == self.ROLE_SUPER_ADMIN:
            self.log_access(agent_id, file_path, action, "success", "超级管理员权限")
            return True

        # 根据文件权限级别检查
        if file_permission == self.PERMISSION_PUBLIC:
            # 公开文件，所有角色都可以读
            if action == self.ACTION_READ:
                self.log_access(agent_id, file_path, action, "success", "公开文件")
                return True
            # 写操作需要高级权限
            if action in [self.ACTION_WRITE, self.ACTION_CREATE, self.ACTION_DELETE]:
                has_perm = role in [self.ROLE_ADMIN, self.ROLE_ADVANCED]
                self.log_access(agent_id, file_path, action, "success" if has_perm else "failed",
                              "公开文件写操作")
                return has_perm

        elif file_permission == self.PERMISSION_INTERNAL:
            # 内部文件，需要管理员或高级用户
            has_perm = role in [self.ROLE_ADMIN, self.ROLE_ADVANCED]
            self.log_access(agent_id, file_path, action, "success" if has_perm else "failed", "内部文件")
            return has_perm

        elif file_permission == self.PERMISSION_PRIVATE:
            # 私密文件，检查特定授权
            has_perm = self._check_specific_permission(agent_id, file_path, action)
            if not has_perm:
                # 管理员也可以访问
                has_perm = role == self.ROLE_ADMIN
            self.log_access(agent_id, file_path, action, "success" if has_perm else "failed", "私密文件")
            return has_perm

        elif file_permission == self.PERMISSION_ENCRYPTED:
            # 加密文件，需要特定授权或管理员
            has_perm = self._check_specific_permission(agent_id, file_path, action)
            if not has_perm:
                has_perm = role == self.ROLE_ADMIN
            self.log_access(agent_id, file_path, action, "success" if has_perm else "failed", "加密文件")
            return has_perm

        self.log_access(agent_id, file_path, action, "failed", "未知权限级别")
        return False

    def _check_specific_permission(self, agent_id: str, file_path: str, action: str) -> bool:
        """检查特定权限"""
        if file_path in self.permissions:
            if agent_id in self.permissions[file_path]:
                return action in self.permissions[file_path][agent_id]
        return False

    def log_access(self, agent_id: str, file_path: str, action: str, result: str, details: str = ""):
        """
        记录访问日志

        Args:
            agent_id: 智能体ID
            file_path: 文件路径
            action: 操作类型
            result: 结果
            details: 详情
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent_id': agent_id,
            'action': action,
            'file_path': file_path,
            'result': result,
            'details': details
        }
        self.access_logs.append(log_entry)

        # 保持日志数量在合理范围内
        if len(self.access_logs) > 1000:
            self.access_logs = self.access_logs[-1000:]

    def get_access_logs(self, agent_id: Optional[str] = None,
                        file_path: Optional[str] = None,
                        limit: int = 100) -> List[Dict]:
        """
        获取访问日志

        Args:
            agent_id: 智能体ID过滤
            file_path: 文件路径过滤
            limit: 返回数量限制

        Returns:
            list: 日志列表
        """
        logs = self.access_logs.copy()

        if agent_id:
            logs = [log for log in logs if log['agent_id'] == agent_id]
        if file_path:
            logs = [log for log in logs if log['file_path'] == file_path]

        return logs[-limit:]

    def get_file_permission_from_content(self, content: str) -> str:
        """
        从文件内容中提取权限级别

        Args:
            content: 文件内容

        Returns:
            str: 权限级别
        """
        import re
        match = re.search(r'\*\*访问权限\*\*:\s*(\w+)', content)
        if match:
            return match.group(1)
        return self.PERMISSION_PUBLIC
