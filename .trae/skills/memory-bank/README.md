# Memory Bank - 图书馆式记忆库

一个基于文件系统的智能体记忆管理技能，采用图书馆索引式设计，使用Markdown文件存储记忆内容。

## 功能特性

- ✅ **纯文件存储**: 使用Markdown文件，无复杂数据库依赖
- ✅ **图书馆式索引**: 分级目录索引，快速定位信息
- ✅ **自动分类存储**: 智能识别内容类型，自动分类存储
- ✅ **快速检索**: 支持关键词搜索、标签筛选
- ✅ **安全加密**: 敏感信息加密存储
- ✅ **权限管理**: 基于角色的访问控制

## 目录结构

```
记忆库/
├── 分类目录.md                          # 根目录索引
├── 01-工作事业/
│   ├── 分类目录.md
│   ├── 项目管理/
│   └── 技能提升/
├── 02-生活日常/
│   ├── 分类目录.md
│   ├── 健康管理/
│   └── 家庭事务/
├── 03-个人成长/
│   ├── 分类目录.md
│   ├── 阅读笔记/
│   └── 学习计划/
├── 04-社交关系/
├── 05-财务管理/
├── 06-密码密钥/                         # 专用密码存储区
│   ├── API密钥/
│   ├── 账号密码/
│   └── 证书密钥/
├── 07-资源收藏/
└── 08-临时便签/
```

## 快速开始

### 1. 初始化记忆库

使用Python模块:

```python
from memory_bank import MemoryBankSkill

# 初始化记忆库
mb = MemoryBankSkill("/path/to/memory_bank", "agent_001")
```

或使用命令行:

```bash
cd .trae/skills/memory-bank
python -m memory_bank.cli init
```

### 2. 存储记忆

```python
# 自动存储（会自动识别内容类型）
result = mb.auto_store_memory("记住我的OpenAI API密钥是sk-proj-xxxxx")
print(result['file_path'])  # 06-密码密钥/API密钥/OpenAI_API密钥.md
```

命令行:

```bash
python -m memory_bank.cli store "记住我的API密钥是sk-xxx"
```

### 3. 检索记忆

```python
# 自动检索
results = mb.auto_retrieve_memory("我的OpenAI API密钥")
for result in results:
    print(f"找到: {result['filename']}")
    print(f"路径: {result['path']}")
```

命令行:

```bash
python -m memory_bank.cli search "API密钥"
```

### 4. 更多操作

```python
# 列出目录
content = mb.list_directory("01-工作事业")

# 读取文件
file_data = mb.read_file("01-工作事业/项目管理/项目A.md")

# 按标签搜索
results = mb.search_by_tag("API")

# 重建索引
mb.rebuild_index()

# 获取统计信息
stats = mb.get_statistics()
```

## 命令行工具

完整的命令行工具使用:

```bash
# 初始化
python -m memory_bank.cli init

# 存储记忆
python -m memory_bank.cli store "记忆内容"

# 搜索记忆
python -m memory_bank.cli search "关键词"
python -m memory_bank.cli search --tag "API"

# 列出目录
python -m memory_bank.cli list
python -m memory_bank.cli list "01-工作事业"

# 读取文件
python -m memory_bank.cli read "01-工作事业/项目管理/项目A.md"

# 显示统计
python -m memory_bank.cli stats

# 重建索引
python -m memory_bank.cli reindex
```

## 运行示例

```bash
cd .trae/skills/memory-bank
python examples/demo.py
```

## 自动识别的内容类型

系统会自动识别以下类型的内容并分类存储:

| 类型 | 关键词 | 存储位置 | 是否加密 |
|------|--------|----------|----------|
| API密钥 | api_key, token, secret, 密钥 | 06-密码密钥/API密钥 | 是 |
| 密码 | 密码, password, pwd | 06-密码密钥/账号密码 | 是 |
| 项目 | 项目, project, 任务, task | 01-工作事业/项目管理 | 否 |
| 会议 | 会议, meeting, 讨论 | 01-工作事业/项目管理 | 否 |
| 健康 | 健康, 体检, 运动 | 02-生活日常/健康管理 | 否 |
| 偏好 | 喜欢, 偏好, prefer, 习惯 | 03-个人成长 | 否 |

## 文件格式

### 分类目录.md

每个目录都有一个分类目录.md文件，包含该目录下的文件索引:

```markdown
# [目录名] - 分类目录

## 📂 子目录列表
| 目录名 | 说明 | 包含文件数 | 创建时间 |
|--------|------|-----------|----------|

## 📄 文件索引
| 文件名 | 简介 | 标签 | 重要程度 | 更新时间 |
|--------|------|------|----------|----------|

## 📊 统计信息
- 总文件数: X
- 总目录数: Y
- 最后更新: YYYY-MM-DD HH:mm:ss
```

### 内容文件

普通内容文件格式:

```markdown
# 文件标题

## 📌 基本信息
- **创建时间**: YYYY-MM-DD
- **最后更新**: YYYY-MM-DD HH:mm:ss
- **标签**: #标签1 #标签2
- **重要程度**: ⭐⭐⭐
- **访问权限**: public/private/encrypted
- **版本**: v1.0

## 📝 核心内容
[主要内容]

## 📊 更新历史
| 日期 | 版本 | 更新内容 | 更新人 |
|------|------|----------|--------|
```

### 密码文件

密码/密钥文件格式:

```markdown
# 密钥名称

## 🔐 安全信息
- **加密级别**: high
- **授权智能体**: [智能体列表]
- **最后使用**: YYYY-MM-DD
- **有效期至**: 长期有效

## 🔑 密钥内容
```
[密钥内容]
```

## 📋 使用记录
| 时间 | 智能体ID | 用途 | 结果 |
|------|----------|------|------|
```

## 技能集成

该Skill可以被智能体自动调用。当智能体需要存储或检索记忆时，会自动触发。

### 自动调用场景

- **存储记忆**: 当用户说"记住..."、"保存..."时
- **检索记忆**: 当用户问"我的...在哪？"、"之前..."时
- **更新记忆**: 当用户说"更新..."、"修改..."时
- **删除记忆**: 当用户说"删除..."、"忘记..."时

## 开发说明

### 模块结构

```
memory_bank/
├── __init__.py          # 模块入口
├── memory_bank.py       # 主类 MemoryBankSkill
├── file_manager.py      # 文件管理器
├── index_manager.py     # 索引管理器
├── permission_manager.py # 权限管理器
├── encryption_service.py # 加密服务
└── cli.py               # 命令行工具
```

### 扩展功能

继承 MemoryBankSkill 类来添加自定义功能:

```python
from memory_bank import MemoryBankSkill

class MyMemoryBank(MemoryBankSkill):
    def custom_search(self, params):
        # 自定义搜索逻辑
        pass
```

## 注意事项

1. **隐私保护**: 敏感信息会自动加密存储
2. **备份建议**: 定期备份整个记忆库目录
3. **文件编码**: 统一使用UTF-8编码
4. **文件大小**: 单个文件建议不超过10MB

## 许可证

本项目仅供学习和研究使用。
