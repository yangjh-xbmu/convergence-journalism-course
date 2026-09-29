# INPUT: ../config/course.yaml + ../syllabus/syllabus.md + ../lecture_notes/output/week{N}.md + prompts/gen_slides.md
# OUTPUT: output/week{N}.md（Slidev 格式幻灯片 Markdown）
# POS: 幻灯片生成工具链第一步，以讲义为主要依据，调用 AI 提炼 Slidev 格式幻灯片
"""
调用 Anthropic API 生成 Slidev 格式幻灯片。

用法：
    python gen_content.py --week 1
    python gen_content.py --week 1 --dry-run
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

# ── 加载共享库 ──
SHARED = Path(__file__).parent.parent.parent / "course-toolkit" / "shared"
sys.path.insert(0, str(SHARED))

from config_loader import load_config
from ai_client import call_ai, strip_outer_fence
from prompt_builder import load_prompt, build_user_prompt
from syllabus_parser import parse_theory, get_week_entry

if sys.stdout.encoding and sys.stdout.encoding.lower() in ('gbk', 'gb2312', 'cp936'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR           = Path(__file__).parent
CONFIG_PATH        = BASE_DIR / "../config/course.yaml"
PROMPT_PATH        = BASE_DIR / "prompts/gen_slides.md"
SYLLABUS_PATH      = BASE_DIR / "../syllabus/syllabus.md"
LECTURE_NOTES_DIR  = BASE_DIR / "../lecture_notes/output"
OUTPUT_DIR         = BASE_DIR / "output"


def extract_week_title(content: str) -> str:
    title = content.split("：")[0].split(":")[0].strip()
    return title[:20]


def fix_blank_cover_slide(text: str) -> str:
    """将 layout: cover 移入全局 frontmatter，避免空白封面页。"""
    return re.sub(
        r'^(---\n)([\s\S]*?)(---)\n\n+---\nlayout:\s*cover\n---\n',
        r'\1\2layout: cover\n\3\n',
        text
    )


def main():
    parser = argparse.ArgumentParser(description="AI 生成 Slidev 幻灯片")
    parser.add_argument("--week",    type=int, default=1)
    parser.add_argument("--output",  default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = load_config(CONFIG_PATH)
    entries = parse_theory(SYLLABUS_PATH.resolve())
    entry = get_week_entry(args.week, entries)
    if not entry:
        print(f"错误：未找到第 {args.week} 课次大纲内容")
        sys.exit(1)
    print(f"  → 条目 #{entry.get('index')}: {entry.get('content', '')[:40]}")

    # ── 读取讲义 ──
    lecture_path = LECTURE_NOTES_DIR / f"week{args.week}.md"
    if not lecture_path.exists():
        print(f"错误：未找到讲义 {lecture_path}")
        print(f"  请先运行: python ../lecture_notes/run.py --week {args.week}")
        sys.exit(1)
    lecture_content = lecture_path.read_text(encoding="utf-8")
    print(f"  讲义长度: {len(lecture_content)} 字符")

    system, user_tpl = load_prompt(PROMPT_PATH)
    c = config["course"]
    s = config["school"]
    lesson_hours = int(entry.get("hours", 2)) if str(entry.get("hours", 2)).isdigit() else 2
    variables = {
        "course_name":           c["name"],
        "major":                 s["major"],
        "semester":              s["semester_label"],
        "week":                  args.week,
        "week_title":            extract_week_title(entry.get("content", "")),
        "lesson_hours":          lesson_hours,
        "total_minutes":         lesson_hours * 45,
        "syllabus_section":      entry.get("content", ""),
        "syllabus_requirements": entry.get("requirements", ""),
        "lecture_content":       lecture_content,
    }
    user = build_user_prompt(user_tpl, variables)

    if args.dry_run:
        print("\n" + "="*60)
        print("【SYSTEM】\n", system)
        print("\n【USER】\n", user)
        return

    print("\n调用 AI 生成幻灯片...")
    md_text = strip_outer_fence(call_ai(system, user, config))
    md_text = fix_blank_cover_slide(md_text)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = Path(args.output) if args.output else OUTPUT_DIR / f"week{args.week}.md"
    out.write_text(md_text, encoding="utf-8")

    # Slidev 要求 style.css 与 Markdown 同目录
    style_src = BASE_DIR / "style.css"
    if style_src.exists():
        shutil.copy2(style_src, OUTPUT_DIR / "style.css")
        print("  style.css → output/")

    print(f"\n[OK] 幻灯片已保存: {out}")
    print(f"  下一步: python build.py --week {args.week}")


if __name__ == "__main__":
    main()
