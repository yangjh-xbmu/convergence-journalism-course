# INPUT: dist/week{N:02d}/（Slidev 静态构建产物）
# OUTPUT: hugo-blog/static/slides/{course_slug}/week{N:02d}/
# POS: 幻灯片发布工具，将构建产物复制到 Hugo 静态资源目录
"""
将构建好的幻灯片发布到 hugo-blog 静态目录。

用法：
    python publish.py --week 1
    python publish.py --all
"""

import argparse
import re
import sys
from pathlib import Path

# ── 加载共享库 ──
SHARED = Path(__file__).parent.parent.parent / "course-toolkit" / "shared"
sys.path.insert(0, str(SHARED))

from config_loader import load_config
from hugo_publisher import publish_slides

if sys.stdout.encoding and sys.stdout.encoding.lower() in ('gbk', 'gb2312', 'cp936'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR    = Path(__file__).parent
DIST_DIR    = BASE_DIR / "dist"
CONFIG_PATH = BASE_DIR / "../config/course.yaml"


def get_course_slug(config: dict) -> str:
    return (config.get("ai", {}).get("hugo_course_slug")
            or config["course"]["code"].lower())


def main():
    parser = argparse.ArgumentParser(description="发布幻灯片到 hugo-blog")
    parser.add_argument("--week", type=int, default=None, help="发布指定课次")
    parser.add_argument("--all",  action="store_true",    help="发布所有已构建的幻灯片")
    args = parser.parse_args()

    config = load_config(CONFIG_PATH)
    course_slug = get_course_slug(config)

    if args.all:
        dirs = sorted(DIST_DIR.glob("week*"))
        if not dirs:
            print("dist/ 下没有构建产物，请先运行 build.py --all")
            sys.exit(1)
        ok = sum(1 for d in dirs
                 if (m := re.match(r'week(\d+)', d.name)) and publish_slides(int(m.group(1)), DIST_DIR, course_slug))
        print(f"\n共发布 {ok}/{len(dirs)} 个幻灯片")
    elif args.week is not None:
        if not publish_slides(args.week, DIST_DIR, course_slug):
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
