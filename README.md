# Memory Bank - 图书馆式记忆库 Skill

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-orange.svg)](https://www.python.org)

> 一个基于文件系统的智能体记忆管理技能，采用图书馆索引式设计，支持自动分类存储、智能检索和安全加密。

## ✨ 核心特性

- 🗂️ **图书馆式索引** - 分级目录索引，快速定位信息
- 🤖 **自动调用** - 智能体默认调用，无需手动触发
- 📝 **纯文件存储** - 使用Markdown文件，简单直观
- 🔐 **安全加密** - AES-256加密敏感信息
- 🏷️ **智能分类** - 自动识别内容类型并分类存储
- 🔄 **自动索引** - 存储后自动更新分类目录索引
- 🔍 **多维检索** - 支持关键词、标签、时间范围检索
- 🌐 **跨平台** - 标准文件系统，支持多设备同步

## 📦 项目结构

```
shuizu/
├── .trae/
│   └── skills/
│       └── memory-bank/
│           └── SKILL.md              # Skill定义文件
├── sk.md                             # 原始构想文档
├── sk-dev-doc.md                     # 完整开发文档
├── QUICKSTART.md                     # 快速开始指南
└── README.md                         # 项目说明文档
```

## 🚀 快速开始

### 1. 安装

Skill已按照标准格式创建，无需额外安装步骤。

### 2. 初始化记忆库

```bash
# 创建记忆库根目录
mkdir -p ~/memory_bank

# 创建基础分类
cd ~/memory_bank
mkdir -p 01-工作事业 02-生活日常 03-个人成长 04-社交关系 \
         05-财务管理 06-密码密钥 07-资源收藏 08-临时便签
```

### 3. 配置智能体

```yaml
skills:
  memory_bank:
    enabled: true
    auto_invoke: true
    root_path: "~/memory_bank"
```

### 4. 开始使用

```
用户: "记住我的OpenAI API密钥是sk-xxxxx"
智能体: ✅ 已自动存储到密码库并加密

用户: "我的GitHub token是什么?"
智能体: ✅ 自动检索并返回结果
```

## 📚 记忆库结构

```
记忆库/
├── 分类目录.md                    # 根目录索引
│
├── 01-工作事业/                   # 工作相关记忆
│   ├── 分类目录.md
│   ├── 项目管理/
│   └── 技能提升/
│
├── 02-生活日常/                   # 生活相关记忆
│   ├── 分类目录.md
│   ├── 健康管理/
│   └── 家庭事务/
│
├── 03-个人成长/                   # 成长相关记忆
├── 04-社交关系/                   # 社交相关记忆
├── 05-财务管理/                   # 财务相关记忆
│
├── 06-密码密钥/                   # 🔐 密码密钥存储区
│   ├── 分类目录.md
│   ├── API密钥/                   # API密钥自动加密存储
│   ├── 账号密码/                  # 账号密码自动加密存储
│   └── 证书密钥/                  # 证书密钥自动加密存储
│
├── 07-资源收藏/                   # 资源收藏
└── 08-临时便签/                   # 临时信息
```

## 🎯 核心功能

### 1. 自动记忆存储

智能体识别到重要信息时自动存储：

```python
# 用户: "记住我的OpenAI API密钥是sk-xxxxx"
# 系统自动执行:
{
    "type": "api_key",
    "category": "06-密码密钥/API密钥",
    "encrypted": true,
    "file": "openai-api.md",
    "index_updated": true
}
```

### 2. 智能检索

支持多种检索方式：

```python
# 关键词检索
results = memory_bank.search("OpenAI API")

# 标签检索
results = memory_bank.search_by_tag("API")

# 时间范围检索
results = memory_bank.search_by_time(
    start="2026-01-01",
    end="2026-03-05"
)
```

### 3. 自动索引更新

每次操作后自动更新索引：

```markdown
# 06-密码密钥 - 分类目录

## 📄 文件索引
| 文件名 | 简介 | 标签 | 更新时间 |
|--------|------|------|----------|
| openai-api.md | OpenAI API密钥 | #API #密钥 | 2026-03-05 |
```

### 4. 安全加密

敏感信息自动加密：

- API密钥 → AES-256加密
- 账号密码 → AES-256加密
- 证书密钥 → AES-256加密

## 📖 使用示例

### 场景1: 存储API密钥

```
用户: 记住我的OpenAI API密钥是sk-proj-xxxxx，用于GPT-4访问

智能体:
✅ 已识别为API密钥
✅ 自动分类到: 06-密码密钥/API密钥/
✅ 已加密存储
✅ 已更新索引
```

### 场景2: 检索项目信息

```
用户: 我上周的项目会议记录在哪?

智能体:
✅ 分析查询意图
✅ 检索分类目录
✅ 找到匹配文件: 01-工作事业/项目管理/项目A会议记录.md
✅ 返回相关内容
```

### 场景3: 更新记忆

```
用户: 更新我的项目进度，已完成80%

智能体:
✅ 找到对应文件
✅ 更新内容
✅ 同步索引
```

## 🔧 高级配置

### 自定义分类规则

```python
CUSTOM_PATTERNS = {
    "custom_type": {
        "patterns": [r"自定义关键词"],
        "category": "自定义分类",
        "encrypt": False,
        "tags": ["自定义标签"]
    }
}
```

### 性能优化

```yaml
performance:
  cache_enabled: true
  cache_size: 1000
  index_update_interval: 300
  max_file_size: 10485760  # 10MB
```

### 安全配置

```yaml
security:
  encryption_algorithm: "AES-256"
  key_storage: "/secure/keys"
  auto_detect_sensitive: true
  access_log_enabled: true
```

## 📋 API文档

### 存储记忆

```python
memory_bank.auto_store_memory(
    content="记忆内容",
    context={"user_message": "上下文"}
)
```

### 检索记忆

```python
results = memory_bank.auto_retrieve_memory(
    query="搜索关键词",
    agent_id="agent_001"
)
```

### 更新记忆

```python
memory_bank.auto_update_memory(
    file_path="文件路径",
    new_content="新内容",
    agent_id="agent_001"
)
```

### 删除记忆

```python
memory_bank.auto_delete_memory(
    file_path="文件路径",
    agent_id="agent_001"
)
```

## 🛠️ 开发指南

### 环境要求

- Python 3.8+
- 文件系统支持UTF-8编码

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行测试

```bash
pytest tests/ -v --cov=memory_bank
```

### 构建文档

```bash
mkdocs serve
```

## 📚 文档资源

- [完整开发文档](./sk-dev-doc.md) - 详细的技术开发文档
- [快速开始指南](./QUICKSTART.md) - 快速上手指南
- [原始构想](./sk.md) - 项目原始构想文档
- [Skill定义](./.trae/skills/memory-bank/SKILL.md) - Skill标准定义文件

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0 (2026-03-05)
- ✅ 初始版本发布
- ✅ 实现自动记忆存储
- ✅ 实现智能检索
- ✅ 实现自动索引更新
- ✅ 实现安全加密
- ✅ 创建标准Skill结构

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

感谢所有贡献者和用户的支持！

## 📮 联系方式

- 项目主页: [GitHub Repository]
- 问题反馈: [GitHub Issues]
- 邮箱: [your-email@example.com]

---

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**
