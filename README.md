# VIDEO_AGENT_SKILL V2.2 — 爆款视频二创工作流

> 一条爆款视频 → 自动拆解/重写/生成/质检 → 可发布的二创成片。

![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-2.2-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Platform](https://img.shields.io/badge/platform-www.yimiagent.cn-orange)

---

## 安装（30 秒）

### 方式一：Claude Code 插件（推荐）

```
/plugin marketplace add Yf040528/video-recreation-skill
/plugin install video-recreation@video-recreation-skills
```

装完在 Claude Code 里直接说“做一条爆款二创”即可触发。

### 方式二：通用 Skill 安装

```
npx skills add Yf040528/video-recreation-skill
```

如提示选择 Skill，选 `video-recreation-skill`。

### 方式三：手动复制

把 `skills/video-recreation-skill` 整个文件夹复制到你所用 Agent 的 skills 目录（Claude Code：`~/.claude/skills/`），或把 `skills/video-recreation-skill/SKILL.md` 内容作为自定义指令导入。

## 这是什么

这是一个面向中文短视频创作的**二创（recreation）工作流规范**。它把「看到一条爆款视频，想做出自己的版本」这件事，拆成了机器可执行的步骤：拆解原片 → 重写脚本 → 生成分镜关键帧 → 图生视频 → 视觉质检 → 剪辑合成。

适用场景：

- **带货短视频**：产品图 + 参考爆款 → 保留卖点结构，替换成你自己的产品、人物和场景
- **风水 / 民俗 / 传统文化内容**：寺庙、本命年、祈福等题材的结构化二创
- **AI 漫剧**：角色一致性控制、分镜规划、台词与口型
- **产品广告**：商品锚点锁定，保证多镜头之间产品外观不漂移

## 解决的核心痛点

| 痛点 | 这个工作流怎么处理 |
|---|---|
| AI 生图人物换一张就变脸 | 全局人物锚点 + 服装锚点，跨镜头强制一致，漂移则质检失败 |
| 产品每个镜头长得不一样 | 商品锚点图片锁定，生成时自动附加产品参考 |
| 二创出来跟原片一模一样 | 三档策略：保守（完整复刻）/ 中度（同风格换实例）/ 大胆（重写） |
| 口型对不上 | 声音随画面原生生成，台词按时长分配到对应镜头 |
| 原片带抖音搜索页、品牌卡片 | 自动识别并替换成干净的品牌片尾 |
| 改了一个镜头的提示词，别的没跟着改 | 人工编辑优先级最高，可一键同步到全片 |

## 三档二创策略

- **保守（conservative）** — 完整复刻原片结构、风格、镜头语言，仅做细微同义词替换
- **中度（medium）** — 锁定结构与风格（配色、题材、象征物），只替换同类别、同色系的实例
- **大胆（bold）** — 每个镜头的卖点与功能保留，画面与文案全面重写

## 快速开始

### 方式一：网页一键用（零技术门槛）

1. 打开 **[www.yimiagent.cn](https://www.yimiagent.cn)**
2. 新建「爆款二创」任务，上传一条参考视频
3. 选择二创档位（保守 / 中度 / 大胆），填写你的产品与要求
4. 一键生成：拆解 → 脚本 → 关键帧 → 视频 → 质检 → 成片

### 方式二：装进你自己的 Agent（开发者）

本仓库是一套标准 Skill 规范（`SKILL.md` + `specs/` + `schemas/`），任何支持 Skill 的 Agent 平台都可直接加载，**无需登录平台即可离线使用规范本身**：

- **WorkBuddy**：`git clone` 本仓库到 `~/.workbuddy/skills/video-recreation/`
- **Claude / Cursor**：将 `SKILL.md` 内容作为系统提示词或自定义指令导入
- **自定义 Agent**：读取 `specs/` 与 `schemas/` 下的机器可读文件，实现你自己的执行器（参考 `executor/router_adapter_yimiagent.py`）

## 仓库结构

```
skills/video-recreation-skill/SKILL.md  工作流主规范（从这里开始读）
ARCHITECTURE.md       三层架构：Skill / SVML / 执行
CHANGELOG.md          版本演进历史
specs/                各环节规范（生成、运动、连续性、音频时间轴、视觉质检…）
schemas/              机器可读产物定义（SVML、任务、生成请求、质检结果…）
executor/             参考执行器与上游路由适配
tools/                能力声明与路由映射
resources/            V1.8.1 历史规则
```

## 设计原则

- **不绑定模型**：Skill 只声明「需要什么能力」，由上游智能路由决定用哪个模型、如何容灾
- **规范优于散文**：执行器读取 `specs/recreation_policy.json` 等机器可读文件，不依赖自然语言描述
- **人工编辑最高优先**：用户手写的提示词与参考图覆盖一切自动规则
- **失败要暴露**：质检不过就报告具体失败码，不静默跳过

---

## 版本说明

V2.2 强化了完整的二创管线：原片镜头切分 + ASR/OCR/音频分析；带**关键帧与运动**的原片分镜；二创脚本/分镜；全局人物·风格·商品锚点；逐镜头生图与质检/编辑；基于已确认图 + 提示词 + 原片运动 + 音频时序的视频生成；视频质检；原生音频（对白/音效/BGM）；FFmpeg 合成；终检；带版本号的逐镜头素材包；依赖感知的局部重生成；合规与转换审查。

**架构升级**：引入三层分离（Skill / SVML / 执行）、词级语义锚定与时间轴重排、能力插件注册。详见 `ARCHITECTURE.md`、`specs/WORD_ANCHOR_SPEC.md`、`plugins/PLUGIN_SPEC.md`。

**V2.2.1（2026-10-04）**
- 声音（对白、音效、BGM）在「图生视频」步骤原生生成。FFmpeg 只负责剪辑：转场、字幕、调色、卡点。
- 能力 → 服务端路由的映射在 `tools/router_mapping.yimiagent.json`（适配器：`executor/router_adapter_yimiagent.py`）。
- V1 执行器文件在 `resources/legacy_v1/` 与 `executor/`。
- 本 Skill 是**爆款二创**的权威工作流。后续工作流优化记录在此处与 `CHANGELOG.md`。

阅读顺序：从 `skills/video-recreation-skill/SKILL.md` 开始，按其指引逐步加载 specs 与 schemas。V1.8.1 历史规则保留在仓库中，用于兼容性参考。

---

## 关于

本工作流运行在 **[www.yimiagent.cn](https://www.yimiagent.cn)** —— 一个可视化视频智能体工作台，支持文生图、图生图、图生视频、FFmpeg 剪辑合成，以及电商、AI 漫剧、爆款二创等行业工作流。

## License

[MIT](./LICENSE)

**关键词**：视频二创 · 爆款视频拆解 · AI 视频工作流 · 短视频带货 · 图生视频 · 人物一致性 · 商品锚点 · TikTok 二创 · 抖音二创 · AI 漫剧 · 风水视频 · 民俗短视频 · 视频批量生产 · video recreation skill · short video automation
