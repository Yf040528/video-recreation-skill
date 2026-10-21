# Tool / Capability Contract

## Boundary
All external inference is invoked through one logical interface: `upstream_router.execute(request)`. The concrete server implementation may expose HTTP, RPC, Python, queue, or another transport. The integrator should adapt this boundary to the server without changing SVML or director rules.

## Standard request
Required: `request_id`, `capability`, `task_id`, `inputs`, `requirements`. Optional: `routing_hints`, `metadata`.

## Standard response
Required: `request_id`, `status`. On success include `outputs`; on failure include normalized `error` with `code`, `message`, `retryable`. Provider/model metadata may be returned for observability but must not become a planning dependency.

## Capability semantics
- `text_analysis`: planning/reasoning over text/metadata.
- `vision_analysis`: inspect images.
- `video_analysis`: inspect/deconstruct video.
- `image_generation`: create a new image.
- `image_edit`: transform an existing image with references.
- `video_generation`: create video from prompt/reference inputs.
- `vision_qa`: judge actual generated visual output against structured criteria.
- `audio_generation` / `speech_generation`: optional standalone audio capabilities. Since V2.2.1 the default workflows do not call them, because dialogue/SFX/BGM come from `video_generation` with native audio.
- `media_edit` / `audio_mix`: deterministic final edit (transitions, subtitles, grade, beat-sync, crossfade, loudness). They never synthesise voice, music or SFX.

## Server mapping
The concrete mapping to the yimiagent.cn router is in `router_mapping.yimiagent.json`, and the reference adapter is `../executor/router_adapter_yimiagent.py`.

## Router responsibilities
Provider/model selection, credentials, endpoint formats, upload mechanics, async polling, quotas, cost/latency balancing, retries caused by transport/provider failure, and failover.

## Skill responsibilities
Semantic planning, continuity, constraints, task compilation, generation/QA sequencing, creative retries caused by visual failure, and machine-readable state.

## V2.1 production capabilities
The Skill may request provider-neutral capabilities for shot segmentation, ASR, OCR, audio stem separation, motion analysis, depth analysis, pose tracking, camera trajectory analysis, image generation/edit, image-to-video, video-to-video, lip sync, speech/audio generation, audio mixing, deterministic media editing/FFmpeg, QA, and compliance review. Unsupported controls must be surfaced explicitly by the upstream router; never silently drop motion/audio/consistency constraints.
