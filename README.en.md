# VIDEO_AGENT_SKILL V2.2 — Viral Short-Video Recreation Workflow

> One viral video → automatic decomposition / rewriting / generation / QA → a publishable recreated video.

[中文版 README](./README.md)

![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-2.2-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Platform](https://img.shields.io/badge/platform-www.yimiagent.cn-orange)

---

## Install (30 seconds)

### Option 1: Claude Code plugin (recommended)

```
/plugin marketplace add Yf040528/video-recreation-skill
/plugin install video-recreation@video-recreation-skills
```

After installing, just tell Claude Code you want to make a viral recreation and the skill will trigger.

### Option 2: Generic skill install

```
npx skills add Yf040528/video-recreation-skill
```

If prompted to pick a skill, choose `video-recreation-skill`.

### Option 3: Manual copy

Copy the whole `skills/video-recreation-skill` folder into your agent's skills directory (Claude Code: `~/.claude/skills/`), or import `skills/video-recreation-skill/SKILL.md` as a custom instruction.

---

## What is this

A recreation workflow specification for Chinese short-video creation. It turns "I saw a viral video and want my own version" into machine-executable steps: decompose the original → rewrite the script → generate storyboard keyframes → image-to-video → visual QA → edit and assemble.

Use cases:

- **E-commerce short videos**: a product image + a reference hit → keep the selling-point structure, swap in your own product, person and scene.
- **Folklore / traditional-culture videos**: structured recreation for temple, zodiac-year, blessing and similar themes.
- **AI comic / drama**: character consistency control, storyboard planning, dialogue and lip-sync timing.
- **Product ads**: product anchors lock the product's appearance so it does not drift across shots.

## Core problems it solves

| Problem | How this workflow handles it |
|---|---|
| AI faces change from one image to the next | Global character + costume anchors, enforced across shots; drift fails QA |
| The product looks different in every shot | Product anchor images are locked and attached automatically at generation time |
| The recreation ends up identical to the original | Three modes: conservative (full recreation) / medium (same style, swapped instances) / bold (rewrite) |
| Lip-sync is off | Dialogue is generated natively with the visuals, allocated to shots by duration |
| The original contains Douyin search pages or brand cards | Detected automatically and replaced with a clean brand end card |
| Editing one shot's prompt does not propagate | Human edits have the highest priority and can sync to the whole video in one step |

## Three recreation modes

- **Conservative** — recreate the original's structure, style and shot language, with only minor synonym swaps.
- **Medium** — lock structure and style (palette, theme, symbols), replace only same-category, same-colour instances.
- **Bold** — keep each shot's selling point and function, rewrite visuals and copy completely.

## Quick start

### Option A: Web, no code

1. Open **[www.yimiagent.cn](https://www.yimiagent.cn)**
2. Create a "viral recreation" task and upload a reference video.
3. Pick a mode (conservative / medium / bold) and fill in your product and requirements.
4. Generate in one run: decomposition → script → keyframes → video → QA → final cut.

### Option B: Inside your own agent (developers)

This repository is a standard skill specification (`SKILL.md` + `specs/` + `schemas/`). Any agent platform that supports skills can load it, and the specification itself can be used offline without logging in to the platform:

- **WorkBuddy**: `git clone` this repository to `~/.workbuddy/skills/video-recreation/`
- **Claude / Cursor**: import the `SKILL.md` content as a system prompt or custom instruction
- **Custom agents**: read the machine-readable files under `specs/` and `schemas/` and implement your own executor (see `executor/router_adapter_yimiagent.py`)

## Repository structure

```
skills/video-recreation-skill/SKILL.md  Main workflow specification (start here)
ARCHITECTURE.md       Three layers: Skill / SVML / Execution
CHANGELOG.md          Version history
specs/                Per-stage specifications (generation, motion, continuity, audio timeline, visual QA…)
schemas/              Machine-readable output definitions (SVML, tasks, generation requests, QA results…)
executor/             Reference executor and upstream routing adapters
tools/                Capability declarations and routing maps
resources/            V1.8.1 historical rules
```

## Design principles

- **Model-agnostic**: the skill only declares what capability is needed; the upstream smart router decides which model serves it and how to fail over.
- **Specification over prose**: executors read machine-readable files such as `specs/recreation_policy.json`, not only natural-language descriptions.
- **Human edits win**: user-written prompts and reference images override all automatic rules.
- **Failures are visible**: a failed QA check reports a specific failure code instead of silently skipping.

---

## Version notes

V2.2 strengthens the full recreation pipeline: original shot splitting + ASR/OCR/audio analysis; storyboard with keyframes and motion; recreated script/storyboard; global character, style and product anchors; per-shot image generation with QA/editing; video generation from approved images + prompts + original motion + audio timing; video QA; native audio (dialogue / SFX / BGM); FFmpeg assembly; final check; versioned per-shot asset packs; dependency-aware partial regeneration; compliance and transformation review.

**Architecture upgrade**: three-layer separation (Skill / SVML / Execution), word-level semantic anchors and timeline reordering.

**V2.2.1 (2026-10-04)**
- Dialogue, sound effects and BGM are generated natively in the image-to-video step. FFmpeg only edits: transitions, subtitles, colour grading, beat-sync cuts.
- The capability → server routing map is in `tools/router_mapping.yimiagent.json` (adapter: `executor/router_adapter_yimiagent.py`).
- V1 executor files are in `resources/legacy_v1/` and `executor/`.
- This skill is the authoritative workflow for viral recreation. Further workflow changes are recorded here and in `CHANGELOG.md`.

Reading order: start from `skills/video-recreation-skill/SKILL.md`, then follow its pointers into specs and schemas. V1.8.1 historical rules are kept in the repository for compatibility reference.

---

## About

This workflow runs on **[www.yimiagent.cn](https://www.yimiagent.cn)** — a visual video-agent workspace supporting text-to-image, image-to-image, image-to-video, FFmpeg editing and assembly, and industry workflows for e-commerce, AI comic/drama and viral recreation.

## License

[MIT](./LICENSE)

**Keywords**: video recreation · viral video decomposition · AI video workflow · short-video e-commerce · image-to-video · character consistency · product anchor · TikTok recreation · Douyin recreation · AI comic drama · folklore video · folk short video · batch video production · video recreation skill · short video automation
