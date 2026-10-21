# VIDEO RECREATION SKILL V1.8.1

## Execution Patch --- Prompt Compiler + Controlled Batch + Fail-Closed Visual QA

**Version:** V1.8.1\
**Base:** V1.8\
**Purpose:** 爆款参考视频拆解 → SOURCE → GLOBAL MASTER → RECREATED → QA
→ Video Generation\
**核心升级：** V1.8 的规则不再只停留在 Skill 文档；每个正式 RECREATED
必须把规则编译为可直接执行的 Generation Prompt，并在生成后进行真实视觉
QA。

------------------------------------------------------------------------

## 0. V1.8.1 最高优先级规则

``` text
LOCK 1 = SOURCE STRUCTURE LOCK
LOCK 2 = GLOBAL MASTER LOCK
LOCK 3 = CREATIVE DELTA LOCK
LOCK 4 = PRESERVE LOCK
LOCK 5 = EXECUTION PROMPT LOCK
LOCK 6 = OUTPUT ISOLATION LOCK
LOCK 7 = VISUAL QA GATE
```

``` text
SOURCE STRUCTURE LOCK = 保留参考镜头核心功能、动作逻辑、主体关系
GLOBAL MASTER LOCK = 全片重复出现的人物 / 手 / 产品 / 衣服 / 环境风格保持一致
CREATIVE DELTA LOCK = 正式 RECREATED 镜头必须产生明确二创变化
PRESERVE LOCK = 没有授权修改的元素不得擅自改变
EXECUTION PROMPT LOCK = Skill 规则必须被编译进每张正式图片的生成 Prompt
OUTPUT ISOLATION LOCK = 每个 RECREATED 必须是独立图片资产，不得自动拼图
VISUAL QA GATE = 实际生成结果未通过 QA，不得标记 PASS
```

------------------------------------------------------------------------

## 1. GLOBAL MASTER SYSTEM

每个 Job 首先建立：

``` text
PERSON_MASTER
HAND_MASTER
PRODUCT_MASTER
PRODUCT_COMPONENT_BLUEPRINT
CLOTHING_MASTER
ENVIRONMENT_MASTER
STYLE_MASTER
TEXT_MASTER
```

只出现手时：

``` text
HAND_MASTER = ACTIVE
```

锁定： - 肤色 - 手型 - 手指比例 - 指甲长度 - 指甲形状 - 美甲颜色/风格 -
是否出现完整手掌/手臂 - 左手/右手 - 镜头允许出现的手数量

### HAND COUNT LOCK

``` text
AUTHORIZED_HAND_COUNT = N
EXTRA_HANDS = FORBIDDEN
EXTRA_FINGERS = FORBIDDEN
DUPLICATED_LIMBS = FORBIDDEN
```

SOURCE 只有一只手时，除非 Creative Map 明确授权，不得生成第二只手。

------------------------------------------------------------------------

## 2. PRODUCT MASTER 2.1

必须建立：

``` text
PRODUCT_MASTER
PRODUCT_COMPONENT_BLUEPRINT
PRODUCT_REFERENCE
```

产品身份至少包含：

``` text
COLOR
MATERIAL
COMPONENT_SHAPE
COMPONENT_SIZE_RELATION
COMPONENT_COUNT
COMPONENT_ORDER
METAL_COLOR
CHARM / ACCESSORY
OVERALL_STRUCTURE
```

### PRODUCT REPLACEMENT LOCK

若 Job 已指定新产品：

``` text
SOURCE_PRODUCT_IDENTITY = FORBIDDEN
TARGET_PRODUCT_MASTER = REQUIRED
```

任何 RECREATED 镜头中，只要产品可见，就必须使用 TARGET PRODUCT MASTER。

不得因为 SOURCE 中原产品更清晰而回退到 SOURCE_PRODUCT。

------------------------------------------------------------------------

## 3. PRODUCT GEOMETRY + FIT LOCK

``` text
PRODUCT_GEOMETRY_LOCK = TRUE
PRODUCT_FIT_LOCK = TRUE
```

手串必须满足： - 闭合环路正确 - 珠子不融合 - 珠子不复制 -
珠子不拉长/压扁 - 珠子数量和排列不无故变化 - 弹力线/连接关系连续 -
吊坠/金属件连接合理 - 手腕遮挡正确 - 不穿模 - 不悬空 - 不嵌入皮肤 -
佩戴松紧符合物理关系

``` text
PRODUCT_IDENTITY_PASS = TRUE
PRODUCT_GEOMETRY_PASS = TRUE
PRODUCT_FIT_PASS = TRUE
```

三者缺一不可。

------------------------------------------------------------------------

## 4. CLOTHING MASTER 2.1

重复出现的服装必须建立：

``` text
CLOTHING_MASTER_LOCK = TRUE
```

锁定： - 服装类型 - 主颜色 - 材质 - 纹理 - 袖口形态 - 厚薄 -
针织/棉/丝/皮等材料特征

如果 Job 已明确"替换原袖子"：

``` text
SOURCE_CLOTHING = FORBIDDEN
TARGET_CLOTHING_MASTER = REQUIRED
```

后续所有相关镜头不得重新出现 SOURCE 原袖子。

------------------------------------------------------------------------

## 5. REFERENCE ROLE ISOLATION

支持：

``` text
PRODUCT_REFERENCE
PERSON_REFERENCE
HAND_REFERENCE
CLOTHING_REFERENCE
ENVIRONMENT_REFERENCE
STYLE_REFERENCE
SOURCE_REFERENCE
```

每张参考图必须只有明确角色。

例如 PRODUCT_REFERENCE：

``` text
ALLOW:
product identity
product geometry
product color
product material
component layout

FORBID:
person
hand identity
clothing
background
lighting
camera
composition
```

禁止把产品参考图中的无关人物、袖子、背景一起迁移。

------------------------------------------------------------------------

## 6. SOURCE SEMANTIC FUNCTION LOCK

SOURCE 只能来自参考视频真实抽帧。

每个 SOURCE 必须记录：

``` text
video_sha256
timestamp
frame_number
shot_id
SHOT_SEMANTIC_FUNCTION
```

RECREATED 必须保留镜头功能，而不是复制 SOURCE 外观。

例：

``` text
SOURCE FUNCTION:
hand holds bracelet for product reveal

KEEP:
product reveal function
single-hand interaction

CHANGE:
product identity
clothing identity
environment
camera angle
lighting
composition
```

------------------------------------------------------------------------

## 7. CREATIVE DELTA LOCK 2.1

正式 RECREATED：

``` text
MAJOR_CREATIVE_CHANGES >= 2
TARGET = 3
```

可计入： - 环境 - 镜头角度 - 景别 - 构图 - 前景 - 背景 - 灯光设计 -
姿势 - 动作状态 - 道具布局 - 色彩设计 - 景深结构

以下不计入： - 高清化 - 锐化 - 去字幕 - 删除水印 - 轻微调色 - 单纯改文字

------------------------------------------------------------------------

## 8. EXECUTION PROMPT COMPILER（V1.8.1 核心新增）

禁止直接使用笼统提示词：

``` text
“根据 SOURCE 二创”
“换个手串”
“保持一致”
```

每个 RECREATED 必须先生成 `EXECUTION_PROMPT_xx`。

### 标准编译结构

``` text
[OUTPUT CONTRACT]
Generate exactly ONE independent vertical image for RECREATED_xx.
Do not create a collage, contact sheet, split screen, triptych, comparison board or multiple panels.
No labels unless TEXT_POLICY explicitly requires them.

[SOURCE SEMANTIC FUNCTION]
...

[REQUIRED GLOBAL MASTERS]
HAND_MASTER = ...
PRODUCT_MASTER = ...
CLOTHING_MASTER = ...
STYLE_MASTER = ...

[MANDATORY REPLACEMENTS]
SOURCE_PRODUCT = FORBIDDEN / PRESERVE
SOURCE_CLOTHING = FORBIDDEN / PRESERVE
...

[PRESERVE]
...

[CREATIVE DELTA]
1. ...
2. ...
3. ...

[ANATOMY / OBJECT COUNT]
AUTHORIZED_HAND_COUNT = ...
EXTRA_HANDS = FORBIDDEN
EXTRA_FINGERS = FORBIDDEN
EXTRA_PRODUCTS = FORBIDDEN

[PRODUCT GEOMETRY]
...

[NEGATIVE CONSTRAINTS]
Do not restore source product.
Do not restore source clothing.
Do not invent another hand.
Do not duplicate jewelry.
Do not fuse beads.
Do not alter product component order.
Do not create text unless authorized.

[FINAL OUTPUT]
ONE image only.
RECREATED_xx only.
```

Generation Prompt 必须明确写出"必须出现什么"和"绝对不能出现什么"。

------------------------------------------------------------------------

## 9. MANDATORY REPLACEMENT DECLARATION

每个 Task Manifest 增加：

``` text
REPLACEMENT_MATRIX
```

示例：

``` text
PRODUCT:
SOURCE = original five-elements bracelet
TARGET = PRODUCT_MASTER_A
ACTION = REPLACE
SOURCE_REAPPEARANCE = FORBIDDEN

CLOTHING:
SOURCE = red knitted sleeve
TARGET = CLOTHING_MASTER_A
ACTION = REPLACE
SOURCE_REAPPEARANCE = FORBIDDEN

HAND:
SOURCE = single manicured female hand
TARGET = HAND_MASTER_A
ACTION = PRESERVE_IDENTITY / ADAPT_POSE
AUTHORIZED_HAND_COUNT = 1
```

只要 `ACTION = REPLACE`，原元素就自动加入 Negative Constraints。

------------------------------------------------------------------------

## 10. TWO GENERATION MODES

### MODE A --- PRECISION_EDIT

用于： - 只替换产品 - 只替换袖子 - 去字幕 - 保持其他不变

``` text
CREATIVE_DELTA_LOCK = OFF
PRESERVE_LOCK = MAXIMUM
```

### MODE B --- RECREATED_SHOT

用于： - 二创 - RECREATED - 重新创作

``` text
GLOBAL_MASTER_LOCK = ON
CREATIVE_DELTA_LOCK = ON
PRESERVE_SEMANTIC_FUNCTION = ON
EXECUTION_PROMPT_LOCK = ON
```

不得混淆。

------------------------------------------------------------------------

## 11. SINGLE GENERATION 与 CONTROLLED BATCH

V1.8 的"一张一张生成"升级为：

``` text
ONE SOURCE → ONE TASK MANIFEST → ONE EXECUTION PROMPT → ONE OUTPUT ASSET
```

这不等于用户必须一次只生成一张。

### 允许：CONTROLLED BATCH

用户可以一次要求：

``` text
RECREATED_01
RECREATED_02
RECREATED_03
...
```

系统可以一次提交多个任务，甚至并行执行，但内部必须拆成独立 Generation
Unit：

``` text
TASK_01 → PROMPT_01 → OUTPUT_01 → QA_01
TASK_02 → PROMPT_02 → OUTPUT_02 → QA_02
TASK_03 → PROMPT_03 → OUTPUT_03 → QA_03
```

### 禁止：COMPOSITE BATCH

禁止：

``` text
一个大 Prompt
→ 让模型在同一张画布生成 01/02/03
→ triptych / collage / contact sheet
```

原因：这会削弱 PRODUCT / CLOTHING / HAND / GEOMETRY
的独立控制，并容易发生跨面板污染。

### BATCH CONSISTENCY SNAPSHOT

批量开始前冻结：

``` text
BATCH_MASTER_SNAPSHOT
```

包含：

``` text
HAND_MASTER_VERSION
PRODUCT_MASTER_VERSION
CLOTHING_MASTER_VERSION
ENVIRONMENT_MASTER_VERSION
STYLE_MASTER_VERSION
```

整个 Batch 不允许静默改变 Master。

------------------------------------------------------------------------

## 12. BATCH EXECUTION POLICY

### SAFE_BATCH

当以下条件成立，可并行生成多张：

``` text
GLOBAL_MASTER_APPROVED = TRUE
TASK_MANIFEST_COMPLETE = TRUE
REFERENCE_ROLES_VALID = TRUE
EACH_OUTPUT_ISOLATED = TRUE
```

推荐：

``` text
BATCH_SIZE = 2–4 independent images
```

这只是执行效率建议，不是视觉拼图。

### STRICT_SEQUENTIAL

以下情况自动降级为逐张：

``` text
PRODUCT_MASTER 尚未稳定
首次建立新手串
首次建立新人物/手
复杂佩戴关系
上一镜头出现产品变形
上一镜头出现服装漂移
上一镜头出现多手/多指
连续 QA 失败
```

先把 Master 锁稳，再恢复 Controlled Batch。

------------------------------------------------------------------------

## 13. VISUAL QA GATE（V1.8.1 核心新增）

生成完成后必须检查实际图片，而不是只检查 Prompt。

### QA A --- PRODUCT

``` text
PRODUCT_IDENTITY
PRODUCT_COLOR
PRODUCT_MATERIAL
PRODUCT_COMPONENTS
PRODUCT_ORDER
PRODUCT_GEOMETRY
PRODUCT_FIT
PRODUCT_ACCESSORIES
```

### QA B --- HAND / PERSON

``` text
HAND_COUNT
FINGER_COUNT
HAND_IDENTITY
SKIN_TONE
NAIL_STYLE
LIMB_ANATOMY
```

### QA C --- CLOTHING

``` text
CLOTHING_IDENTITY
COLOR
MATERIAL
TEXTURE
CUFF_SHAPE
SOURCE_CLOTHING_REAPPEARANCE
```

### QA D --- CREATIVE

``` text
creative_delta_count >= 2
```

### QA E --- OUTPUT

``` text
ONE_IMAGE_ONLY
NO_COLLAGE
NO_UNAUTHORIZED_TEXT
NO_EXTRA_OBJECTS
```

------------------------------------------------------------------------

## 14. QA FAIL → TARGETED REGENERATION

禁止失败后重新写一个完全不同的 Prompt。

失败时保留原 Task Manifest，只追加针对失败项的修复约束。

例如：

``` text
FAIL_EXTRA_HAND
→ ADD:
Exactly one visible human hand.
No second hand.
No detached fingers.
No background hand.

FAIL_SOURCE_PRODUCT_REAPPEARANCE
→ ADD:
The source bracelet is prohibited.
Use PRODUCT_MASTER_A exclusively.

FAIL_CLOTHING_CONSISTENCY
→ ADD:
Use CLOTHING_MASTER_A exclusively.
The original red sleeve must not appear.

FAIL_PRODUCT_GEOMETRY
→ ADD:
Preserve exact component blueprint and closed-loop bracelet geometry.
```

然后只重生成失败镜头。

------------------------------------------------------------------------

## 15. FAIL-CLOSED PRODUCTION

``` text
GENERATE
↓
VISUAL QA
↓
PASS?
├─ NO  → REGENERATE CURRENT TASK
└─ YES → APPROVE ASSET
```

Controlled Batch 中：

``` text
01 PASS
02 FAIL
03 PASS
```

只重做 02，不需要重做 01/03。

但若发现：

``` text
MASTER_DEFINITION_ERROR
```

则停止 Batch，修正 Master，并重新检查所有受影响资产。

------------------------------------------------------------------------

## 16. CONTEXT DRIFT KILL SWITCH

发现以下任一情况：

``` text
wrong product
source product returns
wrong sleeve
source sleeve returns
extra hand
wrong person
unrelated environment
cross-job contamination
duplicated jewelry
```

执行：

``` text
STOP_AFFECTED_TASK
CONTEXT_DRIFT_DETECTED
DO_NOT APPROVE
```

------------------------------------------------------------------------

## 17. RECREATED TASK MANIFEST V1.8.1

每张正式图片必须有：

``` text
TASK_ID
JOB_ID
SOURCE_ID
MODE

SOURCE_SEMANTIC_FUNCTION

PERSON_MASTER
HAND_MASTER
AUTHORIZED_HAND_COUNT
PRODUCT_MASTER
PRODUCT_COMPONENT_BLUEPRINT
CLOTHING_MASTER
ENVIRONMENT_MASTER
STYLE_MASTER

REFERENCE_ROLE_MANIFEST
REPLACEMENT_MATRIX

EDITABLE_ELEMENTS
PRESERVE_ELEMENTS
CREATIVE_DELTA

PRODUCT_GEOMETRY_LOCK
PRODUCT_FIT_LOCK
TEXT_POLICY

NEGATIVE_CONSTRAINTS
OUTPUT_CONTRACT
EXECUTION_PROMPT

QA_REQUIREMENTS
```

缺失：

``` text
STOP_TASK_MANIFEST_INCOMPLETE
```

------------------------------------------------------------------------

## 18. GENERATION GATE V1.8.1

正式生成前必须：

``` text
SOURCE_BOUND = TRUE
JOB_ID_VALID = TRUE
GLOBAL_MASTER_VALID = TRUE
TASK_MANIFEST_VALID = TRUE
MODE_VALID = TRUE
EXECUTION_PROMPT_COMPILED = TRUE
OUTPUT_ISOLATION_VALID = TRUE
```

否则：

``` text
GENERATION_DENIED
```

------------------------------------------------------------------------

## 19. COMPLETE EXECUTION CHAIN

``` text
INGEST REFERENCE VIDEO
→ HASH + VIDEO IDENTITY
→ COMPLETE SHOT DETECTION
→ SOURCE EXTRACTION
→ SOURCE PROOF
→ SELECT KEYFRAMES

→ BUILD GLOBAL MASTER
→ BUILD PRODUCT COMPONENT BLUEPRINT
→ BUILD REFERENCE ROLE MANIFEST
→ APPROVE MASTER

→ BUILD CREATIVE MAP
→ BUILD TASK MANIFESTS
→ BUILD REPLACEMENT MATRIX
→ COMPILE EXECUTION PROMPT PER TASK

→ FREEZE BATCH_MASTER_SNAPSHOT

→ GENERATE INDEPENDENT OUTPUT(S)
   ├─ SINGLE
   └─ CONTROLLED BATCH

→ VISUAL QA PER OUTPUT
   ├─ PRODUCT
   ├─ GEOMETRY / FIT
   ├─ HAND / PERSON
   ├─ CLOTHING
   ├─ CREATIVE DELTA
   ├─ PRESERVE
   └─ OUTPUT ISOLATION

→ FAIL = TARGETED REGENERATION
→ PASS = APPROVE

→ ALL PASS
→ COMPARISON BOARD
→ VIDEO GENERATION PACKAGE
```

------------------------------------------------------------------------

## 20. CORE FAIL CODES V1.8.1

``` text
FAIL_PRODUCT_IDENTITY
FAIL_PRODUCT_COMPONENT
FAIL_PRODUCT_COLOR
FAIL_PRODUCT_GEOMETRY
FAIL_PRODUCT_FIT

FAIL_SOURCE_PRODUCT_REAPPEARANCE

FAIL_PERSON_CONSISTENCY
FAIL_HAND_CONSISTENCY
FAIL_EXTRA_HAND
FAIL_EXTRA_FINGER
FAIL_ANATOMY

FAIL_CLOTHING_CONSISTENCY
FAIL_SOURCE_CLOTHING_REAPPEARANCE

FAIL_PRESERVE_MASK
FAIL_UNAUTHORIZED_CHANGE

FAIL_INSUFFICIENT_CREATIVE_DELTA
FAIL_SCENE_REPETITION

FAIL_OUTPUT_ISOLATION
FAIL_COLLAGE_OUTPUT
FAIL_UNAUTHORIZED_TEXT

FAIL_SOURCE_BINDING
FAIL_REFERENCE_ROLE
FAIL_EXECUTION_PROMPT
CONTEXT_DRIFT_DETECTED
```

------------------------------------------------------------------------

## 21. UNIVERSAL EXECUTION RULE

``` text
VIDEO RECREATION SKILL V1.8.1 — UNIVERSAL EXECUTION RULE

Do not rely on the image model to infer the Skill.

Compile every formal RECREATED task into an explicit execution prompt.

Every recurring product, hand/person and clothing identity must come from
the approved GLOBAL MASTER, not from whichever source image is visually strongest.

If an element is marked REPLACE, the source version of that element becomes
explicitly forbidden in the generated output.

Each SOURCE maps to one independent TASK, one independent EXECUTION PROMPT,
and one independent OUTPUT ASSET.

Multiple TASKS may be submitted together as a CONTROLLED BATCH,
but they must never be collapsed into one collage, triptych, contact sheet
or multi-panel generation.

Freeze the same MASTER snapshot across the batch.

Explicitly constrain hand count, product count, clothing identity,
product geometry and product fit.

Inspect the actual generated image after generation.

A prompt that looks correct is not a PASS.
Only the visual output can PASS QA.

If one task fails, regenerate that task only.
If the Master itself is wrong, stop the batch and repair the Master.

FAIL CLOSED.
```

------------------------------------------------------------------------

## 22. FINAL PRINCIPLE

``` text
该统一的必须统一。
该替换的必须真正替换。
被替换的 SOURCE 元素不得偷偷回来。
该二创的必须明显二创。
未授权修改的必须 PRESERVE。
一张 SOURCE 对应一个独立输出资产。
可以一次批量提交多张，但绝不允许合成一张拼图。
Prompt 必须执行 Skill，而不是让模型自己猜 Skill。
QA 必须检查真实输出，而不是检查文字。
失败只修失败镜头。
MASTER 错误才停止整批。
```

------------------------------------------------------------------------

## 23. V1.8 → V1.8.1 的本质变化

V1.8 解决的是：

``` text
WHAT TO LOCK
WHAT TO CHANGE
WHAT TO PRESERVE
WHAT TO QA
```

V1.8.1 新增解决：

``` text
HOW TO COMPILE RULES INTO GENERATION PROMPTS
HOW TO GENERATE MULTIPLE SHOTS WITHOUT COLLAPSING THEM INTO A COLLAGE
HOW TO PREVENT SOURCE PRODUCT / CLOTHING FROM RETURNING
HOW TO PREVENT EXTRA HANDS
HOW TO QA THE ACTUAL IMAGE
HOW TO REGENERATE ONLY THE FAILED TASK
```

因此 V1.8.1 不再要求"用户一次只能叫一张"。

正确含义是：

``` text
一次可以要求多张；
系统内部必须独立任务、独立 Prompt、独立图片、独立 QA；
共享同一个冻结的 GLOBAL MASTER。
```
