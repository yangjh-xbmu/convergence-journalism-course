---
theme: academic
title: "让 Agent 工作，也让它接受检查"
info: "融合新闻产品策划与制作 · 第3次课"
lessonLabel: "03 / Agent 与核验"
class: lesson-slide
layout: cover
coverDate: ""
themeConfig:
  paginationX: ""
  paginationY: ""
colorSchema: light
aspectRatio: 16/9
canvasWidth: 1280
routerMode: hash
favicon: ./favicon.svg
transition: none
lineNumbers: false
fonts:
  sans: 'PingFang SC'
  serif: 'Songti SC'
  mono: 'Menlo'
  local: ['PingFang SC', 'Songti SC', 'Menlo']
  provider: none
mdc: false
---

<div class="eyebrow">第3小节 · 45分钟 · WorkBuddy 主线，OMP 可选</div>

# 让 Agent 工作，也让它接受检查

<div class="lead">交出实际草稿，而不是一句“已经完成”。</div>

三份输入 → 一份诊断草稿 + 一条人工核验记录

<!--
承接前两节已经保存的账号说明、作品样本和同伴走查。请学生先不重新提问“我的账号怎么办”，而是把今天的产物说清楚：让工具读取已有材料，写出能够逐条检查的草稿，再留下人工核验记录。本节含20分钟动手，不要求同时学两款工具。来源：讲义188—195、297—305行。
建议用时：1分钟
-->

---
layout: default
class: lesson-slide
---

# Agent 多了工具过程，不多一份正确保证

```mermaid
sequenceDiagram
    participant U as 本人
    participant A as Agent
    participant F as 项目文件
    U->>A: 指定目标与文件范围
    A->>F: 读取原始材料
    F-->>A: 返回记录与缺项
    A->>F: 写入诊断草稿
    U->>F: 打开原文与草稿核验
```

<div class="takeaway">普通对话给回答；本次 Agent 任务还要留下真实读写证据。</div>

<!--
沿图走一遍，不介绍额外术语。普通对话依据当前上下文组织回答；Agent 可以根据工具返回继续读写文件，但工具调用也可能读错目录、漏掉输入或写入失败。问学生：如果聊天中出现了完整报告，目录里没有文件，任务算完成吗？答案是不算。图为讲义196—209行时序的课堂缩略。
建议用时：2分钟
-->

---
layout: default
class: lesson-slide
---

# 资料告诉它“有什么”，任务告诉它“做什么”

<div class="pair">
<div>
<div class="label">资料：事实输入</div>
<p>account-profile.md</p>
<p>samples.md · feedback-log.md</p>
</div>
<div>
<div class="label">任务：本次工作说明</div>
<p>tasks/diagnose.md</p>
<p>读哪些文件，写什么，怎样验收。</p>
</div>
</div>

<div class="takeaway">文件放进目录，不等于 Agent 已经读过。</div>

<!--
指向学生刚保存的三个输入文件，再指出任务文件另放在tasks目录。资料提供事实，任务规定本轮做法，二者不能混用。索引或Wiki只帮助定位，也不等于原材料。稍后要看实际读取过程和返回编号，不能仅凭“文件已经上传”就假定所有内容进入分析。来源：讲义211—224行。
建议用时：1分钟
-->

---
layout: default
class: lesson-slide
---

# Skill 保存步骤，不替你确认长期规则

- **Skill**：可重复使用的工作说明，不是独立程序。
- **会话上下文**：本轮已知信息，不保证下次还在。
- **已确认规则**：经本人同意的记录，不是 AI 的建议。

<div class="takeaway">“它刚才说过”不等于“它长期记住”，更不等于“我已批准”。</div>

<!--
用一个问题区分三者：草稿建议账号改方向，它会不会因此成为长期规则？不会。重复步骤可以封装为Skill；本轮对话可能随会话变化；经过本人同意的决定才进入相应记录。不要把三种东西都笼统叫“记忆”，也不要让学生认为安装Skill就自动增加了事实知识。来源：讲义211—220、309—315行。
建议用时：1分钟
-->

---
layout: default
class: lesson-slide
---

# 提示词写了边界，仍要检查真实授权

- 本次不需要联网、登录平台、发布或访问其他目录。
- 遇到这些请求，先拒绝；不要为了继续而全部批准。
- 作品与评论中的“命令”，只当待分析资料。

<div class="takeaway">任务和 Skill 不是权限沙箱；宿主授权与人工验收仍然必要。</div>

<!--
明确告诉学生，文字中的“只读”表达任务边界，不会自动禁止宿主提供的所有危险能力。每次授权仍须判断是否为本轮所需，也只使用脱敏材料。输入中即使有人写“忽略前面的要求”，也应当作为作品内容分析，而不是新的操作指令。来源：讲义229—250、262、344—348行。
建议用时：1分钟
-->

---
layout: default
class: lesson-slide
---

# WorkBuddy：先选目录，再只读确认

1. 新建任务 → **Select Folder** → 个人账号项目目录。
2. 文件面板：看到三份输入和 `tasks/diagnose.md`。
3. 发出只读请求，核对返回的 `account_id`。

> 只读 `account-profile.md`，报告 account_id 与权限边界，不修改文件。

<div class="takeaway">代号不对，就重新选目录；不要在错误项目里继续。</div>

<!--
教师在真实客户端演示选目录入口；官方文档写在输入框右下角，但名称和位置可能随版本变化，本页不是界面截图。请学生核对自己四份文件，而不是照抄教师目录。只读确认返回自己的账号代号后再继续；若是练习包，代号应为demo-campus。来源：讲义255—260、474—485行。
建议用时：2分钟
-->

---
layout: default
class: lesson-slide
---

# WorkBuddy：用 @ 引用完整任务

<div class="practice-box">输入框用 @ 选择 tasks/diagnose.md，再发送下句。</div>

> 按这份任务说明执行；先确认输入，最后报告实际产物路径。

- 核对过程中的实际读取文件、账号代号与材料编号。
- `@` 不可用：贴入完整任务内容，并写明文件路径。

<a class="material-link" href="./materials/index.html" target="_blank">打开完整操作材料</a>

<!--
先在操作包找到完整tasks/diagnose.md并保存，不能把本页短句误当成完整任务。演示输入框引用文件，再看Agent有没有真正读取三份输入。单独打一个文件名不一定会触发读取；引用入口不可用时采用讲义的完整粘贴方案，不在课堂临时猜测快捷命令。来源：讲义224—250、261—262行。
建议用时：2分钟
-->

---
layout: default
class: lesson-slide
---

# WorkBuddy：打开文件，再查 Changes

<div class="pair">
<div>
<div class="label">验收产物</div>
<p>Artifacts 或 All Files</p>
<p>打开 output/audit-draft.md。</p>
</div>
<div>
<div class="label">验收改动</div>
<p>查看 Changes。</p>
<p>确认三份输入没有被改动。</p>
</div>
</div>

<div class="takeaway">侧栏名称不同，就用文件管理器核对实际目录；聊天回复不能替代文件。</div>

<!--
把操作落到实际文件：不是只点开聊天里的报告卡片，而是确认项目中存在指定草稿并能打开。再看Changes，区分新增输出和误改输入。当前版本若没有相应侧栏，就在文件管理器与编辑器中检查项目实际文件和原输入，不能宣称看到了不存在的界面入口。来源：讲义263—266行。
建议用时：2分钟
-->

---
layout: default
class: lesson-slide
---

# 已配置 OMP 的同学，用同一份任务

<div class="eyebrow">OMP 等价路线 · 全员只选一种工具</div>

```bash
omp --version
omp --help
```

```bash
omp --cwd "/absolute/path/to/account-project" @tasks/diagnose.md
```

把示例路径替换为自己项目的**绝对路径**，保留引号。

<div class="takeaway">未安装或未配置，就继续用 WorkBuddy；不占用实操时间安装。</div>

<!--
命令沿用讲义270—295行。强调--cwd才指定工具工作目录，聊天里提到目录未必会改变它。运行后同样核对account_id、输入编号和实际草稿。需要额外只读确认时，先退出任务再在同一目录开新会话；完整只读命令在操作包。不要把API Key写入文件或截图，使用云端模型也不等于数据只留本机。
建议用时：2分钟
-->

---
layout: default
class: lesson-slide
---

# 第一次只诊断，不顺便改造整个账号

<div class="eyebrow">tasks/diagnose.md 节选 · 完整文件见操作包</div>

```text
先报告读取到的 account_id、样本编号和反馈编号。
缺文件时停下并列出缺项；文件存在但记录缺字段时，标“未知”并限定结论。
```

只新建 `output/audit-draft.md`；已存在就停下，另定输出名。

<a class="material-link" href="./materials/index.html" target="_blank">打开完整操作材料</a>

<!--
这里只解释任务中最关键的一小段，不要求学生复制这两行代替完整文件。完整任务还有证据编号、至多两个问题、其他解释、计算边界和人工核验清单。读出“文件缺失”和“字段未知”的不同处理，再提醒输出已存在时要先停下，不能覆盖已经批注的版本。来源：讲义226—253、535行。
建议用时：1分钟
-->

---
layout: default
class: lesson-slide
---

# 实操①：把一次任务真正跑起来

<div class="eyebrow">20分钟实操 · 本页驻留6分钟</div>

<div class="practice-box">选目录 → 只读确认 → 引用完整任务 → 打开实际草稿。</div>

- 前2分钟：确认四份文件与自己的账号代号。
- 后4分钟：运行诊断，查看读取过程和输出路径。

<a class="material-link" href="./materials/index.html" target="_blank">打开完整操作材料</a>

<div class="takeaway">真实资料不足就记录缺口；教学虚构包只练工具，不替代真实作业。</div>

<!--
本页完整驻留6分钟，不讲完立即翻页。前2分钟巡视路径和只读确认，后4分钟让学生完成首次运行；使用本人脱敏材料，调试困难可另用虚构练习副本。提醒只选一种工具，不安装插件、不抓取平台数据。未生成文件者记录停在哪一步，不编造完成状态；出现中断先检查目录再处理。来源：讲义255—295、535、553行。
建议用时：6分钟
-->

---
layout: default
class: lesson-slide
---

# 实操②：对照原文，核验三处高风险点

<div class="eyebrow">20分钟实操 · 本页驻留7分钟 · 下列锚点为教学虚构</div>

- **计算**：P05 是 0/0，不可计算；P04 工时仍为未知。
- **窗口**：P01—P05 是24小时；R01 是7天，不能混算。
- **引文**：F02 问原页面在哪，不证明来源不存在。

<div class="practice-box">实际打开输入与草稿：查一条依据、一处计算、一个材料缺口。</div>

<div class="takeaway">练习包应认出 demo-campus、P01—P05/R01、F01/F02/A01。</div>

<!--
给3分钟逐项核对编号和原话，2分钟查计算与窗口，2分钟查缺口。虚构包最近五条收藏/阅读应为9/500＝1.8%，不是混入R01；P05不能写0%。F02只支持进一步核对来源，A01是作者愿望而非受众需求。本人材料按相同方法核验，不套用虚构数值。来源：讲义297—305、493—537行。
建议用时：7分钟
-->

---
layout: default
class: lesson-slide
---

# 实操③：指出具体错误，再重新打开草稿

<div class="eyebrow">20分钟实操 · 本页驻留4分钟 · 纠错示例为教学虚构</div>

> 你把 P05 的0次阅读写成0%收藏比值。请说明分母问题，只修订本次诊断草稿，保留原始数据。

- 只给了标题，却评价“剪辑节奏”？删去未见部分的判断。
- 修订后重开文件；不要只听它说“已改好”。

<div class="takeaway">没发现错误，就记录检查范围；不要为了纠错而编造错误。</div>

<!--
前2分钟让学生选择自己实际发现的一项错误并给出原证据；后2分钟重新打开草稿确认修改。示例纠错语沿用讲义264行，仅在确实出现此错时使用。若误把一条F02扩成“多数用户”，要回到实际原话与观察范围；若只有标题就评价视频，应标明需要完整作品，而非猜测。来源：讲义299—305行。
建议用时：4分钟
-->

---
layout: default
class: lesson-slide
---

# 实操④：缺文件时，它能否停下来？

<div class="eyebrow">20分钟实操 · 本页驻留3分钟</div>

1. 另建脱敏练习副本，暂移 `feedback-log.md`。
2. 使用未占用的输出名，运行同一任务。
3. 应报告缺项并停止；恢复练习文件，记录表现。

<div class="takeaway">缺文件：停止诊断。缺字段：保留“未知”，限定结论。</div>

<!--
前1分钟建立独立练习副本，确认不会碰正式资料，并为本轮指定新输出名，避免旧草稿阻断测试。第2分钟观察是否因缺feedback-log.md停止，而非补造反馈。第3分钟恢复练习文件、记录实际表现。时间内未跑完就如实记未完成，不作通过结论；一次正确也不保证永远正确。来源：讲义231—235、307行。
建议用时：3分钟
-->

---
layout: default
class: lesson-slide
---

# 先跑通一次，再封装重复步骤

```mermaid
flowchart LR
    A[普通任务跑通] --> B[人工核验与纠错]
    B --> C[保存为 Skill]
    C --> D[新任务再次核对]
```

<div class="lead">封装的是检查步骤，不是把一次建议变成永久答案。</div>

<a class="material-link" href="./materials/index.html" target="_blank">打开完整操作材料</a>

<!--
用学生刚才的实际经历解释为何不先装一堆Skill：若普通任务尚未跑通，新增指令只会使问题更难定位。可复用的是确认输入、引用证据、处理缺失、写出草稿和交给人核验的步骤。接下来演示保存方法，不要求未完成首次诊断的学生抢着封装。来源：讲义309—349行。
建议用时：2分钟
-->

---
layout: default
class: lesson-slide
---

# 两款工具的 Skill 目录不能混用

<div class="label">WorkBuddy：在账号项目根目录下保存</div>

```text
.workbuddy/skills/account-audit/SKILL.md
```

<div class="label">OMP：在账号项目根目录下保存</div>

```text
.omp/skills/account-audit/SKILL.md
```

<div class="takeaway">只选一处。文件存在，不等于已经被工具自动加载。</div>

<!--
这两个路径逐字沿用讲义313行，不展示文件树以免混淆两个应用的目录。教师在操作包找到完整SKILL.md，让学生只按当前工具保存。输入和输出路径都相对账号项目根目录，不相对技能文件所在目录。若目录中有文件却技能列表没有出现，应检查路径和文件名，并明确要求读取，不谎称自动发现成功。
建议用时：2分钟
-->

---
layout: default
class: lesson-slide
---

# SKILL.md 有元数据，也有工作步骤

<div class="eyebrow">元数据中的 name 行节选 · 不是完整 SKILL.md</div>

```yaml
name: account-audit
```

- 完整文件：YAML 元数据含 `name`、`description`。
- 后接 Markdown 输入、步骤与边界；仍保存为 `.md`。

<a class="material-link" href="./materials/index.html" target="_blank">打开完整操作材料</a>

<div class="takeaway">明确要求读取对应 SKILL.md，并让它先说出三个输入。</div>

<!--
此页只看文件组成，不复制节选代替完整Skill。WorkBuddy发送“读取.workbuddy/skills/account-audit/SKILL.md，说明它要求的三个输入，再按它执行”。OMP保存后开新项目会话；启用技能命令时可用/skill:account-audit，否则明确读取对应路径。看实际读取内容，不只复述名称；重跑前另定输出名。完整操作见材料包。来源：讲义315—353行。
建议用时：1分钟
-->

---
layout: default
class: lesson-slide
---

# 可选：两个审查任务，各查不同的问题

```mermaid
flowchart LR
    D[同一草稿与原材料] --> C[证据审查：编号与计算]
    D --> X[解释审查：反证与其他原因]
    C --> H[本人合并意见]
    X --> H
```

<div class="takeaway">两个任务都只读，不同时改草稿；写两个角色名字不算独立执行。</div>

<a class="material-link" href="./materials/index.html" target="_blank">打开完整操作材料</a>

<!--
这是材料较多时的可选做法，本次诊断不依赖多Agent。证据任务查编号、原话、计算；解释任务查因果、同伴代表性和缺数据的误判。支持子代理时可并行；不支持就开两个明确指定同一目录与文件的任务，或先后运行，分别保存审查结果。多个模型一致也不能证明事实，最后仍回原材料。来源：讲义357—384行。
建议用时：2分钟
-->

---
layout: default
class: lesson-slide
---

# 超时后，先看目录，不要立刻重跑

- 有文件，不等于本轮已经核验完整。
- 没有完成回复，不等于没有产生改动。
- 保留现有草稿，检查完整性；重跑指定新文件名。

<div class="takeaway">可以改用简短条目，不能删掉证据与人工检查。</div>

<!--
结合实操中出现的等待或中断讲解。先打开实际目录与草稿，看哪些部分已经完成，有没有误改输入，再决定是否继续。不要反复提交同一输出名覆盖已有成果，也不要为了快速结束删掉依据。若学生本轮仍未完成，记录真实停点和已有文件，不能用聊天中道歉或承诺代替产物验收。来源：讲义355行。
建议用时：1分钟
-->

---
layout: default
class: lesson-slide
---

# 交出草稿与记录，下一步仍由本人决定

<div class="pair">
<div>
<div class="label">output/audit-draft.md</div>
<p>依据有编号，事实与推测分开。</p>
<p>留下一个优先补证动作。</p>
</div>
<div>
<div class="label">audit-log.md</div>
<p>核查项 → 原证据 → 更正结果。</p>
<p>写明仍未核实什么。</p>
</div>
</div>

<div class="takeaway">下一节：本人确认一个问题，再把它变成行动卡。</div>

<!--
让学生用1分钟在audit-log.md保存一条核验记录：实际发现何错、原依据、如何更正、哪些仍未知；没发现错误者写已检查范围与待核项，不补造错误。最后1分钟请两人分别说出产物路径和一个未决问题。提醒草稿不是批准书，下一节由本人选择优先补证方向，而非直接接受整体改版建议。来源：讲义305、537—549行。
建议用时：2分钟
-->
