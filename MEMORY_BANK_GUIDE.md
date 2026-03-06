# Memory Bank 快速上手指南

## 🎉 已完成！

图书馆式记忆库 Skill 已经成功实现并初始化！

---

## 📁 项目结构

```
shuizu/
├── 记忆库/                           # ✅ 已创建的记忆库目录
│   ├── 分类目录.md
│   ├── 01-工作事业/
│   ├── 02-生活日常/
│   ├── 03-个人成长/
│   ├── 04-社交关系/
│   ├── 05-财务管理/
│   ├── 06-密码密钥/
│   ├── 07-资源收藏/
│   └── 08-临时便签/
│
├── .trae/skills/memory-bank/         # ✅ Skill 实现
│   ├── SKILL.md                      # Skill 定义
│   ├── README.md                     # 详细文档
│   ├── memory_bank/                  # 核心模块
│   │   ├── __init__.py
│   │   ├── memory_bank.py            # 主类
│   │   ├── file_manager.py           # 文件管理
│   │   ├── index_manager.py          # 索引管理
│   │   ├── permission_manager.py     # 权限管理
│   │   ├── encryption_service.py     # 加密服务
│   │   └── cli.py                    # 命令行工具
│   └── examples/
│       └── demo.py                   # 示例代码
│
├── memory_bank_demo.py               # ✅ 便捷使用脚本
├── sk.md                             # 原始需求
└── sk-dev-doc.md                     # 开发文档
```

---

## 🚀 快速开始

### 方法1: 使用便捷脚本（推荐）

在项目根目录直接使用：

```bash
# 显示统计信息
python3 memory_bank_demo.py stats

# 存储记忆
python3 memory_bank_demo.py store "记住我的GitHub token是ghp_xxxxx"

# 搜索记忆
python3 memory_bank_demo.py search "API密钥"

# 列出目录
python3 memory_bank_demo.py list
python3 memory_bank_demo.py list "01-工作事业"

# 读取文件
python3 memory_bank_demo.py read "06-密码密钥/API密钥/OpenAI API密钥.md"
```

### 方法2: 在 Python 代码中使用

```python
from memory_bank import MemoryBankSkill

# 初始化
mb = MemoryBankSkill("/path/to/shuizu/记忆库", "agent_001")

# 存储记忆
result = mb.auto_store_memory("记住我的API密钥是sk-xxxxx")
print(result['file_path'])

# 检索记忆
results = mb.auto_retrieve_memory("我的API密钥")
for r in results:
    print(r['filename'])

# 列出目录
content = mb.list_directory("01-工作事业")

# 读取文件
file_data = mb.read_file("06-密码密钥/API密钥/OpenAI API密钥.md")
print(file_data['content'])
```

### 方法3: 使用 Skill 自带的 CLI

```bash
cd .trae/skills/memory-bank

# 初始化
python3 -m memory_bank.cli init

# 存储
python3 -m memory_bank.cli store "记忆内容"

# 搜索
python3 -m memory_bank.cli search "关键词"

# 查看所有命令
python3 -m memory_bank.cli --help
```

---

## 📋 核心功能

### ✅ 自动分类存储

系统会自动识别内容类型并存储到正确位置：

| 内容类型 | 关键词 | 存储位置 |
|---------|--------|---------|
| API密钥 | `api_key`, `token`, `secret`, `密钥` | `06-密码密钥/API密钥/` |
| 密码 | `密码`, `password`, `pwd` | `06-密码密钥/账号密码/` |
| 项目 | `项目`, `project`, `任务` | `01-工作事业/项目管理/` |
| 会议 | `会议`, `meeting`, `讨论` | `01-工作事业/项目管理/` |
| 健康 | `健康`, `体检`, `运动` | `02-生活日常/健康管理/` |
| 偏好 | `喜欢`, `偏好`, `习惯` | `03-个人成长/` |

### ✅ 图书馆式索引

每个目录都有 `分类目录.md`，包含：
- 子目录列表
- 文件索引表（文件名、简介、标签、重要程度、更新时间）
- 统计信息

### ✅ 快速检索

- 关键词搜索：`mb.auto_retrieve_memory("搜索词")`
- 标签搜索：`mb.search_by_tag("API")`
- 分类浏览：`mb.list_directory("目录名")`

### ✅ 安全机制

- 权限管理（RBAC）
- 敏感信息加密
- 访问日志记录

---

## 🎯 使用示例

### 示例1: 存储 API 密钥

```python
result = mb.auto_store_memory("""
# OpenAI API 密钥

密钥: sk-proj-abcdef123456
用途: GPT-4 访问
""")

# 自动存储到: 06-密码密钥/API密钥/OpenAI_API密钥.md
# 自动更新索引: 06-密码密钥/API密钥/分类目录.md
```

### 示例2: 存储会议记录

```python
result = mb.auto_store_memory("""
# 项目会议记录 - 2026-03-05

## 参会人员
- 张三
- 李四

## 讨论内容
1. 项目进度
2. 下周计划
""")

# 自动存储到: 01-工作事业/项目管理/项目会议记录_-_2026-03-05.md
```

### 示例3: 搜索记忆

```python
# 搜索所有包含 "API" 的内容
results = mb.auto_retrieve_memory("API")

for r in results:
    print(f"找到: {r['filename']}")
    print(f"路径: {r['path']}")
    print(f"摘要: {r['summary']}")
```

---

## 📊 当前状态

运行 `python3 memory_bank_demo.py stats` 查看：

```
记忆库统计信息
==============================
总文件数: 3
总目录数: 17
```

已有的示例文件：
- `06-密码密钥/API密钥/OpenAI API密钥.md`
- `01-工作事业/项目管理/智能助手项目 - 会议记录.md`
- `01-工作事业/项目管理/个人偏好设置.md`

---

## 📚 更多文档

- **详细文档**: `.trae/skills/memory-bank/README.md`
- **Skill 定义**: `.trae/skills/memory-bank/SKILL.md`
- **开发文档**: `sk-dev-doc.md`
- **原始需求**: `sk.md`

---

## 💡 提示

1. **记忆库位置**: 所有数据存储在 `./记忆库/` 目录
2. **备份建议**: 定期备份整个 `./记忆库/` 目录
3. **文件格式**: 所有文件都是 Markdown 格式，可直接编辑
4. **索引自动更新**: 创建/修改/删除文件后会自动更新分类目录

---

## 🎊 恭喜！

你现在拥有了一个功能完整的图书馆式记忆库！开始使用吧！
