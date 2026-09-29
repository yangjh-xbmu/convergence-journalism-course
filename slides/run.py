# INPUT: course.yaml + syllabus.md + prompts/gen_slides.md
# OUTPUT: 可选直接构建并发布幻灯片
# POS: 幻灯片工具链入口，串联 gen_content → build → publish
"""
一键生成幻灯片。

用法：
    python run.py --week 1                    # 仅生成 output/week1.md
    python run.py --week 1 --build            # 生成 + Slidev 构建
    python run.py --week 1 --build --publish  # 生成 + 构建 + 发布
    python run.py --week 1 --dry-run          # 仅打印 prompt
"""

import argparse
import subprocess
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() in ('gbk', 'gb2312', 'cp936'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent


def run_step(cmd: list[str], step: str) -> int:
    print(f"\n{'='*60}\n步骤: {step}\n命令: {' '.join(cmd)}\n{'='*60}")
    result = subprocess.run(cmd, cwd=str(BASE_DIR))
    if result.returncode != 0:
        print(f"\n✗ {step} 失败（exit {result.returncode}）")
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="一键生成课程幻灯片")
    parser.add_argument("--week",    type=int, default=1)
    parser.add_argument("--build",   action="store_true", help="生成后调用 Slidev 构建")
    parser.add_argument("--publish", action="store_true", help="构建后发布到 hugo-blog")
    parser.add_argument("--dry-run", action="store_true", help="仅打印 prompt")
    args = parser.parse_args()

    python = sys.executable
    week   = str(args.week)

    cmd1 = [python, "gen_content.py", "--week", week]
    if args.dry_run:
        cmd1.append("--dry-run")
    rc = run_step(cmd1, f"Step 1: AI 生成第 {week} 周幻灯片")
    if rc != 0 or args.dry_run:
        sys.exit(rc)

    print(f"\n[OK] output/week{week}.md 已生成，请审查后继续")

    if not args.build:
        print(f"  审查后执行: python build.py --week {week}")
        return

    rc = run_step([python, "build.py", "--week", week], "Step 2: Slidev 构建")
    if rc != 0:
        sys.exit(rc)

    if not args.publish:
        print(f"  审查后执行: python publish.py --week {week}")
        return

    rc = run_step([python, "publish.py", "--week", week], "Step 3: 发布到 hugo-blog")
    sys.exit(rc)


if __name__ == "__main__":
    main()
