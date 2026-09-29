// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { unified } from '@astrojs/markdown-remark';

export default defineConfig({
  site: 'https://ronghe.yangzh.cn',
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
  },
  integrations: [
    starlight({
      title: '融合新闻产品策划与制作',
      description: '2026-2027学年第一学期 2023级卓越新闻学实验班 数字化中台与课程工作区',
      favicon: '/favicon.svg',
      defaultLocale: 'root',
      locales: {
        root: {
          label: '简体中文',
          lang: 'zh-CN',
        },
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/yangjh-xbmu/course-convergence-journalism' },
      ],
      sidebar: [
        {
          label: '课程概览与规程',
          items: [
            { label: '课程导读与教学大纲', slug: 'syllabus' },
            { label: '过程性考核量规 (Rubrics)', slug: 'syllabus/rubrics' },
          ],
        },
        {
          label: '学期深度讲义教材',
          items: [
            { label: '第一章：人机协同采编工作台与可署名责任', slug: 'lectures/week1' },
            { label: '第二章：原子化知识库解构与智能体编排流水线', slug: 'lectures/week2' },
            { label: '第三章：账号逆向工程与融媒体产品最小可行原型', slug: 'lectures/week3' },
            { label: '第四章：内容情报雷达与选题发现工程', slug: 'lectures/week4' },
            { label: '第五章：选题决策模型与出版级内容简报工程', slug: 'lectures/week5' },
            { label: '第六章：多模态视听工程与分镜流水线', slug: 'lectures/week6' },
            { label: '第七章：人工审核把关、反馈闭环与审计台账', slug: 'lectures/week7' },
            { label: '第八章：全流程运行、作品集验收与自主可控工作流', slug: 'lectures/week8' },
          ],
        },
        {
          label: '实训作业与任务通知',
          items: [{ autogenerate: { directory: 'assignments' } }],
        },
        {
          label: '工规指南与答疑中台',
          items: [
            { label: 'GitHub Issue 提问向导与规范', slug: 'guides/issue-guidelines' },
            { label: 'WorkBuddy 本地环境与技能配置', slug: 'guides/workbuddy-setup' },
          ],
        },
      ],
      components: {
        Header: './src/theme/Header.astro',
        Hero: './src/theme/Hero.astro',
        Footer: './src/theme/Footer.astro',
      },
      customCss: [
        'katex/dist/katex.min.css',
        './src/theme/tokens.css',
        './src/theme/nordic.css',
      ],
    }),
    mermaid({
      autoTheme: false,
      theme: 'base',
      mermaidConfig: {
        theme: 'base',
        htmlLabels: false,
        fontFamily: '"PingFang SC", "Hiragino Sans GB", "Source Han Sans SC", "Microsoft YaHei", -apple-system, sans-serif',
        fontSize: 12,
        flowchart: {
          htmlLabels: false,
          useMaxWidth: true,
          wrappingWidth: 240,
          minNodeWidth: 150,
          curve: 'linear',
          nodeSpacing: 40,
          rankSpacing: 48,
          padding: 24,
        },
        themeVariables: {
          darkMode: false,
          fontFamily: '"PingFang SC", "Hiragino Sans GB", "Source Han Sans SC", "Microsoft YaHei", -apple-system, sans-serif',
          fontSize: '12px',
          primaryColor: '#FDFCF9',
          primaryTextColor: '#1E1D1B',
          primaryBorderColor: '#262421',
          lineColor: '#7E786E',
          secondaryColor: '#FAF6ED',
          tertiaryColor: '#F3ECE0',
          clusterBkg: '#FAF6ED',
          clusterBorder: '#DDD5C5',
          titleColor: '#B4533C',
          edgeLabelBackground: '#FDFCF9',
          nodeBorder: '#262421',
          mainBkg: '#FDFCF9',
        },
      },
    }),
  ],
});
