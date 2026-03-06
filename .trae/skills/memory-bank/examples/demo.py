#!/usr/bin/env python3
"""
Memory Bank 使用示例

演示如何使用图书馆式记忆库。
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_bank import MemoryBankSkill


def main():
    """主示例函数"""
    print("=" * 60)
    print("Memory Bank - 图书馆式记忆库 示例")
    print("=" * 60)

    # 初始化记忆库
    memory_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "记忆库")
    print(f"\n1. 初始化记忆库于: {memory_path}")
    mb = MemoryBankSkill(memory_path, "agent_demo")
    print("   ✓ 初始化完成\n")

    # 示例1: 存储API密钥
    print("2. 存储API密钥")
    print("-" * 40)
    result = mb.auto_store_memory("""
# OpenAI API密钥

这是我的OpenAI API密钥，用于访问GPT-4模型。
密钥: sk-proj-xxxxx-xxxxx-xxxxx-xxxxx-xxxxx
    """.strip())
    print(f"   结果: {'成功' if result['success'] else '失败'}")
    print(f"   路径: {result['file_path']}")
    print(f"   分类: {result['category']}")
    print()

    # 示例2: 存储项目信息
    print("3. 存储项目信息")
    print("-" * 40)
    result = mb.auto_store_memory("""
# 智能助手项目 - 会议记录

## 会议时间
2026-03-05 14:00-15:30

## 参会人员
- 张三
- 李四
- 王五

## 会议内容
1. 讨论了项目进度
2. 确定了下周目标
3. 分配了任务

## 下周任务
- [ ] 完成UI设计
- [ ] 开发后端API
- [ ] 编写测试用例
    """.strip())
    print(f"   结果: {'成功' if result['success'] else '失败'}")
    print(f"   路径: {result['file_path']}")
    print()

    # 示例3: 存储偏好信息
    print("4. 存储个人偏好")
    print("-" * 40)
    result = mb.auto_store_memory("""
# 个人偏好设置

## 编程语言偏好
- 首选: Python
- 次选: TypeScript
- 不喜欢: PHP

## 工具偏好
- 编辑器: VS Code
- 终端: iTerm2
- Git客户端: GitHub Desktop

## 工作习惯
- 喜欢在上午写代码
- 下午进行会议和讨论
- 晚上阅读和学习
    """.strip())
    print(f"   结果: {'成功' if result['success'] else '失败'}")
    print()

    # 示例4: 搜索记忆
    print("5. 搜索记忆 - 'API'")
    print("-" * 40)
    results = mb.auto_retrieve_memory("API")
    print(f"   找到 {len(results)} 个结果:")
    for r in results:
        print(f"   - {r.get('filename')}: {r.get('summary', '')[:40]}...")
    print()

    # 示例6: 列出目录
    print("6. 列出根目录内容")
    print("-" * 40)
    content = mb.list_directory("")
    print("   子目录:")
    for d in content['directories']:
        print(f"   - {d}/")
    print()

    # 示例7: 显示统计信息
    print("7. 统计信息")
    print("-" * 40)
    stats = mb.get_statistics()
    print(f"   总文件数: {stats['total_files']}")
    print(f"   总目录数: {stats['total_directories']}")
    print()

    print("=" * 60)
    print("示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
