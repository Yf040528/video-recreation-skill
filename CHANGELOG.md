# Changelog

## 2.2.22 — 2026-10-07
- **Video prompts carry 【时长与规格】**: segment duration, approximate seconds per shot, aspect ratio, resolution, clarity and frame rate. Image prompts state ratio and resolution.
- **QA tolerance**:
  - The product fails only on obvious substitution, colour change, absence or deformation; size, angle and detail differences are accepted.
  - Light is checked against the prompt actually used, not a stale 换一版 plan.

## 2.2.21 — 2026-10-07
- **Prompts follow the confirmed images**:
  - Persisted per-frame user prompts are restored on re-entry.
  - Video prompts follow the first frame (首帧为准) and the anchor.
  - New action 「按图片更新提示词」 refreshes image and video prompts from the generated images.

## 2.2.20 — 2026-10-07
- **Anchor fixes** (field case: frame 3 kept the pink-grey striped dress although frame 1, the anchor, had a red dress):
  1. When reference 2 is both product and look anchor, its role text no longer says "only the product, not the person".
  2. Old garment phrases in 二创画面 / 结构锁定 / 保留 / 全片统一设定 are replaced by the anchor's garment.
  3. The anchor look text drops pose, finger, light and depth clauses.

## 2.2.19 — 2026-10-07
- **One-click**:
  - Strictly follows the selected mode.
  - Resume re-analyses when the mode or description changed.
  - The look lead shot is generated alongside the product lead shot before the parallel batch.

## 2.2.18 — 2026-10-07
- **Brand end card** (all modes): source brand / platform end frames are replaced by a freely created end shot, with subtitle `www.yimiagent.cn` and no voice-over. Nothing is added if the source has none. Includes dedicated image prompt, video note and QA.

## 2.2.17 — 2026-10-07
- **Copy policy per mode**: 保守 light synonym edit, 中度 same points with new wording (following the new models), 大胆 rewrite. Stored in `recreation_policy.json` → `copy`.
- **Audio-visual sync**:
  - Lines are tied to their shot's picture.
  - Video prompts carry a per-shot speech timeline.
  - Video QA adds `FAIL_DIALOGUE_TIMING`.
  - Redo fixes now exist for the audio QA codes.

## 2.2.16 — 2026-10-07
- **Machine-readable policy**: `specs/recreation_policy.json` and `schemas/recreation_policy.schema.json`, exported from the site's `RECREATION_POLICY`, which also generates the analysis prompts.
- **Priority order**: frame reference image > film anchor > manual prompt edit > breakdown description > mode defaults > locks.
- **Film anchor beats prompts**: the anchor frame's look text is stored on the anchor and compiled into every other frame. QA checks it as `FAIL_LOOK_DRIFT`.
- **Manual edits become film-wide** on 修改并联动 (`job.film_edits`, diff against machine versions, free of charge). This replaces the paid sync dialog.

## 2.2.15 — 2026-10-07
- **New mode policy**:
  - 保守 = full replica: props, foreground and depth are kept, and no invented deltas.
  - 中度 = structure and palette kept; product, person / hand, clothing, scene, props and sound become same-category, same-colour new models.
  - 大胆 = product becomes a same-category new design, and everything else is redesigned.
  - User instructions override in every mode.
- The policy is applied as an overlay on the server: analysis, image prompts, QA, redo fixes and the native-audio prompt. The mode dropdown tooltip is updated.

## 2.2.14 — 2026-10-07
- **Natural-language breakdown request = highest priority**:
  - Named elements are replaced even against mode defaults.
  - 「其他不变」 keeps everything else as in the source.
  - `user_requests` and `keep_others` are compiled into all image and video prompts, shown on the breakdown page, kept by 换一版, and QA-checked.

## 2.2.13 — 2026-10-07
- **User edits win over locks**:
  - The diff of the user's edit becomes a 【用户手动修改】 block at top priority.
  - Conflicting palette and look constraints are relaxed.
  - A user reference 2 takes precedence over text settings and locks.
  - QA code `FAIL_USER_EDIT_IGNORED`.
  - `shot.user_edits` persists through sync and 换一版.

## 2.2.12 — 2026-10-07
- **Film-wide consistency anchors**:
  - Product anchor and look anchor (person / clothing / hand), automatic or user-set. Upload-as-anchor is supported.
  - Each reference's role is stated in the prompt.
  - QA adds `FAIL_LOOK_DRIFT`, with the look anchor shown to QA as image 3.
- **Sync look to other frames** after a prompt edit: AI rewrites only the look wording of the affected frames and updates `global_master`.
- The redo dialog no longer treats an auto-added anchor as a user reference.
- Prompt compaction is applied before the length check, dropping 画质 → 画面参数 → 全片统一设定 → 保留.

## 2.2.11 — 2026-10-07
- **Fix: 中度 looked like 保守.** When the user's request had no replacement wording, per-shot plans ran in parallel with the master analysis and received the placeholder "全部保留原样". 中度 and 大胆 now always wait for the master. Field case: 《爆款二创 2026/10/6 23:10:29》. The master said to replace the environment and clothing, but every shot kept the original chairs and tiles, and the deltas were only lighting tweaks.
- **换一版** (中度 / 大胆): per-shot rewrite within the mode's allowed scope, using the history of earlier versions. Billed at the AI 帮写 price, with refund on failure.

## 2.2.10 — 2026-10-07
- **Visual parameter checklist for 爆款二创** (all three modes). Field problems it addresses: missing details, drift, and soft or unclear frames.
  - Analysis adds per-shot `visual`: lighting (source), lighting_plan (recreation), lens/depth of field with focus point, texture, weather/time, props, camera_move, subject_move, pace.
  - Image prompts add 【画面参数】 and a fixed 【画质】 block before 【禁止】.
  - Video prompts add separate per-shot camera and subject motion, pace and light, a fixed 【画质与运动】 block, and redo fixes.
  - One light per shot. Each mode defines how far it may move from the source light.
- **QA**: image `FAIL_BLURRY`, `FAIL_LIGHTING`; video `FAIL_BLURRY`, with targeted fixes for video codes (`FAIL_IDENTITY_DRIFT`, `FAIL_PRODUCT_GEOMETRY`, `FAIL_CAMERA_MOTION`).
- The breakdown cache key changes automatically, because it hashes the instructions.
- On models with a prompt length cap, the image prompt drops 【画质】, then 【画面参数】, before any truncation.

## 2.2.9 — 2026-10-06
- **中度 = structure lock + style & motif lock.** Palette, theme and scene category, product-linked motifs and mood stay as in the source. Only same-category, same-colour instances are replaced.
  - New analysis field `style_lock`.
  - New QA code `FAIL_STYLE_DRIFT`.
  - The rule is in the shared base instructions, so parallel per-shot plans follow it.
- **爆款二创 剪辑合成 uses the edit-plan confirmation dialog.** Transitions default to 跟随原视频. The price is charged on confirm.

## 2.2.8 — 2026-10-06
- **Fixed subtitle style** (supersedes the 2.2.7 one-third position). This is now the permanent editing standard:
  - Reference frame 1080×1920; other sizes scale proportionally.
  - Font: 思源黑体 Bold 54, white, black outline 3, shadow 1.
  - Position: bottom-centre, MarginV 300, MarginL/R 60.
  - Keeps the 2.2.7 rules: no trailing full stop, ASR hallucination filter, auto-subtitle switch.
- **Single editing module**: 漫剧创作, 爆款二创, 图生视频, 只剪辑合成 and the canvas share one post-production module. Every editing-rule update applies to all of them at once.

## 2.2.7 — 2026-10-06
- **Subtitle style rules** (every workflow, every final edit):
  - No subtitle line ends with a full stop (。/．/.). A full stop between two sentences in one line becomes a space. ？！ and ellipses are kept.
  - The subtitle's bottom edge sits one third of the frame height above the bottom (ASS `MarginV = H/3`). After publishing, the bottom-left account info, caption and buttons would otherwise cover it.
- **ASR hallucination filter**: on music-only audio, ASR "hears" platform stock phrases (请点赞、订阅、转发、打赏、感谢观看、字幕由…提供). These are dropped before subtitle generation and dialogue QA.
- **Auto-subtitle switch**: the edit-plan dialog has 「按视频里的台词自动生成字幕」 (default on). When it is off, no dialogue subtitles are added; explicit shot subtitles are kept. The setting is stored on the task and reused by re-runs.
- **Standard edit defaults**:
  - Output: 1080×1920 portrait / 1920×1080 landscape, 30 fps, CRF 18, preset medium. A user bitrate is floored at ≈8 Mbps for 1080p.
  - Grade: light unified grade with light luma-only sharpen.
  - Grade mapping: brightness 2 → +0.02, contrast 7 → ×1.07.
  - Empty plan fields mean "not specified". Fixes empty total duration → 1 s and empty size/fps → 240/15.
- **漫剧 self-check** (人物 / 景 / 声音) with manual redo and lesson logging.

## 2.2.6 — 2026-10-06
- **Edit plan**: the user's editing script is compiled into a structured plan (per-cut transitions, grade parameters, shot subtitles, output spec, target duration) and executed exactly. Items that need missing media are reported as not executed.
- **Executor fix**: hard cuts are concatenated, not done as 0.04 s xfades. On FFmpeg 8, an xfade shorter than about 2 frames silently truncates everything after it; real transitions are at least 0.1 s.
- Once a plan exists, it decides beat-sync and shot-level subtitles; keywords in the free text no longer override it.
- **Plan confirmation**: edit-only first calls POST /api/edit-plan (free) and shows the plan in an editable dialog. Charging and synthesis start only after the user confirms, and the confirmed plan is saved on the task. Re-runs reuse it instead of re-interpreting the prompt, so results are reproducible.

## 2.2.5 — 2026-10-05
- **Sound continuity (声音衔接)** added to the final edit in every workflow (图生视频, 漫剧创作, 爆款二创, canvas): per-segment loudness levelling, join fades, audio crossfades with transitions.
- **Edit-only (只剪辑合成)** in 图生视频 and 漫剧创作: edits the uploaded reference images and videos without generating anything.
- **Correction to 2.2.4**: measured upstream tokens show the analysis route ignores the `detail` flag; images were always analysed at full resolution. Inaccurate hand side and bead counts are therefore model judgement errors on ambiguous close-ups, not image resolution. The remaining 2.2.4 fixes (QA text presence, reference replaces all products, redo loop) stand.

## 2.2.4 — 2026-10-05
- **Analysis sees full detail**: keyframes go to the analysis model at high image detail. With low detail it could not read finger poses, hand side or bead counts, which produced vague structure locks ("无法确认") and repeated redos.
- **QA no longer requires source text**: the source's on-screen text is removed from the reference, so presence checks skip `text` (this false FAIL_PRESENCE caused needless redos).
- **User reference = replace all products**: when the user attaches a product reference to a frame, every product instance in the shot (whatever the count, strands or layers) becomes the reference product. Positions and hand pose follow the source frame; the reference wins over conflicting text.
- **Redo loop**: 重做 opens a dialog. It shows the QA reason, auto-drafts a revised scene addressing exactly the failed checks (editable), and lets the user replace or remove reference image 2. The redo is billed normally; nothing retries automatically.
- **Self-improvement record**: every redo outcome (before/after prompt, fail codes, whether the user edited the prompt or changed the reference, pass/fail after the redo) is stored as a skill lesson and periodically reviewed into this Skill.

## 2.2.3 — 2026-10-05
- **User-prompt-only rule** for 漫剧创作 and 图生视频: nothing the user didn't request is added (dialogue, captions/subtitles, grade, beat-sync, transitions, BGM). Only 爆款二创 imitates the source, and it never adds subtitles or speech the source lacks. Reason: an internal prompt containing 「字幕」 caused AI captions on a dialogue-free video.

## 2.2.2 — 2026-10-05
- **Merged multi-shot segments**: adjacent shots are merged into one image-to-video request (span ≤ 10 s, ≤ 4 shots, generated duration ≤ 12 s), so dialogue and BGM stay continuous inside a segment and there are fewer joins.
- **Word-level timing in practice**: local ASR now returns per-word timestamps (biased to Simplified Chinese). Long subtitles are split at punctuation and each phrase is timed to the spoken words. Beat-sync cuts check word boundaries.
- **Video + audio QA**: every recreated segment is checked automatically. Audio checks: audio present; planned lines spoken (character similarity, tolerant of ASR and traditional/simplified differences); no speech when the source had none. Visual checks on the first/middle/last frames: presence, overlaid text (OCR re-check), collage, extra hands, product geometry, identity drift. BGM presence is recorded as a note, not a failure. No automatic retry.
- **Field finding**: the first native-audio test produced action SFX (frying/sizzle) but no detectable BGM. Track `checks.music` before relying on video-native BGM.

## 2.2.1 — 2026-10-04
- **Audio moved into image-to-video**: dialogue/narration, SFX and BGM are generated natively by the video model together with the picture. FFmpeg now does only the final edit: transitions, subtitles (aligned to the spoken audio), colour grading and beat-sync cuts. Updated: SKILL.md workflow/execution chain, AUDIO_TIMELINE_SPEC, GENERATION_SPEC, MOTION_SPEC, ASSET_DEPENDENCY_SPEC, VISUAL_QA_SPEC, TOOL_SPEC, PLUGIN_SPEC. Added workflow logic for 漫剧创作 / 图生视频 / 爆款二创 / 画布.
- **Router mapping**: `tools/router_mapping.yimiagent.json` maps every capability to the yimiagent.cn server's existing router and local tools. `executor/router_adapter_yimiagent.py` is the reference `UpstreamRouter`.
- **Registered from the server (VIDEO_AGENT_EXECUTOR_V1)**: the server copy is byte-identical to the original upload. The V1 files that were missing from 2.2.0 are now included: `executor/adapters_legacy.py`, `executor/__init__.py`, `resources/legacy_v1/QA_RESULT_TEMPLATE.json`, `resources/legacy_v1/EXECUTOR_V1_README.md`.
- Unchanged: core non-negotiable rules, SVML (`specs/SVML_SPEC.md`) and all JSON Schemas.

## 2.2.0
- Standardised package: three-layer architecture, word-level anchoring, capability plugins, layered QA, per-shot asset packages.
