# Memory Bank Skill - 快速开始指南

## 📚 简介

Memory Bank是一个图书馆式记忆库技能，能够被智能体默认调用，自动管理记忆碎片的存储和索引。

## 🚀 快速开始

### 1. 安装Skill

Skill已经按照标准格式创建在项目中：

```
.trae/
└── skills/
    └── memory-bank/
        └── SKILL.md
```

### 2. 初始化记忆库

创建记忆库根目录和基础结构：

```bash
# 创建记忆库根目录
mkdir -p ~/memory_bank

# 创建基础分类目录
cd ~/memory_bank
mkdir -p 01-工作事业 02-生活日常 03-个人成长 04-社交关系 \
         05-财务管理 06-密码密钥 07-资源收藏 08-临时便签
```

### 3. 配置智能体

在智能体配置文件中添加Memory Bank配置：

```yaml
# agent_config.yaml
skills:
  memory_bank:
    enabled: true
    auto_invoke: true
    auto_store: true
    root_path: "~/memory_bank"
```

### 4. 使用示例

#### 存储记忆

**用户**: "记住我的OpenAI API密钥是sk-proj-xxxxx"

**智能体自动执行**:
- ✅ 识别为API密钥
- ✅ 自动分类到 `06-密码密钥/API密钥/`
- ✅ 自动加密存储
- ✅ 自动更新索引

#### 检索记忆

**用户**: "我的GitHub token是什么?"

**智能体自动执行**:
- ✅ 分析查询意图
- ✅ 检索密码库
- ✅ 返回结果

## 📖 核心功能

### 1. 自动分类存储

系统会自动识别内容类型并分类存储：

| 内容类型 | 自动分类 | 是否加密 |
|---------|---------|---------|
| API密钥 | 06-密码密钥/API密钥 | ✅ |
| 账号密码 | 06-密码密钥/账号密码 | ✅ |
| 项目信息 | 01-工作事业/项目管理 | ❌ |
| 健康信息 | 02-生活日常/健康管理 | ❌ |
| 个人偏好 | 03-个人成长 | ❌ |

### 2. 自动索引更新

每次存储、更新或删除记忆时，系统会自动更新对应的分类目录索引。

### 3. 智能检索

支持多种检索方式：
- 关键词搜索
- 标签筛选
- 时间范围查询
- 分类浏览

### 4. 安全加密

敏感信息自动使用AES-256加密存储。

## 🛠️ 开发指南

### 文件结构

```
记忆库/
├── 分类目录.md                    # 根目录索引
├── 01-工作事业/
│   ├── 分类目录.md                # 分类索引
│   └── 项目A.md                   # 内容文件
└── 06-密码密钥/
    ├── 分类目录.md
    └── API密钥/
        ├── 分类目录.md
        └── openai-api.md          # 加密文件
```

### API调用

```python
# 存储记忆
memory_bank.auto_store_memory(
    content="记忆内容",
    context={"user_message": "用户消息"}
)

# 检索记忆
results = memory_bank.auto_retrieve_memory(
    query="搜索关键词",
    agent_id="agent_001"
)

# 更新记忆
memory_bank.auto_update_memory(
    file_path="文件路径",
    new_content="新内容",
    agent_id="agent_001"
)

# 删除记忆
memory_bank.auto_delete_memory(
    file_path="文件路径",
    agent_id="agent_001"
)
```

## 📋 最佳实践

### 1. 记忆存储

- ✅ 及时存储重要信息
- ✅ 使用准确的描述
- ✅ 让系统自动分类

### 2. 检索优化

- ✅ 使用具体的关键词
- ✅ 结合时间范围
- ✅ 利用分类筛选

### 3. 安全管理

- ✅ 敏感信息自动加密
- ✅ 定期更新密钥
- ✅ 审查访问日志

### 4. 维护建议

- ✅ 定期备份记忆库
- ✅ 清理过期信息
- ✅ 重建索引优化性能

## 🔧 高级配置

### 自定义分类规则

```python
CUSTOM_CATEGORIES = {
    "custom_type": {
        "patterns": [r"自定义模式"],
        "category": "自定义分类",
        "encrypt": False,
        "tags": ["自定义标签"]
    }
}
```

### 索引优化

```yaml
index:
  auto_update: true
  cache_enabled: true
  cache_size: 1000
  update_interval: 300
```

### 加密配置

```yaml
security:
  encryption_algorithm: "AES-256"
  key_storage: "/secure/keys"
  auto_detect_sensitive: true
```

## 📚 相关文档

- [完整开发文档](./sk-dev-doc.md)
- [Skill定义文件](./.trae/skills/memory-bank/SKILL.md)
- [原始构想](./sk.md)

## ❓ 常见问题

### Q1: 如何查看所有存储的记忆?

**A**: 查看对应分类的 `分类目录.md` 文件，或使用检索功能搜索。

### Q2: 如何修改已存储的记忆?

**A**: 直接告诉智能体"更新xxx信息"，系统会自动处理。

### Q3: 如何删除记忆?

**A**: 告诉智能体"删除xxx"，系统会自动删除并更新索引。

### Q4: 记忆库存储在哪里?

**A**: 默认存储在 `~/memory_bank` 目录，可在配置文件中修改。

### Q5: 如何备份记忆库?

**A**: 直接复制整个记忆库目录即可，所有数据都是标准的Markdown文件。

## 🎯 下一步

1. ✅ 阅读完整开发文档
2. ✅ 根据需求自定义分类
3. ✅ 开始使用并积累记忆
4. ✅ 定期维护和优化

---

**版本**: v1.0  
**更新时间**: 2026-03-05
