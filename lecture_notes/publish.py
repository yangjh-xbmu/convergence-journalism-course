# INPUT: output/week{N}.md
# OUTPUT: hugo-blog/content/courses/{course_slug}/week{N:02d}/index.md
# POS: 讲义发布工具，将审查后的 Markdown 复制到 hugo-blog 仓库
"""
将讲义从 output/ 发布到 hugo-blog。

用法：
    python publish.py --week 1
    python publish.py --all

course_slug 从 course.yaml 读取（ai.hugo_course_slug 字段，默认使用课程代码）。
"""

import argparse
import re
import sys
from pathlib import Path

# ── 加载共享库 ──
SHARED = Path(__file__).parent.parent.parent / "course-toolkit" / "shared"
sys.path.insert(0, str(SHARED))

from config_loader import load_config
from hugo_publisher import publish_lecture_note


def build_course_meta(config: dict) -> dict:
    """从 course.yaml 构建课程元信息，供 _index.md 自动生成使用。"""
    c = config["course"]
    s = config["school"]
    return {
        "title":          c["name"],
        "course_code":    c["code"],
        "semester":       s["semester_label"],
        "total_hours":    c["total_hours"],
        "theory_hours":   c["theory_hours"],
        "practice_hours": c["practice_hours"],
        "department":     s["department"],
        "major":          s["major"],
    }

if sys.stdout.encoding and sys.stdout.encoding.lower() in ('gbk', 'gb2312', 'cp936'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR    = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "../config/course.yaml"
OUTPUT_DIR  = BASE_DIR / "output"


def get_course_slug(config: dict) -> str:
    """从 course.yaml 的 ai.hugo_course_slug 读取，或用课程代码作为 fallback。"""
    return (config.get("ai", {}).get("hugo_course_slug")
            or config["course"]["code"].lower())


def main():
    parser = argparse.ArgumentParser(description="发布讲义到 hugo-blog")
    parser.add_argument("--week", type=int, default=None, help="发布指定课次")
    parser.add_argument("--all",  action="store_true",    help="发布 output/ 下所有已生成讲义")
    args = parser.parse_args()

    config = load_config(CONFIG_PATH)
    course_slug = get_course_slug(config)
    course_meta = build_course_meta(config)

    if args.all:
        md_files = sorted(OUTPUT_DIR.glob("week*.md"))
        if not md_files:
            print("output/ 下没有找到 week*.md 文件")
            sys.exit(1)
        ok = 0
        for f in md_files:
            m = re.match(r'week(\d+)\.md', f.name)
            if m:
                if publish_lecture_note(int(m.group(1)), OUTPUT_DIR, course_slug,
                                        course_meta=course_meta):
                    ok += 1
        print(f"\n共发布 {ok}/{len(md_files)} 篇讲义")
    elif args.week is not None:
        if not publish_lecture_note(args.week, OUTPUT_DIR, course_slug,
                                    course_meta=course_meta):
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
