#!/usr/bin/env python3
"""
Memory Bank 命令行接口

提供便捷的命令行工具来操作记忆库。
"""

import sys
import os
import argparse
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_bank import MemoryBankSkill


def get_default_memory_path():
    """获取默认记忆库路径"""
    # 在项目根目录下创建记忆库
    current_dir = Path(__file__).parent.parent.parent.parent.parent
    return str(current_dir / "记忆库")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Memory Bank - 图书馆式记忆库")
    subparsers = parser.add_subparsers(title="命令", dest="command")

    # 存储命令
    store_parser = subparsers.add_parser("store", help="存储记忆")
    store_parser.add_argument("content", help="记忆内容")
    store_parser.add_argument("--path", "-p", help="记忆库路径", default=get_default_memory_path())
    store_parser.add_argument("--agent", "-a", help="智能体ID", default="agent_default")

    # 检索命令
    search_parser = subparsers.add_parser("search", help="检索记忆")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("--path", "-p", help="记忆库路径", default=get_default_memory_path())
    search_parser.add_argument("--agent", "-a", help="智能体ID", default="agent_default")
    search_parser.add_argument("--tag", "-t", help="按标签搜索")

    # 列出命令
    list_parser = subparsers.add_parser("list", help="列出目录内容")
    list_parser.add_argument("directory", nargs="?", default="", help="目录路径")
    list_parser.add_argument("--path", "-p", help="记忆库路径", default=get_default_memory_path())

    # 读取命令
    read_parser = subparsers.add_parser("read", help="读取文件")
    read_parser.add_argument("file", help="文件路径")
    read_parser.add_argument("--path", "-p", help="记忆库路径", default=get_default_memory_path())
    read_parser.add_argument("--agent", "-a", help="智能体ID", default="agent_default")

    # 统计命令
    stats_parser = subparsers.add_parser("stats", help="显示统计信息")
    stats_parser.add_argument("--path", "-p", help="记忆库路径", default=get_default_memory_path())

    # 重建索引命令
    reindex_parser = subparsers.add_parser("reindex", help="重建索引")
    reindex_parser.add_argument("--path", "-p", help="记忆库路径", default=get_default_memory_path())

    # 初始化命令
    init_parser = subparsers.add_parser("init", help="初始化记忆库")
    init_parser.add_argument("--path", "-p", help="记忆库路径", default=get_default_memory_path())

    args = parser.parse_args()

    if args.command == "init":
        print(f"初始化记忆库于: {args.path}")
        mb = MemoryBankSkill(args.path)
        print("✓ 记忆库初始化完成！")
        return

    if args.command == "store":
        mb = MemoryBankSkill(args.path, args.agent)
        result = mb.auto_store_memory(args.content)
        if result['success']:
            print(f"✓ 记忆已存储")
            print(f"  路径: {result['file_path']}")
            print(f"  分类: {result['category']}")
            if result['encrypted']:
                print(f"  加密: 是")
        else:
            print("✗ 存储失败")
        return

    if args.command == "search":
        mb = MemoryBankSkill(args.path, args.agent)
        if args.tag:
            results = mb.search_by_tag(args.tag)
            print(f"按标签 '#{args.tag}' 搜索:")
        else:
            results = mb.auto_retrieve_memory(args.query)
            print(f"搜索 '{args.query}':")

        if not results:
            print("  未找到结果")
            return

        print(f"\n找到 {len(results)} 个结果:\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.get('filename', '未知')}")
            print(f"   路径: {result.get('path', '')}")
            print(f"   摘要: {result.get('summary', '')[:50]}...")
            print()
        return

    if args.command == "list":
        mb = MemoryBankSkill(args.path)
        content = mb.list_directory(args.directory)
        print(f"目录: {args.directory or '根目录'}\n")

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

        if not content['directories'] and not content['files']:
            print("  (空目录)")
        return

    if args.command == "read":
        mb = MemoryBankSkill(args.path, args.agent)
        file_data = mb.read_file(args.file, args.agent)
        if file_data:
            print(f"文件: {args.file}")
            print("=" * 60)
            print(file_data['content'])
        else:
            print(f"✗ 文件不存在: {args.file}")
        return

    if args.command == "stats":
        mb = MemoryBankSkill(args.path)
        stats = mb.get_statistics()
        print("记忆库统计信息")
        print("=" * 30)
        print(f"总文件数: {stats['total_files']}")
        print(f"总目录数: {stats['total_directories']}")
        print("\n分类:")
        for cat in stats['categories']:
            print(f"  - {cat}")
        return

    if args.command == "reindex":
        print("重建索引中...")
        mb = MemoryBankSkill(args.path)
        success = mb.rebuild_index()
        if success:
            print("✓ 索引重建完成")
        else:
            print("✗ 索引重建失败")
        return

    # 默认显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
