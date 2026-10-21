---
name: video-recreation-skill
description: Recreate viral short videos (TikTok / 抖音 — 风水, 民俗, 带货, product ads) for Chinese e-commerce and AI comic/drama channels. Turns one reference video into a recreated script, storyboard keyframes, image-to-video clips and a finished FFmpeg cut, with character and product continuity locks, per-shot visual QA, targeted retry, and an automatic brand end card. Use when deconstructing a competitor video, planning a recreation, keeping a person or product consistent across shots, or when someone asks how to make a 爆款二创 video. Runs on the visual production workspace at www.yimiagent.cn.
version: 2.2.22
---

# Video Agent Director Skill

## Product surface
This Skill powers a **visual video-agent workflow** that users can operate through **www.yimiagent.cn**. It is designed as a visual production workspace in which users can move from creative intent and source materials to analysis, generation, editing, assembly, QA, and delivery.

### Core creation capabilities
- **Text-to-image (文生图)** generation.
- **Image-to-image (图生图)** generation, editing, replacement, and controlled recreation.
- **Image-to-video (图生视频)** generation from approved keyframes, product images, characters, environments, and other visual references.
- **FFmpeg editing and assembly (FFmpeg 剪辑合成)** for the final edit only: clip assembly/trimming, **transitions (转场)**, **subtitles (字幕)**, **colour grading (调色)**, **beat-sync cuts (卡点)**, loudness normalisation and final-output packaging. FFmpeg is treated as a deterministic media-processing capability, not as a generative model. Since V2.2.1 it does **not** create voice, SFX or music.

### Industry solution workflows
The visual Agent can orchestrate reusable industry workflows, including but not limited to:

- **E-commerce video production (电商)** — product/reference analysis, selling-point extraction, shot planning, product and visual consistency control, keyframe generation, image-to-video generation, QA, editing, and final assembly.
- **AI comic/drama production (AI 漫剧)** — story and episode planning, character/environment continuity, storyboard and shot design, keyframe generation, image-to-video production, dialogue/subtitle/audio planning, QA, and assembly.
- **Viral-video creative recreation (爆款二创)** — reference-video deconstruction, semantic shot analysis, reusable structure extraction, creative-delta planning, recreated storyboard/keyframes, consistency control, generation, QA, targeted retry, and final assembly.

### Visual creative workspace
The user-facing workflow may expose these capabilities as connected visual stages rather than isolated model calls:

- **Storyboard/script analysis and deconstruction (分镜脚本分析拆解)** — analyze reference videos, images, scripts, timing, shots, camera language, subjects, products, motion, audio, subtitles, hooks, pacing, CTA, and other production semantics, then express the result as structured SVML where applicable.
- **AI-assisted writing (AI 帮写)** — assist with concepts, scripts, shot descriptions, narration, dialogue, subtitles, hooks, CTAs, generation instructions, and production-ready revisions while preserving structured production constraints.
- **Canvas workflow (画布功能)** — provide a visual workspace for organizing source assets, analysis, storyboard/shot nodes, generated keyframes, video segments, QA states, retries, editing/assembly stages, and final outputs. The canvas is a presentation and orchestration surface; machine-readable state remains governed by SVML, task contracts, and JSON Schemas.

The Skill remains provider- and model-agnostic: generative and analytical capabilities are expressed as capability requests and fulfilled by the **upstream intelligent router**. The website is the visual interaction and workflow surface; this Skill is the director, planning, structured-production, continuity, execution-contract, QA, retry, and media-assembly layer behind it.

## Mission
Act as a director and production controller, not as a single prompt writer. Convert creative intent and references into a deterministic production plan, preserve required identities/continuity, enforce creative transformation, generate independent assets, inspect results, and retry only failed assets.

## Architecture — canonical V2.2
This package deliberately separates three layers so rules can grow without destabilizing execution:

1. **Knowledge / Skill layer** — `SKILL.md`, domain specs, industry playbooks, QA policy. It explains how the director should reason and what production invariants matter.
2. **Language / IR layer** — stable SVML + JSON Schemas. It is the machine-readable contract between reasoning and execution. Skill changes must compile into this layer rather than leaking free-form rules into executors.
3. **Execution layer** — deterministic executor/compiler/validator plus registered capability plugins. It executes validated SVML and MUST NOT contain creative/domain policy that belongs in Skill.

Concrete model/provider integrations are plugins behind the upstream router. Adding or replacing a model must not require edits to SVML or core Skill semantics.

## Word-level anchoring
Dialogue and narration use stable **word/token anchors** as the primary semantic attachment points for subtitles, SFX, visual events, cuts, emphasis, lip-sync cues, beat cues, and other synchronized events. Absolute timecodes are compiled outputs, not the primary authoring identity. When wording or speech timing changes, the compiler reflows dependent events and regenerates derived timecodes. See `specs/WORD_ANCHOR_SPEC.md` and `schemas/word_anchor_timeline.schema.json`.

## Production workflow — canonical V2.2
The default visual workflow is:

`SOURCE VIDEO → COMPLIANCE PRECHECK → SHOT SPLIT + ASR + OCR + AUDIO STEMS → SOURCE STORYBOARD (keyframes + motion + dialogue/SFX/BGM) → HUMAN STRUCTURE CONFIRMATION → RECREATED SCRIPT + RECREATED STORYBOARD → GLOBAL IDENTITY/STYLE/PRODUCT LOCK → PER-SHOT RECREATED IMAGE → IMAGE QA/EDIT → PER-SHOT VIDEO WITH NATIVE AUDIO (approved image + prompt + source-motion reference + dialogue/SFX/BGM plan, generated audio-visually in sync) → VIDEO+AUDIO QA/EDIT → FFMPEG FINAL EDIT (transitions + subtitles + colour grading + beat-sync) → FINAL QA → MULTI-VERSION EXPORT + RELEASE COMPLIANCE CHECK`

### Three strengthened production contracts
1. **Recreated image** = source keyframe semantic/composition reference + recreated prompt + global consistency anchors. Never generate recurring characters/products/styles as unrelated independent images.
2. **Recreated video** = approved recreated image + shot prompt + original/source motion reference + first/last-frame or trajectory controls when supported + **the shot's audio plan (dialogue/narration lines, voice identity, SFX cues, BGM mood/beat) generated natively with the picture**. A keyframe alone is not a motion specification, and the video step is where sound is created.
3. **Final film** = layered QA + per-shot versioned asset packages + dependency-aware regeneration + compliance/transformation review.

### Layered QA gates
QA is mandatory at five levels: **script QA → image QA → video QA → audio QA → final-film QA**. A failed gate blocks dependent downstream work unless explicitly overridden by an authorized human review.

## Progressive disclosure
Load only what the current stage requires:

1. **Planning / deconstruction / shot design** → read `specs/SVML_SPEC.md`.
2. **Reference roles, identity, product/clothing continuity** → read `specs/REFERENCE_SPEC.md` and `specs/CONTINUITY_SPEC.md`.
3. **Motion reconstruction / video generation** → read `specs/MOTION_SPEC.md`, `specs/GENERATION_SPEC.md`, and `schemas/motion_reference.schema.json`.
4. **Dialogue, native video audio, lip sync, SFX, BGM, subtitle timing** → read `specs/WORD_ANCHOR_SPEC.md`, `specs/AUDIO_TIMELINE_SPEC.md`, `schemas/word_anchor_timeline.schema.json`, and `schemas/audio_timeline.schema.json`.
5. **Plugin/capability resolution** → read `plugins/PLUGIN_SPEC.md`, `plugins/registry.json`, and `schemas/plugin_manifest.schema.json`.
6. **Generation request or prompt compilation** → read `specs/GENERATION_SPEC.md`, `tools/TOOL_SPEC.md`, and the relevant schemas.
7. **QA or retry** → read `specs/VISUAL_QA_SPEC.md` and `schemas/qa_result.schema.json`.
8. **Versioning / partial regeneration** → read `specs/ASSET_DEPENDENCY_SPEC.md` and `schemas/shot_asset_package.schema.json`.
9. **Recreation compliance / transformation review** → read `specs/COMPLIANCE_TRANSFORMATION_SPEC.md`.
10. **Legacy recreation constraints** → read `resources/VIDEO_RECREATION_SKILL_V1.8.1.md` only when a recreation task needs the detailed V1.8.1 rules.

Do not load every resource by default.

## Audio-in-generation rule (V2.2.1)
Image-to-video models generate sound well, so sound is produced **together with the picture**:

- **Image-to-video stage (图生视频)** — every video request carries the shot's audio plan and requests native audio (`requirements.native_audio = true`): dialogue/narration lines (quoted text that fits the segment duration, roughly 4 Chinese characters per second), voice identity, SFX cues tied to on-screen actions, and BGM mood/genre/beat (instrumental, no sung vocals, newly composed rather than copied from the source). No burned-in subtitles in the generated picture. If the source is completely silent, generate a silent clip.
- **FFmpeg stage (剪辑合成)** — final edit only: trim/assemble, **sound continuity (声音衔接)** (every segment levelled to the same loudness, ±10 dB max, near-silent segments not boosted; 30 ms fades at every join to remove pops; audio crossfades together with picture transitions), **transitions** (from the storyboard's transition field or the user's request; video crossfade plus audio crossfade), **subtitles** (text from the script/user, timed to the speech actually present in each segment as detected by ASR; **subtitle style rules (V2.2.7)**: no full stop (。/．/.) at the end of any subtitle line — a full stop between two sentences in one line becomes a space, while ？！ and ellipses are kept; fixed subtitle style (V2.2.8) — reference 1080×1920: 思源黑体 Bold (Noto Sans CJK SC Bold) 54 px, white text, black outline 3, shadow 1, bottom-centre (ASS `Alignment=2`), `MarginV=300`, `MarginL/R=60`; other resolutions scale size/outline/side margins by the short side ÷ 1080 and MarginV by height ÷ 1920; lines wrap inside the side margins (bottom-left stays clear for the platform account, watermark and buttons; never closer than 250 px to the bottom); ASR stock hallucinations on music-only audio — 请点赞 / 订阅 / 转发 / 打赏 / 感谢观看 / 字幕由…提供 — are never used as subtitles; the user can switch automatic dialogue subtitles off), **colour grading** (light unifying grade by default, or a named look), **beat-sync** (cut points snapped to strong onsets of the segment's own music or of user-supplied music, never cutting through a spoken line), and loudness normalisation. FFmpeg must not add TTS voice, generated BGM or synthetic SFX. User-supplied music on the canvas may be layered as an explicit user choice.
- **QA** — video QA now also checks the generated audio (line intelligibility, voice continuity, lip sync, SFX timing, music presence/absence as planned). A missing audio track when audio was planned is reported, not hidden.

## Industry workflow logic (V2.2.1)
- **User-prompt-only rule (V2.2.3)** — 漫剧创作 and 图生视频 create from scratch strictly from the user's own prompt. Nothing the user didn't ask for is added: no invented dialogue/voice-over, no AI captions or subtitles, no colour grade, no beat-sync, no transitions, no BGM instructions. Only 爆款二创 imitates a source, and even there, subtitles or speech absent from the source are never added.
- **AI comic/drama (漫剧创作)** — AI-assisted brief (its 声音要点 lists only sound the user mentioned) → keyframe image → image-to-video with native audio → automatic final output that only applies what the user asked for (subtitles only if requested).
- **Image-to-video (图生视频)** — 音画同步 is on by default; long prompts are split into chained segments (each continues from the previous last frame) → automatic final output under the same user-prompt-only rule.
- **Viral recreation (爆款二创)** — follows the canonical workflow above. Each segment's video prompt is compiled from SVML plus an audio block (rewritten voice-over lines, source-like SFX, source-like but newly composed BGM). The final edit mirrors the source shot timing, keeps source-style transitions, aligns subtitles to the spoken lines and places recreated on-screen text at the source text position.
- **Edit plan (剪辑方案, V2.2.6)** — For edit-only and canvas edits, an analysis model first turns the user's editing brief or script into a structured plan: per-cut transitions with durations, numeric grade parameters (brightness / contrast / saturation / temperature / tint / highlights / shadows / sharpen / grain / vignette), shot-level subtitles, output spec (size / fps / bitrate), target duration with last-frame hold, explicit beat-sync. FFmpeg executes the plan deterministically. Requests that need media we don't have (SFX, music files) are listed as "未执行", never silently skipped or invented. Without a plan, edit-only uses professional defaults: a short dissolve, light unified grade, sound continuity.
- **Standard edit defaults (V2.2.7)** — users who don't understand editing parameters get a standardised result; users who do can adjust from these values in the plan dialog. Output: portrait 1080×1920 (landscape sources 1920×1080), 30 fps, constant quality CRF 18 (x264 preset medium). A user-specified bitrate never goes below the quality floor (≈8 Mbps at 1080×1920·30 fps, scaled by pixels × fps). Grade: light unified grade = contrast 3, saturation 5, light luma-only sharpen (unsharp 0.4). Parameter mapping follows common editors (brightness 2 → +0.02, contrast 7 → ×1.07, sharpen 33 ≈ unsharp 0.5, vignette 50 ≈ PI/6). Transitions: 0.6 s dissolve. Empty fields mean "not specified" (an empty total duration follows the material; it is never clamped to 1 s). Subtitles follow the fixed subtitle style above.
- **中度 recreation = structure lock + style & motif lock (V2.2.9)** — 中度 keeps the source's structure **and** its style: main palette (same colour family, e.g. red stays red, gold stays gold), theme and scene category (a red-walled temple stays a red-walled temple or the same class of Chinese architecture; a Buddhist statue stays a Buddhist statue), symbolic motifs tied to the product (e.g. red sleeve / red string → 本命年 luck, temple and Buddha → blessing), and mood and rendering. Only the specific instance changes: another temple of the same kind, a different red knit sleeve, a different light direction, time of day or weather, same-theme foreground props. Swapping category or palette (temple → modern room, red → blue-grey) is a QA failure `FAIL_STYLE_DRIFT`. The rule lives in the shared base instructions, because per-shot plans are written in parallel with the global analysis. Analysis output adds `style_lock {palette, theme, motifs[], mood}`.
- **Prompts follow the confirmed images (V2.2.21)** — `recreation_policy.json` → `prompts`.
  - The prompt actually used for each generation is persisted (`user_scene` / `user_motion`), restored on re-entry, and shown in the saved script. Machine re-renders no longer wipe user edits.
  - Video prompts treat the first frame (the confirmed recreated image) as the single source of truth for appearance, and they also carry the film anchor and the garment override.
  - 「按图片更新提示词」 rewrites every frame's image and video prompt from its confirmed image, so video generation never starts from stale text. Actions, camera and lines are kept.
- **One-click follows the selected mode end to end (V2.2.19)** — `recreation_policy.json` → `one_click`. Analysis, images, video (action, sound, lines), subtitles, the brand end card and the final edit all use the same job, so they all follow the chosen 保守 / 中度 / 大胆 policy and any user request.
  - The first product shot and the first person / clothing shot are generated and QA'd before the rest, so the product and look anchors exist for the parallel batch.
  - A resumed run reuses the previous analysis only if the mode and description are unchanged.
- **Brand end card (V2.2.18, all modes)** — `recreation_policy.json` → `brand_end_card`. If the source's last frames are a brand promotion, shop or account page, a platform search or follow page (e.g. 抖音), a QR code or a logo card:
  - Analysis marks them `brand_card: true`. Only a trailing run within the last third of the shots counts.
  - Their image is freely created in the film's style, never copied. The picture has no text, logo, QR code or platform UI, and a clean centre area is left free.
  - Subtitle is `www.yimiagent.cn`, placed in the centre band. No voice-over.
  - QA uses a dedicated end-card check: any text or logo fails, and so does copying the source card.
  - If the source has no such card, nothing is added.
- **Copy and audio-visual sync (V2.2.17)** — `recreation_policy.json` → `copy`:
  - 保守 `light_synonym`: voice-over and on-screen copy stay almost verbatim (same meaning, sentence pattern and length), with only slight synonym swaps.
  - 中度 `same_points_new_wording`: same selling points, structure and function, new wording. Mentions of product, person, clothing and colour follow the new models.
  - 大胆 `rewrite`: keeps each line's selling point and function, otherwise new phrasing and angle.
  - All modes: similar length, brand / account / platform text removed, user copy instructions and hand-edited subtitles win.
  - **Sync**: each line describes only what its own shot shows, so 「开门」 is spoken over the door-opening shot. Video prompts list each line with its in-segment seconds and picture. Video QA matches each ASR segment to its planned line and fails `FAIL_DIALOGUE_TIMING` when it starts outside its shot window (scaled to the generated length, ±1 s). Final-edit subtitles are anchored to the actual spoken word timings.
- **Machine-readable recreation policy (V2.2.16) — `specs/recreation_policy.json` is the source of truth.** Executors MUST load it, not paraphrase this prose. It contains:
  - `priority_order` (rank 1 wins):
    1. this frame's uploaded reference image;
    2. film anchor (「设第 N 帧为全片参考」 or an uploaded film-wide reference);
    3. the user's manual prompt edits;
    4. the breakdown description;
    5. mode defaults;
    6. locks.
  - `modes.{conservative,medium,bold}.elements`: one action per element, from `action_vocabulary`.
  - `anchors`, `user_edits`, `editing_after_generation`, `visual_checklist`, `qa_codes`.
  - It is validated by `schemas/recreation_policy.schema.json`. The site exports it from its recreation policy module, and the analysis prompts are generated from it, so site and Skill cannot drift.
  - **The film anchor beats prompts**: once a frame is set as the film reference, every other frame's person, clothing, hand and product follow it (reference image + text), even where that frame's prompt says nothing or still describes the old look.
  - **Manual edits are film-wide**: on 「修改并联动」 the edit is diffed against every machine-written version of the frame. Look, colour and product clauses are stored in `job.film_edits` and compiled into every frame as a top-priority requirement, free of charge. Frame-specific clauses (camera, position, pose, light) stay local.
- **Recreation strength policy (V2.2.15, confirmed by the user 2026-10-07)** — Anything the user specifies in the description, a prompt edit or a reference image always overrides this table. After generation, every mode can be edited further with prompts and reference images.

  | Element | 保守 (full replica) | 中度 (default) | 大胆 |
  |---|---|---|---|
  | Composition, camera, shot size, subject position | keep | keep | redesign |
  | Hand side, gesture, action, face visibility | keep | keep | may redesign |
  | Main palette, theme, symbolic motifs | keep | keep | may redesign |
  | Product | keep | same category, same colour family, new model | same category, new design |
  | Person / hand look | keep | same-type person, new look; hand new same-colour skin, nails and jewellery | redesign |
  | Clothing | keep | same type, same colour family, new model | redesign |
  | Scene / environment | keep | another place of the same category | redesign |
  | Foreground accents, background props, props | keep | same-theme new items | redesign |
  | Depth of field | keep | may adjust | redesign |
  | Light | keep | may change direction or time of day | redesign |
  | Sound (voice / SFX / BGM) | as close to the source as possible | same type: same gender, age and tone but a new timbre; same-genre new BGM and SFX | new design |
  | Shot function, edit rhythm, line timing | keep | keep | keep |
  | 换一版 | — | yes | yes |

  - 保守 creative_delta is "完全复刻（高清化、去除画面文字）", and QA does not demand creative change.
  - In 中度 and 大胆 the new product is defined once in `global_master.product` and kept consistent through the product anchor. QA accepts a product that differs from the source but is the same category.
- **Breakdown description is top priority (V2.2.14)** — The user's natural-language request is placed at the very top of the master, full and per-shot analysis instructions, above every mode default.
  - Named elements (face or look, garment style and colour, an animal's coat colour, scene style) are REPLACE with a concrete target, even where the mode defaults to PRESERVE or locks colour or subject appearance.
  - "其他不变 / 其余保持 / 只换…" sets `keep_others`. Everything not named is PRESERVE, mode-default replacements are suppressed, and creative_delta lists only the requested changes.
  - Structure (composition, camera, shot size, action, face visibility) stays unless explicitly requested.
  - Each shot's scene must spell the requested changes out.
  - The master returns `user_requests[{element, change}]`. They are compiled into every image and video prompt as 【用户拆解要求】 (top priority, relaxing palette and look constraints the same way as 2.2.13), shown on the breakdown page as 【你的要求（优先执行）】, kept by 换一版, and checked by QA (`FAIL_USER_EDIT_IGNORED`).
  - The cache key carries a rules tag, so old results are re-analysed.
- **User edits win (V2.2.13)** — When the user hand-edits a frame's scene, or syncs an edit with 「同步到其他帧」, the clause-level diff against the planned scene is compiled as a top-priority 【用户手动修改】 block.
  - Conflicting rules give way:
    - colour edits drop the palette ban from 【禁止】 and exempt the style lock;
    - look edits drop the person, hand and clothing entries from 【全片统一设定】 and 【换新】, and the look-anchor text says the edited parts follow the user.
  - A user-uploaded reference 2 takes precedence over text settings and locks.
  - QA is told that following the edit is correct. Ignoring it fails as `FAIL_USER_EDIT_IGNORED`.
  - Edits accepted via sync persist as `shot.user_edits`, and 换一版 keeps them.
  - Field case: 「修改连衣裙颜色：粉紫色、灰蓝色、米白色」 was ignored because five other prompt sections, the look anchor and QA all enforced the original colour.
- **Film-wide look & product consistency (V2.2.12)**
  - **Auto anchors.** Each 爆款二创 image gets reference 1 (the source shot) plus reference images for consistency:
    - a **product anchor** for shots with the product;
    - a **look anchor** (face, hair, clothing, hand) for shots with a person, clothing or a hand.
  - Anchors are user-chosen ones (「设第 N 帧为全片参考」, or an uploaded reference set as film-wide), otherwise the first QA-passed frame of that kind. If one image serves both, it is sent once.
  - The prompt states each reference's role (LOOK_REFERENCE: copy the look only, not background, composition or light).
  - A user's per-frame reference image overrides auto anchors for that frame. Models that accept only a single reference are skipped.
  - **Sync look to other frames.** After a frame's prompt is edited, the user is offered a sync: AI rewrites only the person, clothing and hand wording in the other frames that show them, and updates `global_master`. Scene, action, composition, light and product are untouched, and nothing changes if the edit wasn't about the look. Billed at the AI 帮写 price, refunded on failure. Uploading a reference offers to make it the film-wide look anchor (free).
  - **QA.** When a look anchor was used, it is shown to QA as image 3. A different person or outfit fails as `FAIL_LOOK_DRIFT`, and its targeted fix is appended on redo.
  - Limitation: one-click generates frames in parallel, so an auto anchor exists only after a frame has passed QA. Set an anchor first for strict consistency.
- **中度 / 大胆 wait for the global master; 换一版 (V2.2.11)**
  - Per-shot plans run in parallel with the global analysis only for 保守 without replacement requests. 中度 and 大胆 always replace environment, clothing and similar elements with film-wide new instances, so per-shot plans must be written after the master. Running them in parallel gave them a "keep everything" placeholder, and the result looked like 保守.
  - 中度 and 大胆 offer 「换一版」 per shot. Each click rewrites the shot's scene, motion, creative_delta and light/camera/subject plan within the mode's allowed scope. It keeps the structure lock (中度), the style & motif lock (中度), the product, the shot function and the film-wide master. Earlier versions are passed in so the new one differs, and they are kept as `variants` (last 5). Billed at the AI 帮写 price, confirmed first, and refunded on failure. 保守 does not offer it.
- **Visual parameter checklist (V2.2.10)** — The checklist is the skeleton; natural language is the product. For every source shot, analysis also records `visual {lighting, lighting_plan, lens, texture, weather_time, props, camera_move, subject_move, pace}` as visible facts ("无法确认" when unclear). Generation compiles them into one paragraph, in priority order: subject > action > scene > camera/composition > light/colour > style > quality. Rules:
  - The image prompt gets a 【画面参数】 block (light, lens/depth of field with the focus point, texture, weather/time, props) and a fixed 【画质】 block (subject sharply in focus, product/hand detail legible, no noise, smearing, plastic skin or motion blur). Both go before 【禁止】.
  - The video prompt gets per-shot camera motion and subject motion written separately (e.g. "镜头缓慢推近，手部静止"), pace, lens, light, and a fixed 【画质与运动】 block (stable, no flicker, jelly or warping, even speed).
  - Conflict rule: `lighting` is the source fact and `lighting_plan` is the one light the recreation uses. 保守 keeps the source light (only slight brightening or softening). 中度 may change direction or time of day in harmony with the palette. 大胆 may redesign but must name the key light's direction, hardness and colour temperature. Contradictory lights in one frame are forbidden.
  - New QA codes: image `FAIL_BLURRY`, `FAIL_LIGHTING`; video `FAIL_BLURRY`. Redo fixes are appended to video prompts as well as image prompts.
  - Old jobs without `visual` still compile; they get the quality block only.
- **Edit-plan confirmation everywhere (V2.2.9)** — 爆款二创's 剪辑合成 opens the same 「剪辑方案确认」 dialog as 只剪辑合成. Transitions default to 「跟随原视频」 (taken from the analysed source). The synthesis price is charged only on 「确认并合成」.
- **One editing module for every workflow (V2.2.8)** — 漫剧创作, 爆款二创, 图生视频, 只剪辑合成 and the canvas all produce their final cut through the same FFmpeg post-production module. Every update to editing rules (subtitle style, defaults, grade, transitions, sound continuity) therefore applies to all workflows at once. Never add a workflow-specific subtitle or encode path.
- **Edit-only (只剪辑合成)** — 图生视频 and 漫剧创作 have a small 「只剪辑合成」 button next to the generate / start button. It skips image and video generation and edits the already-uploaded reference images (stills, 3 s each by default; the prompt can say 「每张图 N 秒」) and reference videos, in upload order. It follows the user-prompt-only rule and always applies sound continuity. A cost confirmation appears first.
- **Canvas (画布)** — image-to-video nodes default to 音画同步. The FFmpeg node only edits (transitions, subtitles, grade, beat-sync). The viral-recreation synced canvas no longer has a background-music node, because music comes from the video nodes. On a free canvas, a connected audio node is an optional extra music bed and beat source.

## Non-negotiable production rules
- Source frames define semantic function/composition intent, not an instruction to copy protected branding, text, UI, or irrelevant identity.
- Build a Presence Map before generation. Never introduce a hand, product, clothing item, person, architecture class, text, or logo where the plan marks it absent.
- Establish reusable masters for recurring product, subject/hand, clothing, environment, typography, and audio identity.
- A recurring master must remain visually consistent across every shot in which it is present.
- Each requested keyframe/output is an independent asset. Never create a collage unless explicitly requested.
- Recreation requires meaningful creative delta while preserving the shot's semantic function.
- Generation is not complete until Visual QA passes.
- On QA failure, regenerate only the failed asset with targeted corrections; do not silently advance.
- Fail closed when required references, outputs, or QA evidence are missing.

## Canonical execution chain
`INGEST → COMPLIANCE PRECHECK → SHOT/ASR/OCR/AUDIO ANALYSIS → SOURCE STORYBOARD + MOTION MAP → RECREATED SCRIPT/SVML → MASTER LOCK → IMAGE GENERATION → IMAGE QA/EDIT → VIDEO GENERATION WITH MOTION + NATIVE AUDIO (dialogue/SFX/BGM) → VIDEO+AUDIO QA/EDIT → FFMPEG FINAL EDIT (transitions/subtitles/grade/beat-sync) → FINAL QA → EXPORT/RELEASE CHECK`

Never collapse motion, audio, or final QA into the image-generation stage. Audio is planned in the storyboard and **generated in the video stage**; it is not added afterwards by FFmpeg.

## Stability rules
- Skill/spec updates may add knowledge but MUST preserve existing SVML semantics unless the SVML version is intentionally bumped.
- Executors consume validated SVML/contracts, not prose from industry playbooks.
- Derived timestamps may change after script edits; stable word/event IDs and shot IDs must survive whenever their semantic identity survives.
- Plugins register capabilities through manifests; core execution never imports provider-specific semantics.
- Unknown optional plugin capabilities must degrade gracefully; missing required capabilities must fail closed.

## Model/provider boundary
This Skill is provider-agnostic. It MUST NOT select or hard-code any vendor, channel or model. It declares a capability request and sends it to the **upstream intelligent router**. The upstream router owns provider/model selection, availability, cost/latency policy, failover, credentials, and transport.

Allowed capability names are defined in `tools/capabilities.json`. The mapping of these capabilities to the yimiagent.cn server's existing router (`POST /api/tasks` with model `auto`) is in `tools/router_mapping.yimiagent.json`; the reference adapter is `executor/router_adapter_yimiagent.py`. Mapping files are integration infrastructure and may change without touching Skill rules, SVML or schemas.

## Required machine-readable artifacts
For a production job, prefer these artifacts:
- SVML job document validated by `schemas/svml.schema.json`.
- Per-shot task validated by `schemas/task.schema.json`.
- Generation request validated by `schemas/generation_request.schema.json`.
- QA result validated by `schemas/qa_result.schema.json`.
- Motion reference validated by `schemas/motion_reference.schema.json`.
- Audio timeline validated by `schemas/audio_timeline.schema.json`.
- Per-shot asset/version package validated by `schemas/shot_asset_package.schema.json`.

## Compatibility
`resources/VIDEO_RECREATION_SKILL_V1.8.1.md` is retained as the detailed legacy rulebook.
