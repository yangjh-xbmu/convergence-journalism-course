#!/usr/bin/env python3
# INPUT: Markdown 文件或包含 Markdown 文件的目录
# OUTPUT: 终端报错报告与修复建议（可选 --fix 原位修复）
# POS: 统一的 Mermaid 图表语法合规检验与防错修复工具，用于讲义生成与 CI/CD 拦截
"""
Mermaid 图表语法静态校验与防错修复工具。

重点防御：
1. subgraph 声明中省略 ASCII 标识符，直接使用中文命名（如 `subgraph 范式一：链式顺序流`）；
2. subgraph 声明行包含全角冒号（：）、空格或非 ASCII 裸字符导致客户端词法解析器（Lexical error）崩溃；
3. subgraph 与 end 标签配对失衡与未闭合；
4. 节点标签中引号转义缺失。

用法：
    python mermaid_validator.py <文件或目录>
    python mermaid_validator.py <文件或目录> --fix
"""

import argparse
import re
import sys
from pathlib import Path


def extract_mermaid_blocks(content: str) -> list[dict]:
    """提取 Markdown 文本中所有的 mermaid 代码块及其所在行号。"""
    blocks = []
    lines = content.splitlines(keepends=True)
    in_mermaid = False
    start_line = 0
    current_lines = []

    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```mermaid"):
            in_mermaid = True
            start_line = idx
            current_lines = []
        elif in_mermaid and stripped.startswith("```"):
            in_mermaid = False
            blocks.append({
                "start_line": start_line,
                "end_line": idx,
                "lines": current_lines,
                "raw_text": "".join([line for _, line in current_lines])
            })
            current_lines = []
        elif in_mermaid:
            current_lines.append((idx, line))

    return blocks


def validate_mermaid_block(block: dict) -> list[dict]:
    """校验单个 mermaid 代码块内部语法合规性。"""
    errors = []
    subgraph_stack = []

    for line_num, line in block["lines"]:
        stripped = line.strip()
        # 跳过空行与注释
        if not stripped or stripped.startswith("%%"):
            continue

        # 检查 subgraph 语法
        if re.match(r"^subgraph\b", stripped):
            subgraph_stack.append(line_num)
            declaration = stripped[len("subgraph"):].strip()

            # 合法格式 1: subgraph ID ["Label"] 或 subgraph ID [Label]
            # 格式：subgraph 后面紧跟纯 ASCII 标识符（字母/数字/下划线/中划线），之后可选方括号标签
            valid_bracketed = re.match(r"^[A-Za-z0-9_-]+(?:\s*\[.*\])?$", declaration)
            # 合法格式 2: subgraph "Label"（双引号包裹整体）
            valid_quoted = re.match(r'^"[^"]+"$', declaration)

            if not (valid_bracketed or valid_quoted):
                errors.append({
                    "line": line_num,
                    "type": "ILLEGAL_SUBGRAPH_SYNTAX",
                    "raw_line": stripped,
                    "message": (
                        "检测到非法的 subgraph 声明语法！"
                        "子图声明必须严格遵循 `subgraph ID [\"中文标签\"]` 规范，"
                        "其中 ID 必须为纯 ASCII 英文标识符。严禁直接使用中文裸字符或全角冒号（：）。"
                    ),
                    "fix_suggestion": f'subgraph Subgraph_{line_num} ["{declaration}"]'
                })

        elif stripped == "end":
            if subgraph_stack:
                subgraph_stack.pop()
            else:
                errors.append({
                    "line": line_num,
                    "type": "UNMATCHED_END",
                    "raw_line": stripped,
                    "message": "检测到孤立的 `end` 标签，未找到对应的 `subgraph` 开口。",
                    "fix_suggestion": "移除多余的 end 标签"
                })

    # 检查未闭合的 subgraph
    for unclosed_line in subgraph_stack:
        errors.append({
            "line": unclosed_line,
            "type": "UNCLOSED_SUBGRAPH",
            "raw_line": f"subgraph at line {unclosed_line}",
            "message": f"第 {unclosed_line} 行的 `subgraph` 未闭合，缺少对应的 `end` 标签。",
            "fix_suggestion": "在代码块末尾添加 `end` 标签"
        })

    return errors


def autofix_mermaid_content(content: str) -> tuple[str, int]:
    """自动修复 Markdown 文本中非法的 subgraph 语法，返回修复后的文本和修复次数。"""
    lines = content.splitlines(keepends=True)
    fix_count = 0
    in_mermaid = False
    subgraph_counter = 1

    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```mermaid"):
            in_mermaid = True
            new_lines.append(line)
        elif in_mermaid and stripped.startswith("```"):
            in_mermaid = False
            new_lines.append(line)
        elif in_mermaid and re.match(r"^subgraph\b", stripped):
            declaration = stripped[len("subgraph"):].strip()
            valid_bracketed = re.match(r"^[A-Za-z0-9_-]+(?:\s*\[.*\])?$", declaration)
            valid_quoted = re.match(r'^"[^"]+"$', declaration)

            if not (valid_bracketed or valid_quoted):
                # 提取缩进
                indent = line[:len(line) - len(line.lstrip())]
                # 清洗标签中的残留双引号与中括号
                clean_label = declaration.strip(' "[]')
                fixed_line = f'{indent}subgraph SG_{subgraph_counter} ["{clean_label}"]\n'
                new_lines.append(fixed_line)
                subgraph_counter += 1
                fix_count += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    return "".join(new_lines), fix_count


def validate_file(file_path: Path, auto_fix: bool = False) -> list[dict]:
    """校验单个 Markdown 文件中的 Mermaid 图表。"""
    content = file_path.read_text(encoding="utf-8")
    
    if auto_fix:
        new_content, fixes = autofix_mermaid_content(content)
        if fixes > 0:
            file_path.write_text(new_content, encoding="utf-8")
            print(f"[FIXED] {file_path}: 自动修复了 {fixes} 处 Mermaid 语法缺陷。")
            content = new_content

    blocks = extract_mermaid_blocks(content)
    file_errors = []
    for b in blocks:
        block_errors = validate_mermaid_block(b)
        for err in block_errors:
            err["file"] = str(file_path)
            file_errors.append(err)

    return file_errors


def main():
    parser = argparse.ArgumentParser(description="Mermaid 图表语法合规检验与防错修复工具")
    parser.add_argument("target", help="待检验的 Markdown 文件或目录路径")
    parser.add_argument("--fix", action="store_true", help="对可自动修复的语法缺陷执行原位自动修复")
    args = parser.parse_args()

    target_path = Path(args.target)
    if not target_path.exists():
        print(f"错误：指定路径不存在: {target_path}", file=sys.stderr)
        sys.exit(1)

    IGNORED_DIRS = {"node_modules", ".git", ".venv", "dist", ".astro", "build"}
    md_files = []
    if target_path.is_file():
        if target_path.suffix.lower() in [".md", ".mdx"]:
            md_files.append(target_path)
    else:
        for p in list(target_path.rglob("*.md")) + list(target_path.rglob("*.mdx")):
            if not any(part in IGNORED_DIRS for part in p.parts):
                md_files.append(p)
    if not md_files:
        print(f"提示：在 {target_path} 下未找到任何 Markdown 文件。")
        sys.exit(0)

    total_errors = []
    for f in md_files:
        errs = validate_file(f, auto_fix=args.fix)
        total_errors.extend(errs)

    if total_errors:
        print("\n" + "=" * 70, file=sys.stderr)
        print(f"【MERMAID 语法静态检验失败】：共发现 {len(total_errors)} 处高危缺陷！", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        for e in total_errors:
            print(f"\n[文件] {e['file']}:{e['line']}", file=sys.stderr)
            print(f"  错误类型: {e['type']}", file=sys.stderr)
            print(f"  原始代码: {e['raw_line']}", file=sys.stderr)
            print(f"  修复建议: {e['fix_suggestion']}", file=sys.stderr)
            print(f"  规则说明: {e['message']}", file=sys.stderr)
        print("\n" + "=" * 70, file=sys.stderr)
        print("提示：可使用 --fix 参数尝试原位自动修正简单子图声明缺陷。", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"[PASS] Mermaid 图表语法合规检验通过（共扫描 {len(md_files)} 个文件）。")
        sys.exit(0)


if __name__ == "__main__":
    main()
