# 图书馆式记忆库 Skill 开发文档

**版本**: v1.0  
**创建日期**: 2026-03-05  
**文档类型**: 技术开发文档  
**适用范围**: 智能体记忆系统开发

---

## 目录

1. [项目概述](#1-项目概述)
2. [系统架构](#2-系统架构)
3. [数据结构设计](#3-数据结构设计)
4. [功能模块设计](#4-功能模块设计)
5. [检索机制](#5-检索机制)
6. [安全权限机制](#6-安全权限机制)
7. [API接口设计](#7-api接口设计)
8. [开发规范](#8-开发规范)
9. [测试方案](#9-测试方案)
10. [部署方案](#10-部署方案)
11. [Skill集成与自动调用](#11-skill集成与自动调用)

---

## 1. 项目概述

### 1.1 项目背景

传统的智能体长期记忆方案存在以下问题：
- 检索效率低下
- 数据结构复杂
- 维护成本高
- 扩展性差

本项目采用图书馆索引式的设计理念，使用纯文件系统（Markdown格式）实现智能体记忆库，具有简单、直观、高效的特点。

### 1.2 核心特性

- ✅ **纯文件存储**: 使用Markdown文件，无复杂数据库依赖
- ✅ **图书馆式索引**: 分级目录索引，快速定位信息
- ✅ **多维度分类**: 涵盖工作、生活、成长等全方位场景
- ✅ **安全可控**: 分级权限管理，加密存储敏感信息
- ✅ **易于扩展**: 模块化设计，便于添加新功能
- ✅ **跨平台兼容**: 标准文件系统，支持多设备同步

### 1.3 技术栈

- **存储格式**: Markdown (.md)
- **文件编码**: UTF-8
- **目录结构**: 树形层级结构
- **权限控制**: 基于角色的访问控制 (RBAC)
- **加密算法**: AES-256 (用于敏感信息)

---

## 2. 系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                    用户交互层                            │
│              (User Interface Layer)                     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  智能体服务层                            │
│              (Agent Service Layer)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ 意图分析  │  │ 检索引擎  │  │ 内容处理  │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  业务逻辑层                              │
│              (Business Logic Layer)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ 权限管理  │  │ 索引管理  │  │ 加密服务  │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  数据存储层                              │
│              (Data Storage Layer)                       │
│  ┌──────────────────────────────────────────┐          │
│  │         文件系统 (Markdown Files)         │          │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │          │
│  │  │ 分类目录 │  │  内容文件 │  │  索引文件 │  │          │
│  │  └─────────┘  └─────────┘  └─────────┘  │          │
│  └──────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

### 2.2 目录结构设计

```
记忆库/
│
├── 分类目录.md                          # 根目录索引
│
├── 01-工作事业/
│   ├── 分类目录.md
│   ├── 项目管理/
│   │   ├── 分类目录.md
│   │   ├── 项目A.md
│   │   └── 项目B.md
│   ├── 技能提升/
│   │   ├── 分类目录.md
│   │   ├── python技能.md
│   │   └── 沟通技巧.md
│   └── 职业规划.md
│
├── 02-生活日常/
│   ├── 分类目录.md
│   ├── 健康管理/
│   │   ├── 分类目录.md
│   │   ├── 体检记录.md
│   │   └── 运动计划.md
│   ├── 家庭事务/
│   │   ├── 分类目录.md
│   │   ├── 家人信息.md
│   │   └── 重要日期.md
│   └── 购物清单.md
│
├── 03-个人成长/
│   ├── 分类目录.md
│   ├── 阅读笔记/
│   ├── 学习计划/
│   └── 目标追踪.md
│
├── 04-社交关系/
│   ├── 分类目录.md
│   ├── 朋友通讯录/
│   ├── 社交活动/
│   └── 人脉管理.md
│
├── 05-财务管理/
│   ├── 分类目录.md
│   ├── 账户信息/
│   ├── 投资理财/
│   └── 消费记录.md
│
├── 06-密码密钥/                         # 专用密码存储区
│   ├── 分类目录.md
│   ├── API密钥/
│   │   ├── 分类目录.md
│   │   ├── openai-api.md
│   │   └── github-token.md
│   ├── 账号密码/
│   │   ├── 分类目录.md
│   │   ├── 银行账户.md
│   │   └── 社交账号.md
│   └── 证书密钥/
│       ├── 分类目录.md
│       └── ssh-key.md
│
├── 07-资源收藏/
│   ├── 分类目录.md
│   ├── 网站书签/
│   ├── 工具软件/
│   └── 素材资源.md
│
└── 08-临时便签/
    ├── 分类目录.md
    ├── 待办事项.md
    └── 临时想法.md
```

### 2.3 核心组件

#### 2.3.1 索引管理器 (IndexManager)
- 负责维护分类目录.md文件
- 自动更新索引信息
- 提供快速检索接口

#### 2.3.2 文件管理器 (FileManager)
- 负责文件的创建、读取、更新、删除
- 维护文件元数据
- 处理文件版本控制

#### 2.3.3 权限管理器 (PermissionManager)
- 管理智能体访问权限
- 验证访问请求
- 记录访问日志

#### 2.3.4 加密服务 (EncryptionService)
- 提供敏感信息加密/解密
- 管理加密密钥
- 处理安全存储

---

## 3. 数据结构设计

### 3.1 分类目录.md 标准格式

```markdown
# [目录名称] - 分类目录

## 📋 目录说明
[该分类的用途和范围说明]

## 📂 子目录列表
| 目录名 | 说明 | 包含文件数 | 创建时间 |
|--------|------|-----------|----------|
| 子目录1 | 说明 | 3 | 2026-03-05 |

## 📄 文件索引
| 文件名 | 简介 | 标签 | 重要程度 | 更新时间 |
|--------|------|------|----------|----------|
| 文件1.md | 文件作用说明 | #标签1 #标签2 | ⭐⭐⭐ | 2026-03-05 |

## 🔍 快速查找
- 按标签: #标签名
- 按类型: [类型说明]
- 按时间: [时间范围]

## ⚠️ 注意事项
[特殊说明、权限要求等]

## 📊 统计信息
- 总文件数: X
- 总目录数: Y
- 最后更新: YYYY-MM-DD HH:mm:ss
```

### 3.2 普通内容文件格式

```markdown
# [文件标题]

## 📌 基本信息
- **创建时间**: YYYY-MM-DD
- **最后更新**: YYYY-MM-DD HH:mm:ss
- **标签**: #标签1 #标签2 #标签3
- **重要程度**: ⭐⭐⭐⭐⭐ (1-5星)
- **访问权限**: public/private/encrypted
- **版本**: v1.0

## 📝 核心内容
[主要内容区域]

## 🔗 相关文件
- [相关文件1](相对路径)
- [相关文件2](相对路径)

## 📎 附件
- [附件名称](附件路径)

## 📊 更新历史
| 日期 | 版本 | 更新内容 | 更新人 |
|------|------|----------|--------|
| YYYY-MM-DD | v1.0 | 初始创建 | Agent-X |

## 💭 备注
[其他补充信息]
```

### 3.3 密码密钥文件格式

```markdown
# [密钥名称]

## 🔐 安全信息
- **加密级别**: high/medium/low
- **授权智能体**: [智能体ID列表，逗号分隔]
- **最后使用**: YYYY-MM-DD HH:mm:ss
- **有效期至**: YYYY-MM-DD
- **访问次数**: X次

## 🔑 密钥内容
```
[加密后的密钥内容]
或
[密钥存储位置指引]
```

## 📋 使用记录
| 时间 | 智能体ID | 用途 | 结果 | IP地址 |
|------|----------|------|------|--------|
| YYYY-MM-DD HH:mm | agent_001 | API调用 | 成功 | 192.168.1.1 |

## ⚠️ 安全提示
- [安全注意事项]
- [使用限制]
- [过期提醒]

## 🔄 更新历史
| 日期 | 操作 | 操作人 |
|------|------|--------|
| YYYY-MM-DD | 创建密钥 | User |
```

### 3.4 元数据结构 (JSON格式，用于程序处理)

```json
{
  "file_info": {
    "id": "uuid",
    "name": "文件名.md",
    "path": "/完整路径/文件名.md",
    "type": "content|password|index",
    "created_at": "2026-03-05T10:00:00Z",
    "updated_at": "2026-03-05T10:00:00Z",
    "size": 1024,
    "version": "1.0"
  },
  "metadata": {
    "tags": ["标签1", "标签2"],
    "importance": 5,
    "permission": "public",
    "category": "工作事业",
    "subcategory": "项目管理"
  },
  "security": {
    "encrypted": false,
    "encryption_level": null,
    "authorized_agents": [],
    "access_count": 0
  },
  "index": {
    "keywords": ["关键词1", "关键词2"],
    "summary": "文件摘要",
    "related_files": ["相关文件路径"]
  }
}
```

---

## 4. 功能模块设计

### 4.1 文件管理模块

#### 4.1.1 功能列表
- 创建文件
- 读取文件
- 更新文件
- 删除文件
- 移动文件
- 复制文件
- 文件搜索
- 批量操作

#### 4.1.2 接口定义

```python
class FileManager:
    def create_file(self, path: str, content: str, metadata: dict) -> bool:
        """创建新文件"""
        pass
    
    def read_file(self, path: str, agent_id: str) -> dict:
        """读取文件内容"""
        pass
    
    def update_file(self, path: str, content: str, agent_id: str) -> bool:
        """更新文件内容"""
        pass
    
    def delete_file(self, path: str, agent_id: str) -> bool:
        """删除文件"""
        pass
    
    def move_file(self, old_path: str, new_path: str, agent_id: str) -> bool:
        """移动文件"""
        pass
    
    def search_files(self, query: str, filters: dict) -> list:
        """搜索文件"""
        pass
```

### 4.2 索引管理模块

#### 4.2.1 功能列表
- 自动生成分类目录.md
- 更新索引信息
- 重建索引
- 标签管理
- 关键词提取

#### 4.2.2 接口定义

```python
class IndexManager:
    def generate_index(self, directory: str) -> bool:
        """生成目录索引"""
        pass
    
    def update_index(self, directory: str, file_path: str, action: str) -> bool:
        """更新索引信息"""
        pass
    
    def rebuild_index(self, root_path: str) -> bool:
        """重建整个索引系统"""
        pass
    
    def search_by_tag(self, tag: str) -> list:
        """按标签搜索"""
        pass
    
    def search_by_keyword(self, keyword: str) -> list:
        """按关键词搜索"""
        pass
```

### 4.3 权限管理模块

#### 4.3.1 功能列表
- 智能体注册
- 权限分配
- 权限验证
- 访问日志记录
- 权限回收

#### 4.3.2 权限级别

| 级别 | 代码 | 说明 | 可访问内容 |
|------|------|------|-----------|
| 公开 | public | 所有智能体可访问 | 公开级文件 |
| 内部 | internal | 授权智能体可访问 | 公开+内部级文件 |
| 私密 | private | 特定智能体可访问 | 公开+内部+私密级文件 |
| 超级 | super | 超级管理员权限 | 所有文件 |

#### 4.3.3 接口定义

```python
class PermissionManager:
    def register_agent(self, agent_id: str, level: str) -> bool:
        """注册智能体"""
        pass
    
    def grant_permission(self, agent_id: str, file_path: str, permission: str) -> bool:
        """授予权限"""
        pass
    
    def revoke_permission(self, agent_id: str, file_path: str) -> bool:
        """回收权限"""
        pass
    
    def check_permission(self, agent_id: str, file_path: str, action: str) -> bool:
        """检查权限"""
        pass
    
    def log_access(self, agent_id: str, file_path: str, action: str, result: str) -> bool:
        """记录访问日志"""
        pass
```

### 4.4 加密服务模块

#### 4.4.1 功能列表
- 敏感信息加密
- 敏感信息解密
- 密钥管理
- 加密级别控制

#### 4.4.2 加密级别

| 级别 | 算法 | 密钥长度 | 适用场景 |
|------|------|----------|----------|
| 低 | AES-128 | 128位 | 一般敏感信息 |
| 中 | AES-256 | 256位 | 重要敏感信息 |
| 高 | AES-256 + RSA | 256位+2048位 | 极度敏感信息 |

#### 4.4.3 接口定义

```python
class EncryptionService:
    def encrypt(self, data: str, level: str) -> str:
        """加密数据"""
        pass
    
    def decrypt(self, encrypted_data: str, agent_id: str) -> str:
        """解密数据"""
        pass
    
    def generate_key(self, level: str) -> str:
        """生成加密密钥"""
        pass
    
    def store_key(self, key_id: str, key: str, agent_id: str) -> bool:
        """存储密钥"""
        pass
```

---

## 5. 检索机制

### 5.1 检索流程

```
用户查询请求
      ↓
  意图分析模块
      ↓
  提取关键信息
      ↓
  确定检索范围
      ↓
  查找分类目录.md
      ↓
  定位目标文件
      ↓
  权限验证
      ↓
  读取文件内容
      ↓
  提取相关信息
      ↓
  格式化返回结果
```

### 5.2 检索策略

#### 5.2.1 直接检索
适用于明确知道文件路径的情况

```python
def direct_search(file_path: str, agent_id: str) -> dict:
    """
    直接检索指定文件
    1. 验证权限
    2. 读取文件
    3. 返回内容
    """
    pass
```

#### 5.2.2 分类检索
适用于知道文件类别的情况

```python
def category_search(category: str, keywords: list, agent_id: str) -> list:
    """
    分类检索
    1. 定位到分类目录
    2. 查找分类目录.md
    3. 匹配关键词
    4. 返回文件列表
    """
    pass
```

#### 5.2.3 全文检索
适用于不确定文件位置的情况

```python
def fulltext_search(query: str, agent_id: str) -> list:
    """
    全文检索
    1. 遍历所有分类目录.md
    2. 匹配标签、关键词、摘要
    3. 排序结果
    4. 返回文件列表
    """
    pass
```

### 5.3 检索优化

#### 5.3.1 缓存机制
- 缓存热门文件的分类目录.md
- 缓存常用检索结果
- 定期清理缓存

#### 5.3.2 索引优化
- 建立标签索引表
- 建立关键词索引表
- 建立时间索引表

#### 5.3.3 智能推荐
- 基于用户历史行为推荐
- 基于文件关联性推荐
- 基于时间相关性推荐

### 5.4 检索示例

#### 示例1: 查找API密钥

**用户查询**: "我的OpenAI API密钥是什么?"

**检索过程**:
```python
# 1. 意图分析
intent = analyze_intent("我的OpenAI API密钥是什么?")
# 结果: {"category": "密码密钥", "subcategory": "API密钥", "target": "OpenAI"}

# 2. 定位目录
directory = locate_directory("06-密码密钥/API密钥/")

# 3. 查看分类目录
index = read_file("06-密码密钥/API密钥/分类目录.md")

# 4. 匹配文件
file_path = match_file(index, "OpenAI")
# 结果: "06-密码密钥/API密钥/openai-api.md"

# 5. 权限验证
has_permission = check_permission(agent_id, file_path, "read")

# 6. 读取并解密
content = read_file(file_path, agent_id)
decrypted_content = decrypt(content, agent_id)

# 7. 返回结果
return format_response(decrypted_content)
```

#### 示例2: 查找项目文档

**用户查询**: "我上周的项目会议记录在哪?"

**检索过程**:
```python
# 1. 意图分析
intent = analyze_intent("我上周的项目会议记录在哪?")
# 结果: {"category": "工作事业", "subcategory": "项目管理", "time_range": "上周"}

# 2. 全文检索
results = fulltext_search("项目 会议记录 上周", agent_id)

# 3. 时间过滤
filtered_results = filter_by_time(results, "last_week")

# 4. 排序
sorted_results = sort_by_relevance(filtered_results)

# 5. 返回结果
return format_response(sorted_results)
```

---

## 6. 安全权限机制

### 6.1 权限模型

#### 6.1.1 RBAC模型 (基于角色的访问控制)

```
用户/智能体
    ↓
   角色
    ↓
   权限
    ↓
  资源(文件)
```

#### 6.1.2 角色定义

| 角色ID | 角色名称 | 权限范围 | 说明 |
|--------|----------|----------|------|
| role_001 | 超级管理员 | 所有权限 | 系统管理 |
| role_002 | 管理员 | 大部分权限 | 分类管理 |
| role_003 | 高级用户 | 内部权限 | 高级智能体 |
| role_004 | 普通用户 | 基本权限 | 普通智能体 |
| role_005 | 访客 | 公开权限 | 临时智能体 |

### 6.2 访问控制

#### 6.2.1 文件级权限

每个文件都有权限标记：
- `permission: public` - 公开访问
- `permission: internal` - 内部访问
- `permission: private` - 私密访问
- `permission: encrypted` - 加密访问

#### 6.2.2 操作级权限

| 操作 | 权限要求 | 说明 |
|------|----------|------|
| 读取 | read | 读取文件内容 |
| 写入 | write | 修改文件内容 |
| 创建 | create | 创建新文件 |
| 删除 | delete | 删除文件 |
| 管理 | admin | 管理权限设置 |

#### 6.2.3 权限验证流程

```python
def verify_permission(agent_id: str, file_path: str, action: str) -> bool:
    """
    权限验证流程
    1. 获取智能体角色
    2. 获取文件权限级别
    3. 检查角色是否有对应操作权限
    4. 记录验证结果
    """
    # 获取智能体信息
    agent = get_agent(agent_id)
    
    # 获取文件信息
    file_info = get_file_info(file_path)
    
    # 检查权限
    if file_info['permission'] == 'public':
        return True
    elif file_info['permission'] == 'internal':
        return agent['role'] in ['admin', 'advanced']
    elif file_info['permission'] == 'private':
        return agent_id in file_info['authorized_agents']
    elif file_info['permission'] == 'encrypted':
        return has_decryption_key(agent_id, file_path)
    
    return False
```

### 6.3 安全存储

#### 6.3.1 敏感信息加密流程

```
原始数据
    ↓
  数据分类
    ↓
  选择加密级别
    ↓
  生成加密密钥
    ↓
  加密数据
    ↓
  存储加密数据
    ↓
  密钥安全存储
```

#### 6.3.2 密钥管理

- **主密钥**: 用于加密其他密钥，存储在安全区域
- **数据密钥**: 用于加密实际数据，由主密钥加密存储
- **访问密钥**: 用于智能体访问，有有效期限制

### 6.4 审计日志

#### 6.4.1 日志格式

```json
{
  "log_id": "uuid",
  "timestamp": "2026-03-05T10:00:00Z",
  "agent_id": "agent_001",
  "action": "read|write|create|delete",
  "file_path": "/path/to/file.md",
  "result": "success|failed",
  "ip_address": "192.168.1.1",
  "user_agent": "Agent-X/1.0",
  "details": "详细描述"
}
```

#### 6.4.2 日志存储

- 日志文件位置: `记忆库/.logs/access.log`
- 日志轮转: 按天轮转，保留30天
- 日志格式: JSON Lines格式

---

## 7. API接口设计

### 7.1 文件操作API

#### 7.1.1 创建文件

**接口**: `POST /api/v1/files`

**请求参数**:
```json
{
  "path": "/01-工作事业/项目管理/新项目.md",
  "content": "文件内容",
  "metadata": {
    "tags": ["项目", "重要"],
    "importance": 5,
    "permission": "private"
  },
  "agent_id": "agent_001"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "文件创建成功",
  "data": {
    "file_id": "uuid",
    "path": "/01-工作事业/项目管理/新项目.md",
    "created_at": "2026-03-05T10:00:00Z"
  }
}
```

#### 7.1.2 读取文件

**接口**: `GET /api/v1/files/{file_path}`

**请求参数**:
```
file_path: 文件路径（URL编码）
agent_id: 智能体ID
```

**响应**:
```json
{
  "code": 200,
  "message": "读取成功",
  "data": {
    "content": "文件内容",
    "metadata": {
      "created_at": "2026-03-05T10:00:00Z",
      "updated_at": "2026-03-05T10:00:00Z",
      "tags": ["项目", "重要"],
      "importance": 5
    }
  }
}
```

#### 7.1.3 更新文件

**接口**: `PUT /api/v1/files/{file_path}`

**请求参数**:
```json
{
  "content": "更新后的内容",
  "agent_id": "agent_001",
  "version": "1.0"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "file_path": "/01-工作事业/项目管理/新项目.md",
    "updated_at": "2026-03-05T11:00:00Z",
    "version": "1.1"
  }
}
```

#### 7.1.4 删除文件

**接口**: `DELETE /api/v1/files/{file_path}`

**请求参数**:
```
file_path: 文件路径
agent_id: 智能体ID
```

**响应**:
```json
{
  "code": 200,
  "message": "删除成功"
}
```

### 7.2 检索API

#### 7.2.1 搜索文件

**接口**: `POST /api/v1/search`

**请求参数**:
```json
{
  "query": "OpenAI API密钥",
  "filters": {
    "category": "密码密钥",
    "tags": ["API"],
    "time_range": {
      "start": "2026-01-01",
      "end": "2026-03-05"
    }
  },
  "agent_id": "agent_001",
  "limit": 10,
  "offset": 0
}
```

**响应**:
```json
{
  "code": 200,
  "message": "搜索成功",
  "data": {
    "total": 1,
    "results": [
      {
        "file_path": "/06-密码密钥/API密钥/openai-api.md",
        "title": "OpenAI API密钥",
        "summary": "OpenAI API访问密钥",
        "relevance": 0.95,
        "updated_at": "2026-03-05T10:00:00Z"
      }
    ]
  }
}
```

#### 7.2.2 按标签搜索

**接口**: `GET /api/v1/search/tags/{tag}`

**请求参数**:
```
tag: 标签名
agent_id: 智能体ID
```

**响应**:
```json
{
  "code": 200,
  "message": "搜索成功",
  "data": {
    "tag": "API",
    "files": [
      {
        "file_path": "/06-密码密钥/API密钥/openai-api.md",
        "title": "OpenAI API密钥"
      }
    ]
  }
}
```

### 7.3 权限管理API

#### 7.3.1 授权智能体

**接口**: `POST /api/v1/permissions/grant`

**请求参数**:
```json
{
  "agent_id": "agent_002",
  "file_path": "/06-密码密钥/API密钥/openai-api.md",
  "permission": "read",
  "expires_at": "2026-12-31T23:59:59Z",
  "granted_by": "agent_001"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "授权成功"
}
```

#### 7.3.2 回收权限

**接口**: `DELETE /api/v1/permissions/revoke`

**请求参数**:
```json
{
  "agent_id": "agent_002",
  "file_path": "/06-密码密钥/API密钥/openai-api.md",
  "revoked_by": "agent_001"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "权限已回收"
}
```

### 7.4 索引管理API

#### 7.4.1 重建索引

**接口**: `POST /api/v1/index/rebuild`

**请求参数**:
```json
{
  "root_path": "/记忆库",
  "agent_id": "agent_001"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "索引重建成功",
  "data": {
    "total_files": 150,
    "total_directories": 30,
    "duration": "5.2s"
  }
}
```

---

## 8. 开发规范

### 8.1 文件命名规范

#### 8.1.1 目录命名
- 使用数字前缀排序: `01-工作事业`, `02-生活日常`
- 使用中文名称，便于理解
- 避免特殊字符: `\ / : * ? " < > |`
- 长度限制: 不超过30个字符

#### 8.1.2 文件命名
- 使用描述性名称: `项目A会议记录.md`
- 使用中文名称
- 避免特殊字符
- 长度限制: 不超过50个字符
- 统一扩展名: `.md`

### 8.2 内容编写规范

#### 8.2.1 Markdown格式
- 使用标准Markdown语法
- 统一使用UTF-8编码
- 换行符: LF (Unix风格)
- 缩进: 2空格

#### 8.2.2 标题层级
- 一级标题: 文件标题
- 二级标题: 主要章节
- 三级标题: 子章节
- 层级不超过4级

#### 8.2.3 标签规范
- 格式: `#标签名`
- 使用小写字母和中文
- 多个标签用空格分隔
- 建议每个文件3-5个标签

### 8.3 代码规范

#### 8.3.1 Python代码规范
- 遵循PEP 8规范
- 使用类型注解
- 函数和类添加文档字符串
- 单元测试覆盖率 > 80%

#### 8.3.2 注释规范
```python
def read_file(file_path: str, agent_id: str) -> dict:
    """
    读取文件内容
    
    Args:
        file_path: 文件路径
        agent_id: 智能体ID
    
    Returns:
        dict: 包含文件内容和元数据的字典
        
    Raises:
        PermissionError: 权限不足
        FileNotFoundError: 文件不存在
    """
    pass
```

### 8.4 Git提交规范

#### 8.4.1 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 8.4.2 Type类型
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

#### 8.4.3 示例
```
feat(file-manager): 添加文件加密功能

- 实现AES-256加密
- 添加密钥管理
- 支持多级加密

Closes #123
```

---

## 9. 测试方案

### 9.1 单元测试

#### 9.1.1 测试范围
- 文件管理模块
- 索引管理模块
- 权限管理模块
- 加密服务模块

#### 9.1.2 测试框架
- 使用 `pytest` 框架
- 测试覆盖率工具: `pytest-cov`
- 目标覆盖率: > 80%

#### 9.1.3 测试示例

```python
import pytest
from file_manager import FileManager

class TestFileManager:
    def setup_method(self):
        self.fm = FileManager()
        self.test_file = "/tmp/test.md"
    
    def test_create_file(self):
        """测试文件创建"""
        result = self.fm.create_file(
            self.test_file,
            "# 测试文件\n\n内容",
            {"tags": ["测试"]}
        )
        assert result == True
        assert os.path.exists(self.test_file)
    
    def test_read_file(self):
        """测试文件读取"""
        content = self.fm.read_file(self.test_file, "agent_001")
        assert content['content'] == "# 测试文件\n\n内容"
    
    def teardown_method(self):
        """清理测试文件"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
```

### 9.2 集成测试

#### 9.2.1 测试场景
- 完整的文件操作流程
- 权限验证流程
- 检索流程
- 加密解密流程

#### 9.2.2 测试数据
- 准备完整的测试记忆库
- 包含各种类型的文件
- 包含不同权限级别的文件

### 9.3 性能测试

#### 9.3.1 测试指标
- 文件读取速度: < 100ms
- 文件写入速度: < 200ms
- 检索响应时间: < 500ms
- 并发处理能力: > 100 QPS

#### 9.3.2 测试工具
- 使用 `locust` 进行压力测试
- 使用 `memory_profiler` 进行内存分析

### 9.4 安全测试

#### 9.4.1 测试项目
- 权限绕过测试
- 加密强度测试
- 注入攻击测试
- 敏感信息泄露测试

#### 9.4.2 测试工具
- OWASP ZAP
- SQLMap (用于注入测试)

---

## 10. 部署方案

### 10.1 系统要求

#### 10.1.1 硬件要求
- CPU: 2核心以上
- 内存: 4GB以上
- 存储: 根据记忆库大小，建议10GB以上

#### 10.1.2 软件要求
- 操作系统: Linux / macOS / Windows
- Python: 3.8+
- 文件系统: 支持UTF-8编码

### 10.2 部署架构

#### 10.2.1 单机部署
```
┌─────────────────────────┐
│    应用服务器            │
│  ┌───────────────────┐  │
│  │   Skill服务       │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │   文件系统         │  │
│  │   (记忆库)        │  │
│  └───────────────────┘  │
└─────────────────────────┘
```

#### 10.2.2 分布式部署
```
┌──────────────┐     ┌──────────────┐
│  负载均衡器   │────→│  应用服务器1  │
└──────────────┘     └──────────────┘
                            │
                            ↓
                     ┌──────────────┐
                     │  应用服务器2  │
                     └──────────────┘
                            │
                            ↓
                     ┌──────────────┐
                     │  文件存储     │
                     │  (NFS/S3)    │
                     └──────────────┘
```

### 10.3 配置管理

#### 10.3.1 配置文件格式

```yaml
# config.yaml
memory_bank:
  root_path: "/data/memory_bank"
  encoding: "utf-8"
  max_file_size: 10485760  # 10MB
  
security:
  encryption:
    algorithm: "AES-256"
    key_storage: "/data/keys"
  
permission:
  default_level: "internal"
  super_admin: "agent_001"
  
logging:
  level: "INFO"
  file: "/var/log/memory_bank.log"
  max_size: 10485760
  backup_count: 10
  
performance:
  cache_enabled: true
  cache_size: 1000
  index_update_interval: 300
```

### 10.4 监控告警

#### 10.4.1 监控指标
- 文件系统使用率
- API响应时间
- 错误率
- 并发连接数

#### 10.4.2 告警规则
- 磁盘使用率 > 80%
- API响应时间 > 1s
- 错误率 > 5%
- 服务不可用

### 10.5 备份策略

#### 10.5.1 备份方案
- **全量备份**: 每周一次
- **增量备份**: 每天一次
- **实时同步**: 重要文件实时同步

#### 10.5.2 备份存储
- 本地备份: `/backup/local`
- 远程备份: 云存储 (S3/OSS)
- 异地备份: 异地机房

#### 10.5.3 恢复测试
- 每月进行一次恢复演练
- 验证备份数据完整性
- 记录恢复时间

---

## 11. Skill集成与自动调用

### 11.1 Skill标准结构

本项目已按照标准Skill格式创建，位于 `.trae/skills/memory-bank/` 目录：

```
.trae/
└── skills/
    └── memory-bank/
        └── SKILL.md              # Skill定义文件
```

#### 11.1.1 SKILL.md 结构

```markdown
---
name: "memory-bank"
description: "Manages intelligent agent memory storage using library-style indexing. Automatically invoked when agent needs to store/retrieve memories, search information, or manage credentials. Supports auto-indexing and categorized storage."
---

# Memory Bank - 图书馆式记忆库
[详细内容...]
```

### 11.2 自动调用机制

#### 11.2.1 触发条件

Memory Bank技能会在以下场景自动调用：

| 触发场景 | 触发条件 | 自动操作 |
|----------|----------|----------|
| 存储记忆 | 智能体识别到重要信息 | 自动分类并存储到对应md文件 |
| 检索记忆 | 用户查询历史信息 | 自动检索并返回结果 |
| 更新记忆 | 用户要求修改信息 | 自动更新文件并同步索引 |
| 删除记忆 | 用户要求删除信息 | 自动删除文件并更新索引 |

#### 11.2.2 智能识别规则

系统会自动识别以下类型的信息并触发存储：

```python
AUTO_STORE_PATTERNS = {
    "api_key": {
        "patterns": [r"api[_-]?key", r"token", r"secret"],
        "category": "06-密码密钥/API密钥",
        "encrypt": True
    },
    "password": {
        "patterns": [r"密码", r"password", r"pwd"],
        "category": "06-密码密钥/账号密码",
        "encrypt": True
    },
    "project": {
        "patterns": [r"项目", r"project", r"任务"],
        "category": "01-工作事业/项目管理",
        "encrypt": False
    },
    "meeting": {
        "patterns": [r"会议", r"meeting", r"讨论"],
        "category": "01-工作事业/项目管理",
        "encrypt": False
    },
    "health": {
        "patterns": [r"健康", r"体检", r"运动"],
        "category": "02-生活日常/健康管理",
        "encrypt": False
    },
    "preference": {
        "patterns": [r"喜欢", r"偏好", r"prefer"],
        "category": "03-个人成长",
        "encrypt": False
    }
}
```

### 11.3 记忆碎片自动处理流程

#### 11.3.1 存储流程

```
智能体产生记忆碎片
        ↓
    内容分析
        ↓
    类型识别
        ↓
    分类定位
        ↓
  创建/更新MD文件
        ↓
    更新索引
        ↓
    返回确认
```

#### 11.3.2 代码实现示例

```python
class MemoryBankSkill:
    """Memory Bank技能核心类"""
    
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.file_manager = FileManager(root_path)
        self.index_manager = IndexManager(root_path)
        self.permission_manager = PermissionManager()
        self.encryption_service = EncryptionService()
    
    def auto_store_memory(self, content: str, context: dict = None):
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
        category = self._determine_category(content_type)
        
        # 3. 生成文件名
        filename = self._generate_filename(content, content_type)
        
        # 4. 准备文件内容
        file_content = self._prepare_file_content(content, content_type, context)
        
        # 5. 检查是否需要加密
        if content_type.get('encrypt', False):
            file_content = self.encryption_service.encrypt(file_content, 'high')
        
        # 6. 创建文件
        file_path = f"{category}/{filename}.md"
        self.file_manager.create_file(file_path, file_content, {
            'tags': content_type.get('tags', []),
            'permission': 'encrypted' if content_type.get('encrypt') else 'private'
        })
        
        # 7. 更新索引
        self.index_manager.update_index(category, file_path, 'create')
        
        # 8. 返回结果
        return {
            'success': True,
            'file_path': file_path,
            'category': category,
            'encrypted': content_type.get('encrypt', False)
        }
    
    def _analyze_content_type(self, content: str) -> dict:
        """分析内容类型"""
        content_lower = content.lower()
        
        for type_name, config in AUTO_STORE_PATTERNS.items():
            for pattern in config['patterns']:
                if re.search(pattern, content_lower):
                    return {
                        'type': type_name,
                        'category': config['category'],
                        'encrypt': config['encrypt'],
                        'tags': [type_name]
                    }
        
        # 默认分类
        return {
            'type': 'general',
            'category': '08-临时便签',
            'encrypt': False,
            'tags': ['临时']
        }
    
    def auto_retrieve_memory(self, query: str, agent_id: str) -> list:
        """
        自动检索记忆
        
        Args:
            query: 查询内容
            agent_id: 智能体ID
        
        Returns:
            list: 检索结果列表
        """
        # 1. 分析查询意图
        intent = self._analyze_query_intent(query)
        
        # 2. 确定检索范围
        search_scope = self._determine_search_scope(intent)
        
        # 3. 执行检索
        results = []
        for category in search_scope:
            category_results = self._search_in_category(
                category, 
                intent['keywords'],
                agent_id
            )
            results.extend(category_results)
        
        # 4. 排序和过滤
        results = self._rank_results(results, intent)
        
        # 5. 解密需要的内容
        for result in results:
            if result.get('encrypted'):
                result['content'] = self.encryption_service.decrypt(
                    result['content'],
                    agent_id
                )
        
        return results
    
    def auto_update_memory(self, file_path: str, new_content: str, agent_id: str):
        """自动更新记忆"""
        # 1. 权限验证
        if not self.permission_manager.check_permission(agent_id, file_path, 'write'):
            raise PermissionError("无权限修改此文件")
        
        # 2. 读取原文件
        old_content = self.file_manager.read_file(file_path, agent_id)
        
        # 3. 合并内容
        merged_content = self._merge_content(old_content, new_content)
        
        # 4. 更新文件
        self.file_manager.update_file(file_path, merged_content, agent_id)
        
        # 5. 更新索引
        category = os.path.dirname(file_path)
        self.index_manager.update_index(category, file_path, 'update')
        
        return {'success': True, 'file_path': file_path}
    
    def auto_delete_memory(self, file_path: str, agent_id: str):
        """自动删除记忆"""
        # 1. 权限验证
        if not self.permission_manager.check_permission(agent_id, file_path, 'delete'):
            raise PermissionError("无权限删除此文件")
        
        # 2. 删除文件
        self.file_manager.delete_file(file_path, agent_id)
        
        # 3. 更新索引
        category = os.path.dirname(file_path)
        self.index_manager.update_index(category, file_path, 'delete')
        
        return {'success': True}
```

### 11.4 索引自动更新机制

#### 11.4.1 索引更新触发器

```python
class IndexManager:
    """索引管理器"""
    
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.index_cache = {}
    
    def update_index(self, category: str, file_path: str, action: str):
        """
        更新索引
        
        Args:
            category: 分类路径
            file_path: 文件路径
            action: 操作类型 (create/update/delete)
        """
        index_file = f"{category}/分类目录.md"
        
        # 读取现有索引
        index_content = self._read_index(index_file)
        
        # 根据操作类型更新索引
        if action == 'create':
            self._add_to_index(index_content, file_path)
        elif action == 'update':
            self._update_in_index(index_content, file_path)
        elif action == 'delete':
            self._remove_from_index(index_content, file_path)
        
        # 写回索引文件
        self._write_index(index_file, index_content)
        
        # 更新缓存
        self._update_cache(category, index_content)
    
    def _add_to_index(self, index_content: dict, file_path: str):
        """添加文件到索引"""
        file_info = self._get_file_info(file_path)
        
        index_content['files'].append({
            'name': os.path.basename(file_path),
            'path': file_path,
            'summary': file_info['summary'],
            'tags': file_info['tags'],
            'updated_at': datetime.now().isoformat()
        })
    
    def _update_in_index(self, index_content: dict, file_path: str):
        """更新索引中的文件信息"""
        file_info = self._get_file_info(file_path)
        
        for file_entry in index_content['files']:
            if file_entry['path'] == file_path:
                file_entry.update({
                    'summary': file_info['summary'],
                    'tags': file_info['tags'],
                    'updated_at': datetime.now().isoformat()
                })
                break
    
    def _remove_from_index(self, index_content: dict, file_path: str):
        """从索引中移除文件"""
        index_content['files'] = [
            f for f in index_content['files'] 
            if f['path'] != file_path
        ]
```

### 11.5 与智能体的集成方式

#### 11.5.1 作为默认技能加载

在智能体初始化时，自动加载Memory Bank技能：

```python
class Agent:
    """智能体基类"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.skills = {}
        
        # 加载默认技能
        self._load_default_skills()
    
    def _load_default_skills(self):
        """加载默认技能"""
        # 加载Memory Bank技能
        memory_bank = MemoryBankSkill(
            root_path=config.MEMORY_BANK_ROOT
        )
        self.skills['memory_bank'] = memory_bank
        
        # 其他默认技能...
    
    def process_message(self, message: str) -> str:
        """处理消息"""
        # 1. 分析消息意图
        intent = self._analyze_intent(message)
        
        # 2. 检查是否需要使用Memory Bank
        if self._needs_memory_operation(intent):
            # 自动调用Memory Bank
            result = self._auto_invoke_memory_bank(intent, message)
            return result
        
        # 3. 正常处理消息
        response = self._generate_response(message)
        
        # 4. 检查是否需要存储记忆
        if self._should_store_memory(response):
            self.skills['memory_bank'].auto_store_memory(
                content=response,
                context={'message': message}
            )
        
        return response
    
    def _needs_memory_operation(self, intent: dict) -> bool:
        """判断是否需要记忆操作"""
        memory_keywords = ['记住', '回忆', '查询', '我的', '之前', '历史']
        return any(kw in intent.get('text', '') for kw in memory_keywords)
    
    def _auto_invoke_memory_bank(self, intent: dict, message: str):
        """自动调用Memory Bank"""
        operation = intent.get('operation')
        
        if operation == 'store':
            return self.skills['memory_bank'].auto_store_memory(
                content=message,
                context=intent
            )
        elif operation == 'retrieve':
            return self.skills['memory_bank'].auto_retrieve_memory(
                query=message,
                agent_id=self.agent_id
            )
        elif operation == 'update':
            return self.skills['memory_bank'].auto_update_memory(
                file_path=intent.get('file_path'),
                new_content=message,
                agent_id=self.agent_id
            )
        elif operation == 'delete':
            return self.skills['memory_bank'].auto_delete_memory(
                file_path=intent.get('file_path'),
                agent_id=self.agent_id
            )
```

#### 11.5.2 配置文件

```yaml
# agent_config.yaml
agent:
  id: "agent_001"
  name: "智能助手"
  
skills:
  memory_bank:
    enabled: true                    # 启用Memory Bank技能
    auto_invoke: true                # 自动调用
    auto_store: true                 # 自动存储记忆
    root_path: "/data/memory_bank"   # 记忆库根目录
    
    auto_store_rules:
      - type: "api_key"
        enabled: true
        encrypt: true
      - type: "password"
        enabled: true
        encrypt: true
      - type: "preference"
        enabled: true
        encrypt: false
      - type: "project"
        enabled: true
        encrypt: false
    
    index:
      auto_update: true              # 自动更新索引
      cache_enabled: true            # 启用索引缓存
      update_interval: 300           # 索引更新间隔(秒)
```

### 11.6 使用示例

#### 示例1: 自动存储API密钥

**用户**: "记住我的OpenAI API密钥是sk-proj-xxxxx"

**智能体处理流程**:
```python
# 1. 意图分析
intent = {
    'operation': 'store',
    'type': 'api_key',
    'content': 'OpenAI API密钥是sk-proj-xxxxx'
}

# 2. 自动调用Memory Bank
result = memory_bank.auto_store_memory(
    content="OpenAI API密钥是sk-proj-xxxxx",
    context={'user_message': "记住我的OpenAI API密钥是sk-proj-xxxxx"}
)

# 3. 自动处理结果
# - 识别为API密钥类型
# - 自动分类到: 06-密码密钥/API密钥/
# - 自动加密存储
# - 自动更新索引

# 4. 返回确认
return "已记住您的OpenAI API密钥，已加密存储在密码库中。"
```

#### 示例2: 自动检索项目信息

**用户**: "我上周的项目会议记录在哪?"

**智能体处理流程**:
```python
# 1. 意图分析
intent = {
    'operation': 'retrieve',
    'type': 'project',
    'keywords': ['项目', '会议记录', '上周'],
    'time_range': 'last_week'
}

# 2. 自动调用Memory Bank
results = memory_bank.auto_retrieve_memory(
    query="项目 会议记录 上周",
    agent_id="agent_001"
)

# 3. 返回结果
return f"找到您的项目会议记录：\n{results[0]['summary']}\n路径：{results[0]['path']}"
```

### 11.7 监控与日志

#### 11.7.1 操作日志

所有Memory Bank操作都会记录日志：

```json
{
  "timestamp": "2026-03-05T10:00:00Z",
  "agent_id": "agent_001",
  "operation": "store",
  "file_path": "/06-密码密钥/API密钥/openai-api.md",
  "content_type": "api_key",
  "encrypted": true,
  "index_updated": true,
  "duration_ms": 45
}
```

#### 11.7.2 性能监控

```python
class MemoryBankMonitor:
    """Memory Bank性能监控"""
    
    def __init__(self):
        self.metrics = {
            'store_count': 0,
            'retrieve_count': 0,
            'update_count': 0,
            'delete_count': 0,
            'avg_store_time': 0,
            'avg_retrieve_time': 0
        }
    
    def record_operation(self, operation: str, duration: float):
        """记录操作"""
        self.metrics[f'{operation}_count'] += 1
        
        # 更新平均时间
        key = f'avg_{operation}_time'
        current_avg = self.metrics[key]
        count = self.metrics[f'{operation}_count']
        self.metrics[key] = (current_avg * (count - 1) + duration) / count
```

---

## 附录

### A. 错误码定义

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 1001 | 文件不存在 | 检查文件路径 |
| 1002 | 文件已存在 | 使用不同文件名 |
| 2001 | 权限不足 | 申请相应权限 |
| 2002 | 智能体未注册 | 注册智能体 |
| 3001 | 加密失败 | 检查加密配置 |
| 3002 | 解密失败 | 检查密钥是否正确 |
| 4001 | 索引损坏 | 重建索引 |
| 5001 | 系统错误 | 查看日志 |

### B. 常见问题FAQ

**Q1: 如何处理文件名冲突?**  
A: 系统会自动检测文件是否存在，如存在会提示用户选择覆盖或使用新名称。

**Q2: 如何迁移现有数据?**  
A: 提供数据迁移工具，支持从其他格式导入数据。

**Q3: 如何处理大文件?**  
A: 系统限制单个文件大小为10MB，超过限制的文件建议分割存储。

**Q4: 如何保证数据安全?**  
A: 采用多层安全机制：权限控制、数据加密、访问日志、定期备份。

### C. 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-03-05 | 初始版本 |

---

**文档维护者**: AI Assistant  
**最后更新**: 2026-03-05  
**文档状态**: 待审核
