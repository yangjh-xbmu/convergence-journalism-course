# INPUT: course.yaml + syllabus.md + prompts/gen_lecture_note.md
# OUTPUT: output/week{N}.md（AI 生成的 Hugo 讲义）
# POS: 讲义生成工具链入口，串联 gen_content + publish
"""
一键生成讲义：AI 生成内容 → 可选发布到 hugo-blog。

用法：
    python run.py --week 1              # 生成第1周讲义到 output/
    python run.py --week 1 --publish    # 生成并发布到 hugo-blog
    python run.py --week 1 --dry-run    # 仅打印 prompt，不调用 API
"""

import argparse
import subprocess
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() in ('gbk', 'gb2312', 'cp936'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent


def run(cmd: list[str], step: str) -> int:
    print(f"\n{'='*60}")
    print(f"步骤: {step}")
    print(f"命令: {' '.join(cmd)}")
    print('='*60)
    result = subprocess.run(cmd, cwd=str(BASE_DIR))
    if result.returncode != 0:
        print(f"\n✗ {step} 失败（exit code {result.returncode}）")
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="一键生成课程讲义")
    parser.add_argument("--week",    type=int, default=1, help="课次号（默认 1）")
    parser.add_argument("--publish", action="store_true", help="生成后发布到 hugo-blog")
    parser.add_argument("--dry-run", action="store_true", help="仅打印 prompt，不调用 API")
    args = parser.parse_args()

    python = sys.executable
    week = str(args.week)

    cmd1 = [python, "gen_content.py", "--week", week]
    if args.dry_run:
        cmd1.append("--dry-run")
    rc = run(cmd1, f"Step 1: AI 生成第 {week} 周讲义内容")
    if rc != 0:
        sys.exit(rc)
    if args.dry_run:
        return

    if args.publish:
        md_path = BASE_DIR / "output" / f"week{week}.md"
        if not md_path.exists():
            print(f"\n✗ 找不到 {md_path}")
            sys.exit(1)
        cmd2 = [python, "publish.py", "--week", week]
        rc = run(cmd2, "Step 2: 发布到 hugo-blog")
        sys.exit(rc)
    else:
        print(f"\n[OK] 讲义已生成：output/week{week}.md")
        print(f"  审查后执行：python publish.py --week {week}")


if __name__ == "__main__":
    main()
