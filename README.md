# video-recreation-skill（VIDEO_AGENT_SKILL V2.2）— 爆款视频二创工作流 + 电商视频提示词模板

[English version](./README.en.md)

> 五级质检 + 人物/商品一致性锚点 + 品牌片尾：一条爆款视频 → 自动拆解/重写/生成/质检 → 可发布的二创成片。
>
> 由 **FrameFlow** 出品。FrameFlow 是 [yimiagent.cn](https://yimiagent.cn/?utm_source=github&utm_medium=repo&utm_campaign=video-recreation-skill) 的产品名，两者是同一个平台。

**电商视频提示词模板见 [prompts/ecommerce-video](./prompts/ecommerce-video/README.md)**：39 个电商品类 × 7 种爆款结构（273 个）+ 6 个通用模板，共 285 个，可直接用于 Seedance、可灵 Kling、万相 Wan、MiniMax 等视频模型。独立仓库：[Yf040528/ecommerce-video-prompts](https://github.com/Yf040528/ecommerce-video-prompts)。

![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-2.2-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Platform](https://img.shields.io/badge/platform-FrameFlow%20(yimiagent.cn)-orange)

---

## 和同类 Skill 的区别

|  | video-recreation-skill（本仓库） | 常见的通用复刻 Skill |
|---|---|---|
| 质检 | 五级质检：脚本 → 图片 → 视频 → 音频 → 成片，失败阻断下游并报失败码 | 多数只给提示词，没有质检关卡和失败码 |
| 人物 / 商品一致性 | 全局人物锚点 + 服装锚点 + 商品锚点，跨镜头强制一致，漂移则质检失败 | 只有“保留关系”原则，没有锚点机制 |
| 品牌片尾 | 原片末尾的品牌 / 店铺 / 关注页自动替换成干净品牌片尾 | 无 |
| 二创档位 | 保守 / 中度 / 大胆三档 + 元素级替换表 | 只有“保留骨架、换外皮”一句话策略 |
| 场景 | 带货、风水 / 民俗、AI 漫剧、产品广告各有专属流程 | 通用，不分场景 |
| 形态 | 厚规范（SKILL + specs + schemas + 提示词模板）+ 网页工作台一键用 | 薄 Skill，或只给提示词、不出成片 |

> 上表“常见的通用复刻 Skill”指 2026-11-07 核对过的同类公开仓库的共性，不是针对某一家的逐项断言。

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

## 不用装，先看效果 / 有问题去哪问

- 网页一键用（零技术门槛）：打开 FrameFlow（[yimiagent.cn](https://yimiagent.cn/?utm_source=github&utm_medium=repo&utm_campaign=video-recreation-skill)），新建「爆款二创」任务，上传参考视频即可。
- 定价与模型：以 [yimiagent.cn/pricing](https://yimiagent.cn/pricing?utm_source=github&utm_medium=repo&utm_campaign=video-recreation-skill) 和 [yimiagent.cn/models](https://yimiagent.cn/models?utm_source=github&utm_medium=repo&utm_campaign=video-recreation-skill) 为准，本仓库不写具体价格。
- 提问：装不上先按上面三路安装逐一试，仍有问题去 [Issues](https://github.com/Yf040528/video-recreation-skill/issues) 或 [Discussions](https://github.com/Yf040528/video-recreation-skill/discussions) 发帖，附上你用的安装方式、参考视频类型、档位和质检失败码。

## 电商视频提示词模板

电商视频提示词模板见 **[prompts/ecommerce-video](./prompts/ecommerce-video/README.md)**。覆盖护肤、彩妆、女装、男装、鞋靴、箱包、零食、生鲜、饮品、母婴、玩具、家居、小家电、数码、运动、宠物等 39 个品类，每个品类都有痛点开场、卖点特写、前后对比、场景种草、开箱上手、达人口播、限时促销 7 种结构。装了本 Skill 的 Agent 会按品类自动选模板并填好你的产品；不想自己拼，在 [FrameFlow 无限画布](https://yimiagent.cn/features/infinite-canvas?utm_source=github&utm_medium=repo&utm_campaign=video-recreation-skill) 的图生视频节点下点「模板」即可直接使用。

## 支持的模型（网页工作台已上线，以 /models 为准）

Skill 本身不绑定模型：它只声明「需要什么能力」，在 FrameFlow 网页工作台里可以用「自动匹配」按能力选模型；通过公开 API 调用时由你指定模型。以下是在 [yimiagent.cn/models](https://yimiagent.cn/models?utm_source=github&utm_medium=repo&utm_campaign=video-recreation-skill) 上 2026-11-07 10:10 核对时已上线的模型（共 22 个），增减以该页为准，本仓库不写具体价格：

- **生视频**：Seedance 2.0 Mini、Seedance 2.0 Fast、Seedance 2.0、Seedance 2.5 Image to Video、Wan 3.0、HappyHorse 1.1 Image-to-Video、MiniMax H3、MiniMax H3 Max
- **生图（分镜关键帧）**：GPT Image 2.5、GPT-Image-2、Gemini-3-Pro-Image（Nano Banana Pro）、Gemini-3.1-Flash-Image（Nano Banana 2）、Nano Banana 2.1、Ideogram 4.5
- **对话 / 分析（拆解、脚本与文本处理）**：GPT-5.6 Sol、GPT-6.1 Sol、doubao-seed-2-1-turbo、doubao-seed-2-1-pro、Qwen3 VL Plus、Qwen3.7 Plus、Gemini 3.8 Flash、Claude Opus 5.5

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

1. 打开 **FrameFlow（[yimiagent.cn](https://yimiagent.cn/?utm_source=github&utm_medium=repo&utm_campaign=video-recreation-skill)）**
2. 新建「爆款二创」任务，上传一条参考视频
3. 选择二创档位（保守 / 中度 / 大胆），填写你的产品与要求
4. 一键生成：拆解 → 脚本 → 关键帧 → 视频 → 质检 → 成片

### 方式二：装进你自己的 Agent（开发者）

本仓库是一套标准 Skill 规范（`SKILL.md` + `specs/` + `schemas/`），任何支持 Skill 的 Agent 平台都可直接加载，**无需登录平台即可离线使用规范本身**：

- **WorkBuddy**：`git clone` 本仓库到 `~/.workbuddy/skills/video-recreation/`
- **Claude / Cursor**：将 `SKILL.md` 内容作为系统提示词或自定义指令导入
- **自定义 Agent**：读取 `specs/` 与 `schemas/` 下的机器可读文件，实现你自己的执行器；生图 / 生视频可接 FrameFlow 公开 API（`https://yimiagent.cn/v1`，用 API Key，文档见 [API 文档](https://yimiagent.cn/api-docs?utm_source=github&utm_medium=repo&utm_campaign=video-recreation-skill)），参考 `executor/router_adapter_yimiagent.py`

## 仓库结构

```
skills/video-recreation-skill/SKILL.md  工作流主规范（从这里开始读）
ARCHITECTURE.md       三层架构：Skill / SVML / 执行
CHANGELOG.md          版本演进历史
specs/                各环节规范（生成、运动、连续性、音频时间轴、视觉质检…）
schemas/              机器可读产物定义（SVML、任务、生成请求、质检结果…）
executor/             参考适配器（FrameFlow 公开 API）与校验工具
tools/                能力声明与 API 映射
prompts/              电商视频提示词模板（39 品类 × 7 结构）
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
- 能力 → FrameFlow 公开 API 的映射在 `tools/router_mapping.yimiagent.json`（适配器：`executor/router_adapter_yimiagent.py`）。
- 本 Skill 是**爆款二创**的权威工作流。后续工作流优化记录在此处与 `CHANGELOG.md`。

阅读顺序：从 `skills/video-recreation-skill/SKILL.md` 开始，按其指引逐步加载 specs 与 schemas。

**V2.2.25（2026-11-09）**：新增 285 个电商视频提示词模板；参考适配器改用 FrameFlow 公开 API（API Key）；移除旧版规则与回归示例。

---

## 关于

本工作流运行在 **FrameFlow（[yimiagent.cn](https://yimiagent.cn/?utm_source=github&utm_medium=repo&utm_campaign=video-recreation-skill)）** —— FrameFlow 是 yimiagent.cn 的产品名，两者是同一个平台。它是一个可视化视频智能体工作台，支持文生图、图生图、图生视频、FFmpeg 剪辑合成，以及电商、AI 漫剧、爆款二创等行业工作流。

## License

[MIT](./LICENSE)

**关键词**：FrameFlow · yimiagent · 电商视频提示词 · 带货视频提示词模板 · 视频二创 · 爆款视频拆解 · AI 视频工作流 · 短视频带货 · 图生视频 · 人物一致性 · 商品锚点 · TikTok 二创 · 抖音二创 · AI 漫剧 · 风水视频 · 民俗短视频 · 视频批量生产 · video recreation skill · short video automation