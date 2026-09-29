---
purpose: 《融合新闻产品策划与制作》公开课程资产库，包含出版级教材讲义、Astro Starlight 课程站及课件
status: active
next_steps:
  - 持续增补视听分镜与多模态实训案例文档
  - 维持 Starlight 课程站点边缘自动化构建与部署
capabilities:
  - convergence-journalism-course
  - starlight-documentation
  - mermaid-validation
  - slidev-presentation
---

# 融合新闻产品策划与制作 (Convergence Journalism)

本仓库是《融合新闻产品策划与制作》的公开课程资产中心，承载教材级全套讲义、在线课程站点源码以及教学课件。

- **课程在线站点**：[https://ronghe.yangzh.cn](https://ronghe.yangzh.cn)
- **部署服务**：基于 Cloudflare Pages 与 GitHub Actions 自动化持续集成与部署。

## 仓库结构

```text
course-convergence-journalism/
├── site/                     # Astro Starlight 课程站源码（北欧人文出版风设计体系）
│   ├── src/content/docs/     # 核心讲义（8 章教材级长文，约 42 万字）与教学大纲
│   └── src/theme/            # 纸墨质感主题与三层 Token 规范
├── lecture_notes/            # 课程全套讲义源文
├── slides/                   # Slidev 互动课件工程
├── scripts/                  # 工程治理脚本（含 Mermaid 全链路静态校验器）
└── .github/workflows/        # Cloudflare Pages 自动部署工作流
```

## 资产与隐私安全边界

本仓库为公开（Public）学术与教学智力资产库：
- 仅追踪并公开课程讲义、课件、代码、教案大纲及公开教学文档。
- 严禁存放任何学生隐私信息、班级花名册、平时成绩表、期末考卷以及考勤记录。学期教务与成绩管理在独立的私有学期仓内闭环。

## 本地开发与构建

```bash
cd site
bun install
bun run dev       # 启动本地开发预览 (默认端口 4321)
bun run build     # 运行 Mermaid 校验并构建静态站点
```
