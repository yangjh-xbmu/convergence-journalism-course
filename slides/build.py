# INPUT: output/week{N}.md（Slidev Markdown）
# OUTPUT: dist/week{N:02d}/（静态 HTML，可直接部署）
# POS: 幻灯片构建工具，调用 Slidev CLI 将 Markdown 编译为静态网站
"""
将 Slidev Markdown 构建为静态 HTML。

用法：
    python build.py --week 1
    python build.py --all
    python build.py --week 3 --parts  # 四小节、操作材料及离线包

course_slug 从 course.yaml 的 ai.hugo_course_slug 读取（用于 base URL）。
"""

import argparse
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() in ('gbk', 'gb2312', 'cp936'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR    = Path(__file__).parent
OUTPUT_DIR  = BASE_DIR / "output"
DIST_DIR    = BASE_DIR / "dist"
CONFIG_PATH = BASE_DIR / "../config/course.yaml"
IS_WINDOWS  = platform.system() == "Windows"


def get_course_slug(config: dict) -> str:
    return (config.get("ai", {}).get("hugo_course_slug")
            or config["course"]["code"].lower())


def run_slidev_build(src: Path, out_dir: Path, base_url: str) -> bool:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    cmd = ["npx", "--no-install", "slidev", "build", str(src), "--out", str(out_dir), "--base", base_url]
    print(f"  命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(BASE_DIR), shell=IS_WINDOWS)
    return result.returncode == 0


def build_week(week: int, course_slug: str) -> bool:
    src = OUTPUT_DIR / f"week{week}.md"
    if not src.exists():
        print(f"✗ 找不到 {src}，请先运行 gen_content.py --week {week}")
        return False

    for asset in ("style.css", "global-top.vue", "setup/mermaid.ts", "public/favicon.svg"):
        target = OUTPUT_DIR / asset
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(BASE_DIR / asset, target)

    out_dir  = DIST_DIR / f"week{week:02d}"
    base_url = f"/slides/{course_slug}/week{week:02d}/"

    print(f"\n构建第 {week} 周幻灯片 → {out_dir.name}/  (base: {base_url})")
    ok = run_slidev_build(src, out_dir, base_url)
    if ok:
        print(f"[OK] 构建完成: dist/week{week:02d}/")
    else:
        print("✗ 构建失败")
    return ok


def prepare_materials(week: int) -> None:
    """Derive copyable classroom inputs from the approved lecture, not another prompt."""
    import zipfile

    lecture = (BASE_DIR.parent / "lecture_notes" / f"week{week}.md").read_text(encoding="utf-8")
    blocks = re.findall(r"^```(?:markdown|text|bash)\n(.*?)^```\s*$", lecture, re.M | re.S)

    def pick(label: str, predicate) -> str:
        matches = [block for block in blocks if predicate(block)]
        if len(matches) != 1:
            raise ValueError(f"讲义中无法唯一定位操作材料：{label}")
        return matches[0]

    skill = pick("Skill", lambda text: text.startswith("---\nname: account-audit\n"))
    files = {
        "demo/account-profile.md": pick("虚构账号", lambda text: text.startswith("# 账号说明\n") and "account_id：demo-campus" in text),
        "demo/samples.md": pick("虚构样本", lambda text: text.startswith("# 教学虚构样本")),
        "demo/feedback-log.md": pick("虚构反馈", lambda text: text.startswith("# 教学虚构反馈")),
        "demo/tasks/diagnose.md": pick("诊断任务", lambda text: text.startswith("# 账号诊断任务")),
        "demo/tasks/action-card.md": pick("行动卡任务", lambda text: text.startswith("读取 account-profile.md、samples.md、feedback-log.md 与 output/audit-draft.md。")),
        "demo/.omp/skills/account-audit/SKILL.md": skill,
        "demo/.workbuddy/skills/account-audit/SKILL.md": skill,
        "templates/account-profile.md": pick("账号填写模板", lambda text: text.startswith("# 账号说明\n") and "account_id：demo-campus" not in text),
        "templates/samples.md": (
            "# 本人账号样本记录\n\n"
            "仅填写已获准使用的材料；未知保持未知，代表作单列，重复作品沿用编号。\n\n"
            "| 编号 | 连续样本或代表作 | 平台及指标原名 | 作品链接或凭据 | 标题与摘要 | 发布时间 | 采集时间与窗口 | 数值及分母 | 制作工时及来源 | 信源与核查状态 |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        ),
        "templates/feedback-log.md": (
            "# 同伴走查记录\n\n"
            "尚未观察时不要填写结果；不能确认逐字准确的内容标为转述，不加引号。\n\n"
            "## 一条记录（复制本节新增）\n\n"
            "- 反馈编号：\n- 账号代号：\n- 材料编号及凭据：\n- 观察日期时间：\n"
            "- 反馈者脱敏代号与类别（经同意）：\n- 实际浏览范围：\n"
            "- 原话或转述（注明）：\n- 可见动作：\n"
            "- 活动后作者解释（另记）：\n- 记录者推测：\n- 待核问题与局限：\n\n"
            "先记录原话与动作，再讨论解释；不把同伴当成全部目标用户。\n"
        ),
        "templates/audit-log.md": (
            "# 人工核验与决定\n\n"
            "## 一次核验（复制本节新增）\n\n"
            "- 日期：\n- 执行方式及输入范围：\n- 实际输出路径：\n"
            "- 核查的问题：\n- 原始依据：\n- 更正结果（无误则写已查范围）：\n"
            "- 仍未核实什么：\n- 本人确认人、日期与范围：\n- 复查条件：\n\n"
            "未运行不写运行成功；未批准不写已确认；不记录密钥或私密原件。\n"
        ),
        "templates/action-card.md": (
            "# 行动卡草稿\n\n"
            "尚未确认优先问题时先列候选，不替本人选择。已存在文件时另存，不覆盖批注。\n\n"
            "- 本人确认的优先问题及依据编号：待本人确认\n\n"
            "## ① 保留\n\n已有做法及证据或价值依据：\n\n"
            "## ② 调整或暂缓\n\n本轮范围、依据与复查点：\n\n"
            "## ③ 一个验证问题\n\n希望区分的两种解释：\n\n"
            "## ④ 材料与时间\n\n- 所需材料、来源与授权：待取得、待核\n"
            "- 单次时间预算：待本人确认\n- 邀请人数：待本人确认\n\n"
            "## ⑤ 观察办法\n\n- 观察行为或指标、分母及比较对象：\n"
            "- 观察时限：待本人确认\n- 判断规则：待本人确认\n- 可能的其他解释：\n\n"
            "## ⑥ 人工确认\n\n- 确认人、日期与范围：待本人确认\n"
            "- 发布前事实、权利与隐私检查：待核\n- 发布或暂缓决定：待本人确认\n"
            "- 交给运营课的版本、来源与拟观察问题：\n\n"
            "每周可用时间不自动换成本次预算；本卡不授权平台操作或长期规则更新。\n"
        ),
        "lecture.md": lecture,
    }
    materials = BASE_DIR / "public" / "materials"
    materials.mkdir(parents=True, exist_ok=True)
    for relative, text in files.items():
        target = materials / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    shutil.copy2(BASE_DIR / "materials.html", materials / "index.html")
    with zipfile.ZipFile(materials / "account-audit-demo.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for relative, text in files.items():
            if relative.startswith("demo/"):
                archive.writestr(relative.removeprefix("demo/"), text)


def build_parts(week: int) -> bool:
    """Build four independent hash-routed decks and a local-server delivery bundle."""
    sources = [BASE_DIR / f"week{week}-part{part}.md" for part in range(1, 5)]
    missing = [str(source) for source in sources if not source.is_file()]
    if missing:
        print("缺少小节源文件：" + "、".join(missing))
        return False
    prepare_materials(week)
    destination = DIST_DIR / f"week{week:02d}"
    for part, source in enumerate(sources, 1):
        if not run_slidev_build(source, destination / f"part{part}", "./"):
            return False
    shutil.copy2(BASE_DIR / "offline.html", destination / "index.html")
    shutil.copy2(BASE_DIR / "preview.py", destination / "start.py")
    (destination / "start.command").write_text(
        '#!/bin/sh\ncd -- "$(dirname -- "$0")"\nexec python3 start.py\n', encoding="utf-8"
    )
    (destination / "start.command").chmod(0o755)
    (destination / "start.bat").write_text(
        '@echo off\r\ncd /d "%~dp0"\r\npy -3 start.py\r\nif errorlevel 1 pause\r\n', encoding="utf-8"
    )
    archive = shutil.make_archive(str(DIST_DIR / f"week{week:02d}-offline"), "zip", destination.parent, destination.name)
    print(f"[OK] 四套离线课件：{destination}\n[OK] 离线压缩包：{archive}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Slidev 静态构建")
    parser.add_argument("--week", type=int, default=None, help="构建指定课次")
    parser.add_argument("--all",  action="store_true",    help="构建所有已生成的幻灯片")
    parser.add_argument("--parts", action="store_true", help="构建指定课次的四个小节及离线包")
    args = parser.parse_args()
    if args.parts:
        if args.week is None or args.all:
            parser.error("--parts 必须与 --week 一起使用，不能与 --all 同用")
        sys.exit(0 if build_parts(args.week) else 1)

    # 旧的整课流程读取正式配置；手写小节不依赖共享库或教务材料。
    sys.path.insert(0, str(BASE_DIR.parent.parent / "course-toolkit" / "shared"))
    from config_loader import load_config

    config = load_config(CONFIG_PATH)
    course_slug = get_course_slug(config)

    if args.all:
        files = sorted(OUTPUT_DIR.glob("week*.md"))
        if not files:
            print("output/ 下没有找到 week*.md")
            sys.exit(1)
        ok = sum(1 for f in files
                 if (m := re.match(r'week(\d+)\.md', f.name)) and build_week(int(m.group(1)), course_slug))
        print(f"\n共构建 {ok}/{len(files)} 个幻灯片")
    elif args.week is not None:
        if not build_week(args.week, course_slug):
            sys.exit(1)
        print(f"\n下一步: python publish.py --week {args.week}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
