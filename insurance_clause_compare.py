#!/usr/bin/env python3
"""保险合同条款对比工具。

功能：
1. 按“条款编号 + 内容”解析两份合同文本；
2. 输出新增、删除、修改的条款；
3. 对修改条款给出行内差异。

用法：
    python insurance_clause_compare.py old.txt new.txt
"""

from __future__ import annotations

import argparse
import difflib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

# 常见条款标题形式：
# 第1条 ...
# 一、...
# 1. ...
CLAUSE_HEADER = re.compile(
    r"^\s*(?:第\s*[一二三四五六七八九十百千\d]+\s*条|[一二三四五六七八九十]+[、.]|\d+[、.])\s*"
)


@dataclass
class Clause:
    title: str
    content: str


def normalize_text(text: str) -> str:
    """统一换行与空白，便于比较。"""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    return "\n".join(lines).strip()


def parse_clauses(text: str) -> Dict[str, Clause]:
    """从合同文本中抽取条款。

    如果无法识别任何条款标题，则将全文作为一个“总则”。
    """
    lines = normalize_text(text).split("\n")
    clauses: Dict[str, Clause] = {}

    current_title: str | None = None
    current_lines: List[str] = []

    def flush() -> None:
        nonlocal current_title, current_lines
        if current_title is not None:
            content = "\n".join(current_lines).strip()
            clauses[current_title] = Clause(title=current_title, content=content)

    for line in lines:
        if CLAUSE_HEADER.match(line):
            flush()
            current_title = line.strip()
            current_lines = []
        else:
            if current_title is None and line.strip() == "":
                continue
            if current_title is None:
                current_title = "总则"
            current_lines.append(line)

    flush()
    return clauses


def make_inline_diff(old: str, new: str) -> str:
    """生成行级 unified diff。"""
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile="旧条款",
        tofile="新条款",
        lineterm="",
    )
    return "\n".join(diff)


def compare_contracts(old_text: str, new_text: str) -> str:
    old_clauses = parse_clauses(old_text)
    new_clauses = parse_clauses(new_text)

    old_keys = set(old_clauses.keys())
    new_keys = set(new_clauses.keys())

    added = sorted(new_keys - old_keys)
    removed = sorted(old_keys - new_keys)
    common = sorted(old_keys & new_keys)

    changed = [
        key
        for key in common
        if old_clauses[key].content.strip() != new_clauses[key].content.strip()
    ]

    output: List[str] = []
    output.append("=== 保险合同条款对比结果 ===")

    output.append("\n[新增条款]")
    if added:
        for key in added:
            output.append(f"- {key}")
    else:
        output.append("- 无")

    output.append("\n[删除条款]")
    if removed:
        for key in removed:
            output.append(f"- {key}")
    else:
        output.append("- 无")

    output.append("\n[修改条款]")
    if changed:
        for key in changed:
            output.append(f"\n--- {key} ---")
            output.append(make_inline_diff(old_clauses[key].content, new_clauses[key].content))
    else:
        output.append("- 无")

    return "\n".join(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="保险合同条款对比工具")
    parser.add_argument("old_file", type=Path, help="旧版合同文本文件路径")
    parser.add_argument("new_file", type=Path, help="新版合同文本文件路径")
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="输出文件路径（默认打印到控制台）"
    )
    args = parser.parse_args()

    old_text = args.old_file.read_text(encoding="utf-8")
    new_text = args.new_file.read_text(encoding="utf-8")

    result = compare_contracts(old_text, new_text)

    if args.output:
        args.output.write_text(result, encoding="utf-8")
        print(f"对比完成，结果已写入: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
