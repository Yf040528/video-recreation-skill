# VIDEO AGENT EXECUTOR V1

这不是新的 Skill，而是 V1.8.1 的执行器。

## V1 的核心修正

1. `GLOBAL_MASTER` 只定义“元素出现时必须是谁”。
2. 新增 `PRESENCE_MAP` 定义“这个镜头到底应不应该出现该元素”。
3. 每个 SOURCE 永远是独立 Task / Prompt / Output。
4. 禁止任何 Task 要求生成多张图、拼图、triptych/contact sheet。
5. QA 使用 fail-closed：存在输出 ≠ PASS。
6. 失败镜头进入 `retry_queue.json`；通过的镜头不重做。
7. 如果 Generator/视觉 QA 没真正接入，Executor 明确停在 WAITING 状态，不假装已经自动完成。

## 本次手串回归测试应有的 Presence Map

- RECREATED_01: HAND=YES, PRODUCT=YES, CLOTHING=NO, TEMPLE=NO
- RECREATED_02: HAND=NO, PRODUCT=NO, CLOTHING=NO, TEMPLE=YES
- RECREATED_03: HAND=YES, PRODUCT=YES, CLOTHING=YES, TEMPLE=NO

这意味着：
- 02 不允许因为 PRODUCT_MASTER 存在就凭空出现手串。
- 02 不允许出现手。
- 01 没有袖子时，不强行塞入 CLOTHING_MASTER。
- 03 袖子出现时，才使用 CLOTHING_MASTER。

## 快速运行

```bash
python3 video_agent_executor.py validate jobs/bracelet_regression/job.json
python3 video_agent_executor.py build jobs/bracelet_regression/job.json
python3 video_agent_executor.py queue jobs/bracelet_regression/job.json
python3 video_agent_executor.py qa jobs/bracelet_regression/job.json
```

`build` 会生成每个镜头独立的 task JSON 和 prompt TXT。
`queue` 会生成 generation_queue.json，每一项只能对应 ONE OUTPUT ASSET。
`qa` 会读取 qa/*.json。没有真实视觉审核结果时不会宣称 PASS。

## 真正自动闭环还需要什么

需要给 `src/adapters.py` 接入你实际使用的：
- Image Generator adapter
- Vision QA adapter

V1 已经把接口固定好；接入后无需再改 Skill 架构。

## 最重要的约束

`MASTER != PRESENCE`

Master 解决身份一致性。
Presence Map 解决是否出现。
两者必须同时满足。
