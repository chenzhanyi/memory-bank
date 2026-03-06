#!/usr/bin/env python3
"""
Memory Bank - 图书馆式记忆库 便捷使用脚本

在项目根目录直接使用此脚本操作记忆库。
"""

import sys
import os

# 添加 Skill 路径
skill_path = os.path.join(os.path.dirname(__file__), ".trae", "skills", "memory-bank")
sys.path.insert(0, skill_path)

from memory_bank import MemoryBankSkill


def get_memory_bank():
    """获取记忆库实例"""
    memory_path = os.path.join(os.path.dirname(__file__), "记忆库")
    return MemoryBankSkill(memory_path, "agent_001")


def store_memory(content: str):
    """存储记忆"""
    mb = get_memory_bank()
    result = mb.auto_store_memory(content)
    if result['success']:
        print(f"✓ 记忆已存储")
        print(f"  路径: {result['file_path']}")
        print(f"  分类: {result['category']}")
    else:
        print("✗ 存储失败")
    return result


def search_memory(query: str):
    """搜索记忆"""
    mb = get_memory_bank()
    results = mb.auto_retrieve_memory(query)
    print(f"搜索 '{query}':")
    if not results:
        print("  未找到结果")
        return []
    print(f"\n找到 {len(results)} 个结果:\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.get('filename', '未知')}")
        print(f"   路径: {result.get('path', '')}")
        print(f"   摘要: {result.get('summary', '')}")
        print()
    return results


def list_dir(path: str = ""):
    """列出目录"""
    mb = get_memory_bank()
    content = mb.list_directory(path)
    print(f"目录: {path or '根目录'}\n")
    if content['directories']:
        print("📂 子目录:")
        for d in content['directories']:
            print(f"  - {d}/")
        print()
    if content['files']:
        print("📄 文件:")
        for f in content['files']:
            print(f"  - {f}")
        print()
    return content


def read_file(file_path: str):
    """读取文件"""
    mb = get_memory_bank()
    file_data = mb.read_file(file_path)
    if file_data:
        print(f"文件: {file_path}")
        print("=" * 60)
        print(file_data['content'])
    else:
        print(f"✗ 文件不存在: {file_path}")
    return file_data


def show_stats():
    """显示统计"""
    mb = get_memory_bank()
    stats = mb.get_statistics()
    print("记忆库统计信息")
    print("=" * 30)
    print(f"总文件数: {stats['total_files']}")
    print(f"总目录数: {stats['total_directories']}")
    print("\n分类:")
    for cat in stats['categories']:
        print(f"  - {cat}")
    return stats


def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description="Memory Bank - 图书馆式记忆库")
    subparsers = parser.add_subparsers(title="命令", dest="command")

    # 存储命令
    store_parser = subparsers.add_parser("store", help="存储记忆")
    store_parser.add_argument("content", help="记忆内容")

    # 搜索命令
    search_parser = subparsers.add_parser("search", help="搜索记忆")
    search_parser.add_argument("query", help="搜索关键词")

    # 列出命令
    list_parser = subparsers.add_parser("list", help="列出目录")
    list_parser.add_argument("directory", nargs="?", default="", help="目录路径")

    # 读取命令
    read_parser = subparsers.add_parser("read", help="读取文件")
    read_parser.add_argument("file", help="文件路径")

    # 统计命令
    subparsers.add_parser("stats", help="显示统计")

    args = parser.parse_args()

    if args.command == "store":
        store_memory(args.content)
    elif args.command == "search":
        search_memory(args.query)
    elif args.command == "list":
        list_dir(args.directory)
    elif args.command == "read":
        read_file(args.file)
    elif args.command == "stats":
        show_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
