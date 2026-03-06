#!/usr/bin/env python3
"""
Memory Bank 便捷使用脚本（带操作记录）

这是长期使用的主入口脚本。
"""

import sys
import os
import argparse

# 添加模块路径
memory_dir = os.path.join(os.path.dirname(__file__), "memory")
sys.path.insert(0, memory_dir)

from memory_bank_with_logging import get_memory_bank


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Memory Bank - 图书馆式记忆库（带操作记录）")
    subparsers = parser.add_subparsers(title="命令", dest="command")

    # 存储命令
    store_parser = subparsers.add_parser("store", help="存储记忆")
    store_parser.add_argument("content", help="记忆内容")

    # 搜索命令
    search_parser = subparsers.add_parser("search", help="搜索记忆")
    search_parser.add_argument("query", help="搜索关键词")

    # 标签搜索
    tag_parser = subparsers.add_parser("tag", help="按标签搜索")
    tag_parser.add_argument("tag", help="标签名")

    # 列出命令
    list_parser = subparsers.add_parser("list", help="列出目录")
    list_parser.add_argument("directory", nargs="?", default="", help="目录路径")

    # 读取命令
    read_parser = subparsers.add_parser("read", help="读取文件")
    read_parser.add_argument("file", help="文件路径")

    # 统计命令
    subparsers.add_parser("stats", help="显示统计")

    # 重建索引命令
    subparsers.add_parser("reindex", help="重建索引")

    args = parser.parse_args()

    mb = get_memory_bank()

    if args.command == "store":
        result = mb.auto_store_memory(args.content)
        if result.get('success'):
            print(f"✓ 记忆已存储")
            print(f"  路径: {result.get('file_path')}")
            print(f"  分类: {result.get('category')}")
        else:
            print("✗ 存储失败")

    elif args.command == "search":
        results = mb.auto_retrieve_memory(args.query)
        print(f"搜索 '{args.query}':")
        if not results:
            print("  未找到结果")
        else:
            print(f"\n找到 {len(results)} 个结果:\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r.get('filename', '未知')}")
                print(f"   路径: {r.get('path', '')}")
                print(f"   摘要: {r.get('summary', '')}")
                print()

    elif args.command == "tag":
        results = mb.search_by_tag(args.tag)
        print(f"按标签 '#{args.tag}' 搜索:")
        if not results:
            print("  未找到结果")
        else:
            print(f"\n找到 {len(results)} 个结果:\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r.get('filename', '未知')}")
                print(f"   路径: {r.get('path', '')}")
                print()

    elif args.command == "list":
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

    elif args.command == "read":
        file_data = mb.read_file(args.file)
        if file_data:
            print(f"文件: {args.file}")
            print("=" * 60)
            print(file_data['content'])
        else:
            print(f"✗ 文件不存在: {args.file}")

    elif args.command == "stats":
        stats = mb.get_statistics()
        print("记忆库统计信息")
        print("=" * 30)
        print(f"总文件数: {stats['total_files']}")
        print(f"总目录数: {stats['total_directories']}")
        print("\n分类:")
        for cat in stats['categories']:
            print(f"  - {cat}")

    elif args.command == "reindex":
        print("重建索引中...")
        success = mb.rebuild_index()
        if success:
            print("✓ 索引重建完成")
        else:
            print("✗ 索引重建失败")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
