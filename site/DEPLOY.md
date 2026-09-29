# 卓越班课程站点 Cloudflare Pages 自动化部署指南

本文档指导如何将《融合新闻产品策划与制作》独立 Starlight 站点接入 Cloudflare Pages，并绑定二级域名 `ronghe.yangzh.cn`，实现**本地更新 Markdown/MDX，推送 GitHub 后全自动边缘编译与发布**。

---

## 核心部署架构

```text
[本地编辑与推演]               [代码与事实源中枢]             [边缘自动化构建与全球分发]
本地 VS Code / OMP  ──git push──►  GitHub 远端仓库  ──Webhook──►  Cloudflare Pages
(site/src/content/docs)        (yangjh-xbmu/...)             (自动执行 bun run build -> dist)
                                                                     │
                                                                     ▼
                                                      https://ronghe.yangzh.cn (全球极速直连)
```

---

## 第一次接入配置步骤（仅需操作一次，用时约 2 分钟）

### 第一步：在 Cloudflare Pages 创建关联项目

1. 打开 [Cloudflare 控制台](https://dash.cloudflare.com/)。
2. 左侧导航栏进入 **Workers 和 Pages (Workers & Pages)** ➔ 点击 **创建应用程序 (Create application)**。
3. 选择 **Pages** 标签页 ➔ 点击 **连接到 Git (Connect to Git)**。
4. 授权并选中 GitHub 仓库：`yangjh-xbmu/teaching-2026-2027-s1`。

### 第二步：配置构建参数（关键）

在项目的构建配置页面，填写以下参数：

| 配置字段 | 填报内容 | 说明 |
| :--- | :--- | :--- |
| **项目名称 (Project name)** | `ronghe-course` | 可自定义，用于生成默认 pages.dev 域名 |
| **生产分支 (Production branch)** | `main` | 跟踪主分支提交 |
| **框架预设 (Framework preset)** | `Astro` | 自动匹配 Astro 静态构建环境 |
| **根目录 (Root directory)** | `融合新闻产品策划与制作/site` | **必须精准填写此相对路径** |
| **构建命令 (Build command)** | `bun run build` 或 `npm run build` | 编译静态页面与 Pagefind 索引 |
| **构建输出目录 (Output directory)** | `dist` | 静态产物目录 |

点击 **保存并部署 (Save and Deploy)**。Cloudflare Pages 将在 1 分钟内完成首次自动构建。

### 第三步：绑定二级域名 `ronghe.yangzh.cn`

由于您的主域名 `yangzh.cn` 已经在 Cloudflare 托管，二级域名绑定享受零配置自动化：

1. 进入刚创建的 Pages 项目主页 ➔ 切换到 **自定义域 (Custom domains)** 标签页。
2. 点击 **设置自定义域 (Set up a custom domain)**。
3. 输入二级域名：`ronghe.yangzh.cn` ➔ 点击继续。
4. Cloudflare 会自动识别托管在同一个账户下的 DNS 区域，全自动为您添加对应的 CNAME 记录并申请配置通用 SSL 证书（全程无需手动添加 DNS 解析）。
5. 等待数秒即可通过安全加密的 **`https://ronghe.yangzh.cn`** 全球高速访问。

---

## 日常教学内容更新工作流

完成首次配置后，后续所有教学内容的更新全部回归纯文本 Git 操作：

1. **本地编写或修改讲义**：
   在 `融合新闻产品策划与制作/site/src/content/docs/` 下编辑任意 `.md` 或 `.mdx` 文件（如第 6 周课件发布或作业通知修改）。
2. **提交并推送到 GitHub**：
   ```bash
   git add 融合新闻产品策划与制作/site/src/content/docs/
   git commit -m "docs(ronghe): update week 6 lecture notes"
   git push origin main
   ```
3. **静待自动上线**：
   GitHub 收到推送后，Cloudflare Pages 将通过 Webhook 毫秒级触发自动化构建流水线，通常在 30 秒至 1 分钟之内，`https://ronghe.yangzh.cn` 上的内容就会全量无缝更新，具备完整的全网搜索（Pagefind）支持。

---

## 多课程横向扩展经验

后续《融媒体内容生产实践》（专硕）、《统计与大数据分析》等课程需要上线独立站点时，采用完全相同的标准化模式：
- 复制 `site/` 工程模板至对应课程目录下。
- 在 Cloudflare Pages 中新建一个 Pages 项目，仅需将“根目录”指向该课程的 `site/` 路径。
- 分别绑定对应的二级域名（如 `mfa.yangzh.cn`、`stat.yangzh.cn`），实现全校课程的矩阵化独立分发。
