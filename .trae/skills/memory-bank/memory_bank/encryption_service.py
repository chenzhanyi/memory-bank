"""
加密服务模块

提供敏感信息的加密和解密功能。
"""

import base64
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime


class EncryptionService:
    """加密服务"""

    # 加密级别
    LEVEL_LOW = "low"
    LEVEL_MEDIUM = "medium"
    LEVEL_HIGH = "high"

    def __init__(self):
        self.keys: Dict[str, str] = {}
        self.key_metadata: Dict[str, Dict] = {}
        self._init_default_keys()

    def _init_default_keys(self):
        """初始化默认密钥"""
        # 生成默认密钥（实际使用中应该从安全位置加载）
        self._generate_and_store_key("default_low", self.LEVEL_LOW)
        self._generate_and_store_key("default_medium", self.LEVEL_MEDIUM)
        self._generate_and_store_key("default_high", self.LEVEL_HIGH)

    def _generate_and_store_key(self, key_id: str, level: str):
        """生成并存储密钥"""
        key = self.generate_key(level)
        self.keys[key_id] = key
        self.key_metadata[key_id] = {
            'level': level,
            'created_at': datetime.now().isoformat(),
            'key_id': key_id
        }

    def generate_key(self, level: str) -> str:
        """
        生成加密密钥

        Args:
            level: 加密级别

        Returns:
            str: 生成的密钥
        """
        import secrets
        # 根据级别生成不同长度的密钥
        if level == self.LEVEL_LOW:
            key_bytes = secrets.token_bytes(16)  # 128位
        elif level == self.LEVEL_MEDIUM:
            key_bytes = secrets.token_bytes(32)  # 256位
        else:  # high
            key_bytes = secrets.token_bytes(64)  # 512位

        return base64.b64encode(key_bytes).decode('utf-8')

    def _simple_encrypt(self, data: str, key: str) -> str:
        """
        简单的XOR加密（示例用，实际应使用AES等强加密）

        注意：这只是一个演示实现，生产环境应使用cryptography库
        """
        # 生成密钥的哈希作为实际加密密钥
        key_bytes = hashlib.sha256(key.encode('utf-8')).digest()
        data_bytes = data.encode('utf-8')

        # XOR加密
        encrypted_bytes = bytearray()
        key_len = len(key_bytes)
        for i, byte in enumerate(data_bytes):
            encrypted_bytes.append(byte ^ key_bytes[i % key_len])

        # Base64编码
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def _simple_decrypt(self, encrypted_data: str, key: str) -> str:
        """
        简单的XOR解密

        注意：这只是一个演示实现，生产环境应使用cryptography库
        """
        try:
            # Base64解码
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))

            # 生成密钥的哈希
            key_bytes = hashlib.sha256(key.encode('utf-8')).digest()

            # XOR解密
            decrypted_bytes = bytearray()
            key_len = len(key_bytes)
            for i, byte in enumerate(encrypted_bytes):
                decrypted_bytes.append(byte ^ key_bytes[i % key_len])

            return decrypted_bytes.decode('utf-8')
        except Exception:
            return ""

    def encrypt(self, data: str, level: str = LEVEL_MEDIUM, key_id: Optional[str] = None) -> str:
        """
        加密数据

        Args:
            data: 原始数据
            level: 加密级别
            key_id: 密钥ID（可选）

        Returns:
            str: 加密后的数据
        """
        if not data:
            return ""

        # 选择密钥
        if key_id and key_id in self.keys:
            key = self.keys[key_id]
        else:
            default_key_id = f"default_{level}"
            key = self.keys.get(default_key_id, self.keys.get("default_medium", ""))

        if not key:
            # 如果没有密钥，返回base64编码的原始数据（不加密）
            return base64.b64encode(data.encode('utf-8')).decode('utf-8')

        # 加密
        encrypted = self._simple_encrypt(data, key)

        # 添加加密级别标记
        return f"ENC:{level}:{encrypted}"

    def decrypt(self, encrypted_data: str, agent_id: Optional[str] = None) -> str:
        """
        解密数据

        Args:
            encrypted_data: 加密的数据
            agent_id: 智能体ID（用于权限验证）

        Returns:
            str: 解密后的数据
        """
        if not encrypted_data:
            return ""

        # 检查是否是加密格式
        if not encrypted_data.startswith("ENC:"):
            # 尝试base64解码
            try:
                return base64.b64decode(encrypted_data.encode('utf-8')).decode('utf-8')
            except Exception:
                return encrypted_data

        # 解析加密格式
        parts = encrypted_data.split(':', 3)
        if len(parts) < 3:
            return encrypted_data

        level = parts[1]
        data = parts[2]

        # 获取对应级别的密钥
        key_id = f"default_{level}"
        key = self.keys.get(key_id, self.keys.get("default_medium", ""))

        if not key:
            return encrypted_data

        # 解密
        return self._simple_decrypt(data, key)

    def store_key(self, key_id: str, key: str, agent_id: str, level: str = LEVEL_MEDIUM) -> bool:
        """
        存储密钥

        Args:
            key_id: 密钥ID
            key: 密钥内容
            agent_id: 智能体ID
            level: 加密级别

        Returns:
            bool: 是否成功
        """
        self.keys[key_id] = key
        self.key_metadata[key_id] = {
            'level': level,
            'stored_by': agent_id,
            'stored_at': datetime.now().isoformat()
        }
        return True

    def wrap_sensitive_content(self, content: str, level: str = LEVEL_HIGH) -> str:
        """
        包装敏感内容，添加标记

        Args:
            content: 原始内容
            level: 加密级别

        Returns:
            str: 包装后的内容
        """
        encrypted = self.encrypt(content, level)
        return f"""
```encrypted
{encrypted}
```
"""

    def unwrap_sensitive_content(self, wrapped_content: str, agent_id: Optional[str] = None) -> str:
        """
        解包敏感内容

        Args:
            wrapped_content: 包装的内容
            agent_id: 智能体ID

        Returns:
            str: 原始内容
        """
        import re
        match = re.search(r'```encrypted\s*\n([\s\S]*?)\n```', wrapped_content)
        if match:
            encrypted = match.group(1).strip()
            return self.decrypt(encrypted, agent_id)
        return wrapped_content

    def extract_and_decrypt_all(self, content: str, agent_id: Optional[str] = None) -> str:
        """
        提取并解密内容中所有加密部分

        Args:
            content: 包含加密内容的文本
            agent_id: 智能体ID

        Returns:
            str: 解密后的完整文本
        """
        import re

        def replace_encrypted(match):
            encrypted = match.group(1).strip()
            decrypted = self.decrypt(encrypted, agent_id)
            return f"\n{decrypted}\n"

        return re.sub(r'```encrypted\s*\n([\s\S]*?)\n```', replace_encrypted, content)

    def is_encrypted_data(self, data: str) -> bool:
        """
        检查是否是加密数据

        Args:
            data: 数据

        Returns:
            bool: 是否加密
        """
        return data.startswith("ENC:")
