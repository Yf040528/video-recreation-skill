# Generation Specification
The Skill emits capability requests; the upstream router chooses the provider/model.

For each asset: validate task → compile prompt/constraints → create one generation request → route upstream → persist one output → request visual QA. `asset_count: 1` is mandatory for independent keyframes unless the user explicitly asks for a set/collage.

Generation requests should carry: capability, task_id, prompt, source/reference URIs, hard constraints, desired output properties, and routing hints expressed only as capability/QoS needs (quality, latency, cost tier, reference support). Never include API credentials.

## Video requests carry native audio (V2.2.1)
A `video_generation` request sets `requirements.native_audio = true` (unless the source/job is intentionally silent) and includes the shot's audio plan in the prompt/inputs: spoken lines, voice identity, SFX cues and BGM mood. No burned-in subtitles. The router passes this to models that support native audio. It may route silent-only channels only when native audio is not required, and it must report a missing audio capability instead of dropping the plan. Post-production never substitutes TTS or generated music for a missing native track.

## Visual parameter checklist (V2.2.10)
Prompts are compiled from the shot's structured fields; the checklist is never sent as a bare tag list. Image: subject → action → scene → camera/composition → 【画面参数】(lighting_plan, lens + focus point, texture, weather/time, props) → 【画质】 → 【禁止】. Video: structure → per-shot camera_move / subject_move / pace / lens / light (separately stated) → 【画质与运动】 → targeted fixes → 【声音】. A shot has exactly one light plan; the recreation mode bounds how far it may move from the source light.
