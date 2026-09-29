# AI Agent 入口与工程规约

## 仓库定位

本仓库是《融合新闻产品策划与制作》的公开课程资产中心。承载课程站点（Astro Starlight）、教材级深度讲义（`lecture_notes/`）与 Slidev 课件。

## 严格安全边界

1. **公开资产原则**：本仓库面向学生和学界公开，仅追踪讲义、课件、代码范例与站点配置。
2. **严禁混入学生隐私**：严禁提交任何班级花名册、学生成绩（`.xlsx`）、考勤记录、期末机密试卷或评语。
3. **敏感教务隔离**：学生管理、考勤与成绩处理全流程在独立的私有学期仓（如 `teaching-2026-2027-s1`）内进行。

## 关键技术栈与构建

- **站点工程**：Astro 7 + Starlight + Bun + Cloudflare Pages
- **部署地址**：`https://ronghe.yangzh.cn`
- **图表校验**：`python3 scripts/mermaid_validator.py site/src/content/docs/lectures/`
- **构建命令**：
  ```bash
  cd site
  bun run build
  ```

## 变更工作流

1. 修改讲义或站点页面后，必须先运行 `bun run build`（自动执行 Mermaid 静态校验与编译）。
2. 保持与整站北欧人文慢读出版风设计体系一致。
3. 验证通过后方可提交并推送至 `main` 分支。
