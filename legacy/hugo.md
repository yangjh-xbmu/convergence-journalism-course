# Hugo--开源内容管理工具

## 静态网站

与动态网站相比，静态网站包含固定内容，每个访问者看到的都是相同的页面。具有建设成本低，发布渠道广泛等优势。

## Hugo 简介

[Hugo](https://gohugo.io/) 是一个用于构建网站的开源静态网站生成器。

![](https://oss-yangjh.oss-cn-chengdu.aliyuncs.com/images/202311231445562.png)

### 为什么选择 Hugo

:::: {.columns}

::: {.column width="40%"}
![](https://oss-yangjh.oss-cn-chengdu.aliyuncs.com/images/202311241113636.png)
:::

::: {.column width="60%"}

- 速度快: Hugo 构建网站的速度非常快，可以迅速发布新闻。
- 易部署: 可以使用多个平台免费部署，适合预算有限的情景。
- 易学习: Hugo 的学习曲线较低，适合非技术背景的学生。
- 人气旺: Hugo 有一个活跃的社区，提供大量的主题和插件，方便用户设计和自定义网站。
:::

::::

### 安装 Hugo

使用包管理工具安装Hugo：例如在Windows终端中，使用`winget`安装：

```bash
winget install Hugo.Hugo.Extended
```

安装完毕后，重启终端，运行如下命令查看是否安装成功：

```bash
hugo version
```

### 安装Git

从官网下载Git，按照默认设置安装即可。

### 安装编辑器

安装文本编辑器，以便完成对内容的编辑。推荐使用VS Code编辑器。

### 选择主题

- 在官网主题列表中选择合适的主题:

例如：<https://github.com/theNewDynamic/gohugo-theme-ananke>

### 安装主题并初始化

```bash
hugo new site quickstart
cd quickstart
git init
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
echo "theme = 'ananke'" >> hugo.toml
hugo server
```

### 主要目录结构解析

- archetypes：主要用于定义新内容文件（如博客文章、新闻稿等）的模板。
- content: 存放所有的新闻文章和页面。
- static: 用于存放图片、CSS、JavaScript等静态资源。
- layouts: 存放模板文件，用于定义网站的布局和外观。
- config.toml: Hugo 的主要配置文件。

## 内容管理

可以通过命令或者编辑器创建新闻内容。

可以使用Markdown语法继续内容的标注。

### 极简Markdown语法

- 标题使用`#`进行标记
- 图片使用`![]()`这样的语法进行标记
- 视频可以使用在线播放器地址,也可以自定义短代码的方式进行标记

### 自定义短代码

```html
<style>
    .meta-media {
      position: relative;
      margin-bottom: 30px;
      display: flex;
      width: 100%;
      height: 0;
      padding-bottom: 75%;
    }
    .video {
      position: absolute;
      width: 100%;
      height: 100%;
      left: 0;
      top: 0;
    }
    </style>
    <div class="meta-media">
        <iframe src="{{ .Get "src" }}&high_quality=1" frameborder="no" scrolling="yes" allowfullscreen="allowfullscreen" high_quality="1" framespacing="1" class="video" >
    </iframe>
    </div>
```

### 使用front matter进行内容属性的设置

```text
---
title: "Ananke: a Hugo Theme"

description: "The last theme you'll ever need. Maybe."
# 1. To ensure Netlify triggers a build on our exampleSite instance, we need to change a file in the exampleSite directory.
theme_version: '2.8.2'
cascade:
  featured_image: '/images/gohugo-default-sample-hero-image.jpg'
---
Welcome to my blog with some of my work in progress. I've been working on this book idea. You can read some of the chapters below.
```

## 网站配置

```yoml
languageCode = 'zh'
theme = 'ananke'
title = '搞个大新闻网'

[[menu.main]]
identifier = "home"
name = "Home"
url = "/"
weight = 10

[[menu.main]]
identifier = "post"
name = "Posts"
url = "/posts/"
weight = 20

[markup]
defaultMarkdownHandler = "goldmark"
[markup.goldmark]
[markup.goldmark.renderer]
unsafe = true

```

## 网站部署

参见<https://www.yangzh.cn/notes/front-end/deploy.html>

## 实践：创建一个简单的新闻网站

为自己的团队、社团、项目建立新闻网站，并持续维护。

## 进阶功能

- 增加评论
- 增加统计
- 增加数据埋点
- 绑定域名
- 自定义模版

## 参考资料

1. <https://hugo-in-action.foofun.cn/zh/>
2. <https://gohugo.io/>
3. <https://themes.gohugo.io/>
