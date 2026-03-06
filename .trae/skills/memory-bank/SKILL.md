---
name: "memory-bank"
description: "Manages intelligent agent memory storage using library-style indexing. Automatically invoked when agent needs to store/retrieve memories, search information, or manage credentials. Supports auto-indexing and categorized storage."
---

# Memory Bank - 图书馆式记忆库

## 概述

Memory Bank是一个基于文件系统的智能体记忆管理技能，采用图书馆索引式设计，使用Markdown文件存储记忆内容。该技能能够被智能体默认调用，自动管理记忆碎片的存储和索引更新。

## 核心功能

### 1. 自动记忆存储
- 智能体产生新记忆时自动调用
- 自动分类并存储到对应的md文件
- 自动更新分类目录索引

### 2. 快速检索
- 支持关键词搜索
- 支持标签筛选
- 支持时间范围查询
- 支持分类浏览

### 3. 密码密钥管理
- 安全存储API密钥、账号密码等敏感信息
- 加密存储机制
- 权限访问控制

### 4. 自动索引维护
- 创建/修改文件后自动更新分类目录.md
- 维护标签索引系统
- 定期清理过期信息

## 调用时机

该技能会在以下场景自动调用：

1. **存储记忆**: 当智能体需要保存重要信息时
   ```
   用户: "记住我的OpenAI API密钥是sk-xxx"
   → 自动调用memory-bank存储到 06-密码密钥/API密钥/openai-api.md
   ```

2. **检索记忆**: 当智能体需要查询历史信息时
   ```
   用户: "我的GitHub token是什么?"
   → 自动调用memory-bank检索并返回
   ```

3. **更新记忆**: 当智能体需要修改已有信息时
   ```
   用户: "更新我的项目进度"
   → 自动调用memory-bank更新对应文件
   ```

4. **删除记忆**: 当智能体需要删除过期信息时
   ```
   用户: "删除旧的API密钥"
   → 自动调用memory-bank删除并更新索引
   ```

## 目录结构

```
记忆库/
├── 分类目录.md                    # 根目录索引
├── 01-工作事业/
│   ├── 分类目录.md
│   ├── 项目管理/
│   │   ├── 分类目录.md
│   │   └── 项目A.md
│   └── 技能提升/
├── 02-生活日常/
│   ├── 分类目录.md
│   ├── 健康管理/
│   └── 家庭事务/
├── 03-个人成长/
├── 04-社交关系/
├── 05-财务管理/
├── 06-密码密钥/                   # 专用密码存储区
│   ├── 分类目录.md
│   ├── API密钥/
│   ├── 账号密码/
│   └── 证书密钥/
├── 07-资源收藏/
└── 08-临时便签/
```

## 使用示例

### 示例1: 存储API密钥

**用户输入**:
```
记住我的OpenAI API密钥是sk-proj-xxxxx，用于GPT-4访问
```

**智能体自动执行**:
1. 分析内容类型 → API密钥
2. 定位存储位置 → `06-密码密钥/API密钥/`
3. 创建/更新文件 → `openai-api.md`
4. 更新索引 → `API密钥/分类目录.md`
5. 返回确认信息

**存储结果** (`06-密码密钥/API密钥/openai-api.md`):
```markdown
# OpenAI API密钥

## 🔐 安全信息
- **加密级别**: high
- **授权智能体**: [所有智能体]
- **最后使用**: 2026-03-05
- **有效期至**: 长期有效

## 🔑 密钥内容
```
sk-proj-xxxxx
```

## 📋 使用记录
| 时间 | 智能体 | 用途 | 结果 |
|------|--------|------|------|
| 2026-03-05 | Agent | GPT-4访问 | 记录创建 |

## 💭 备注
用于GPT-4访问
```

### 示例2: 检索项目信息

**用户输入**:
```
我上周的项目会议记录在哪?
```

**智能体自动执行**:
1. 分析查询意图 → 项目会议记录 + 时间范围(上周)
2. 检索分类目录 → `01-工作事业/项目管理/分类目录.md`
3. 匹配关键词和时间
4. 返回匹配文件列表

### 示例3: 自动记忆碎片存储

**场景**: 智能体在对话中获取到重要信息

**智能体内部处理**:
```python
# 检测到重要信息
important_info = {
    "type": "preference",
    "content": "用户喜欢使用Python进行数据分析",
    "category": "个人偏好",
    "tags": ["Python", "数据分析", "偏好"]
}

# 自动调用memory-bank
memory_bank.store_memory(important_info)

# 自动存储到: 03-个人成长/学习计划/python偏好.md
# 自动更新索引: 03-个人成长/学习计划/分类目录.md
```

## API接口

### 存储记忆
```python
memory_bank.store_memory(
    content="记忆内容",
    category="分类名称",
    tags=["标签1", "标签2"],
    importance=5,
    permission="private"
)
```

### 检索记忆
```python
results = memory_bank.search_memory(
    query="搜索关键词",
    category="分类名称",
    tags=["标签"],
    time_range={"start": "2026-01-01", "end": "2026-03-05"}
)
```

### 更新记忆
```python
memory_bank.update_memory(
    file_path="文件路径",
    content="更新内容",
    agent_id="智能体ID"
)
```

### 删除记忆
```python
memory_bank.delete_memory(
    file_path="文件路径",
    agent_id="智能体ID"
)
```

## 自动化特性

### 1. 智能分类
- 自动识别内容类型
- 自动选择合适的分类目录
- 自动生成文件名

### 2. 索引同步
- 文件创建后立即更新索引
- 文件修改后自动更新索引
- 文件删除后自动清理索引

### 3. 标签管理
- 自动提取关键词作为标签
- 维护标签索引系统
- 支持标签推荐

### 4. 权限控制
- 敏感信息自动加密
- 根据内容类型设置权限
- 记录访问日志

## 配置选项

```yaml
memory_bank:
  root_path: "/path/to/memory_bank"
  auto_store: true              # 自动存储记忆
  auto_index: true              # 自动更新索引
  auto_encrypt: true            # 自动加密敏感信息
  
  categories:
    - "01-工作事业"
    - "02-生活日常"
    - "03-个人成长"
    - "04-社交关系"
    - "05-财务管理"
    - "06-密码密钥"
    - "07-资源收藏"
    - "08-临时便签"
  
  security:
    encryption_algorithm: "AES-256"
    auto_detect_sensitive: true  # 自动检测敏感信息
    
  indexing:
    update_interval: 300         # 索引更新间隔(秒)
    cache_enabled: true          # 启用缓存
```

## 最佳实践

### 1. 记忆存储
- 及时存储重要信息
- 使用准确的标签
- 设置合适的重要程度
- 定期清理过期信息

### 2. 检索优化
- 使用具体的关键词
- 结合分类和标签筛选
- 利用时间范围缩小结果

### 3. 安全管理
- 敏感信息使用加密存储
- 定期更新密钥和密码
- 审查访问日志

### 4. 维护建议
- 定期备份记忆库
- 重建索引优化性能
- 清理重复或过期内容

## 注意事项

1. **隐私保护**: 敏感信息必须加密存储
2. **权限管理**: 不同智能体有不同的访问权限
3. **存储限制**: 单个文件不超过10MB
4. **编码规范**: 统一使用UTF-8编码
5. **备份策略**: 建议定期备份整个记忆库

## 技术实现

详见开发文档: `sk-dev-doc.md`

---

**技能版本**: v1.0  
**最后更新**: 2026-03-05
