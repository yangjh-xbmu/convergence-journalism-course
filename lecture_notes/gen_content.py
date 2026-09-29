# INPUT: ../config/course.yaml + ../syllabus/syllabus.md + prompts/gen_lecture_note.md
# OUTPUT: output/week{N}.md（Hugo-ready Markdown 讲义，含 YAML frontmatter）
# POS: 讲义生成工具链第一步，调用 AI API 生成面向学生的 Markdown 讲义
"""
调用 Anthropic API 生成 Markdown 格式在线讲义（面向学生）。

用法：
    python gen_content.py --week 1
    python gen_content.py --week 1 --dry-run
    python gen_content.py --week 1 --output custom.md
"""

import argparse
import sys
from pathlib import Path

# ── 加载共享库 ──
SHARED = Path(__file__).parent.parent.parent / "course-toolkit" / "shared"
sys.path.insert(0, str(SHARED))

from config_loader import load_config
from ai_client import call_ai, strip_outer_fence
from prompt_builder import load_prompt, build_user_prompt
from syllabus_parser import parse_theory, get_week_entry
from date_calculator import compute_lecture_date

if sys.stdout.encoding and sys.stdout.encoding.lower() in ('gbk', 'gb2312', 'cp936'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR      = Path(__file__).parent
CONFIG_PATH   = BASE_DIR / "../config/course.yaml"
PROMPT_PATH   = BASE_DIR / "prompts/gen_lecture_note.md"
SYLLABUS_PATH = BASE_DIR / "../syllabus/syllabus.md"
OUTPUT_DIR    = BASE_DIR / "output"


def main():
    parser = argparse.ArgumentParser(description="调用 AI 生成 Markdown 格式在线讲义")
    parser.add_argument("--week",    type=int, default=1,  help="课次号（默认 1）")
    parser.add_argument("--output",  default=None,         help="输出路径（默认 output/week{N}.md）")
    parser.add_argument("--dry-run", action="store_true",  help="仅打印 prompt，不调用 API")
    args = parser.parse_args()

    print(f"加载配置 {CONFIG_PATH.resolve().name}...")
    config = load_config(CONFIG_PATH)

    syllabus_path = SYLLABUS_PATH.resolve()
    print(f"解析大纲 {syllabus_path.name}...")
    entries = parse_theory(syllabus_path)
    entry = get_week_entry(args.week, entries)
    if not entry:
        print(f"错误：未找到第 {args.week} 课次对应的大纲内容")
        sys.exit(1)
    print(f"  → 条目 #{entry.get('index')}: {entry.get('content', '')[:40]}")

    system, user_tpl = load_prompt(PROMPT_PATH)
    c = config["course"]
    s = config["school"]
    semester_start = s.get("semester_week1_monday", "2026-03-02")
    lesson_hours = int(entry.get("hours", 2)) if str(entry.get("hours", 2)).isdigit() else 2
    lecture_date = compute_lecture_date(args.week, semester_start)

    variables = {
        "course_name":          c["name"],
        "major":                s["major"],
        "week":                 args.week,
        "date":                 lecture_date,
        "lesson_hours":         lesson_hours,
        "syllabus_section":     entry.get("content", ""),
        "syllabus_requirements": entry.get("requirements", ""),
    }
    user = build_user_prompt(user_tpl, variables)

    if args.dry_run:
        print("\n" + "=" * 60)
        print("【SYSTEM PROMPT】")
        print(system)
        print("\n【USER PROMPT】")
        print(user)
        print("=" * 60)
        return

    print("\n调用 AI 生成讲义内容...")
    md_text = strip_outer_fence(call_ai(system, user, config))

    # ── Mermaid 语法安全自检与防错自动修复 ──
    from mermaid_validator import autofix_mermaid_content, extract_mermaid_blocks, validate_mermaid_block
    md_text, fix_count = autofix_mermaid_content(md_text)
    if fix_count > 0:
        print(f"  [Mermaid 守护] 自动修正了 {fix_count} 处非标准 subgraph 子图声明。")
    blocks = extract_mermaid_blocks(md_text)
    errors = [err for b in blocks for err in validate_mermaid_block(b)]
    if errors:
        print(f"  [警告] 检测到 {len(errors)} 处 Mermaid 语法风险：")
        for e in errors:
            print(f"    - 第 {e['line']} 行 ({e['type']}): {e['message']}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else OUTPUT_DIR / f"week{args.week}.md"
    output_path.write_text(md_text, encoding="utf-8")
    print(f"\n[OK] 讲义已保存到: {output_path}")
    print(f"  下一步: python publish.py --week {args.week}")


if __name__ == "__main__":
    main()
