# Per-shot Asset Package and Dependency Specification

Every shot is an independently versioned asset package. A canonical shot package may contain:

- source clip / source keyframe(s)
- source analysis and motion reference
- source transcript/OCR/audio cues
- recreated script and shot prompt
- continuity/master references
- recreated image/keyframe
- generated video segment
- audio plan (dialogue lines, voice identity, SFX cues, BGM mood)
- native audio track (embedded in the generated video segment)
- subtitles
- QA records
- version/dependency manifest

## Dependency invalidation
Downstream assets record the IDs and versions of their upstream dependencies. If an upstream script, timing, keyframe, master, or motion reference changes, mark only dependent downstream assets stale. Re-run affected shots/assets, not the entire job.

Typical dependency chain:
`source → analysis → recreated_script/shot_plan (incl. audio plan) → recreated_image → video_segment (picture + native audio) → final_edit (transitions/subtitles/grade/beat-sync) → final_QA`

Changing a shot's dialogue, SFX or BGM plan makes that shot's video segment stale, because audio is generated with the video. Changing only subtitle text, transitions, grade or beat-sync makes only the final edit stale.

A manual edit creates a new asset version and must preserve lineage.
