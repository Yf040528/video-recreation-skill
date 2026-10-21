# SVML 1.0 — Semantic Video Markup Language

SVML is the Skill's provider-neutral intermediate representation for video/image production. It describes **what must exist and remain consistent**, not which model should create it.

## Core hierarchy
`job → masters → references → timeline/shots → generation → qa_policy`

## Job
Required: `svml_version`, `job_id`, `intent`, `output`, `masters`, `shots`.

## Masters
Reusable visual/audio identities. Common keys: `subject`, `hand`, `product`, `clothing`, `environment`, `style`, `audio`. A master may contain `description`, `reference_ids`, `invariants`, and `allowed_variation`.

## References
Every reference has an `id`, `uri`, and `role`. Roles include `semantic`, `product_identity`, `subject_identity`, `clothing_identity`, `style`, `environment`, `motion`, `audio`, and `negative`. One reference may have multiple explicit roles; unassigned roles must not be inferred.

## Shot
Each shot has a stable `id`, `semantic_function`, `presence`, `preserve`, `replace`, `creative_delta`, optional `camera`, `motion`, `audio`, `timing`, and `generation` requirements.

### Presence
Presence is authoritative. Common entities: `subject`, `hand`, `product`, `clothing`, `architecture`, `text`, `logo`. Values are boolean. Generation and QA must treat false as a hard negative constraint.

### Preserve vs Replace
`preserve` describes functional/structural attributes to retain. `replace` describes source elements that must be transformed or removed. Do not collapse them into one free-text prompt.

### Creative delta
A recreation shot must declare at least two meaningful changes unless the task explicitly requests faithful restoration/editing. Typical deltas: camera/viewpoint, composition, environment, lighting/weather, foreground/background organization, styling.

## Timing
Video shots may define `start_sec`, `end_sec`, `duration_sec`. Timeline validation should reject negative durations and overlapping shots unless overlap is explicitly allowed.

## Generation
Generation describes capability requirements such as `image_generation`, `image_edit`, or `video_generation`, aspect ratio, duration, reference support, consistency level, and output count. It never names a provider/model.

## QA policy
A job can define required checks, retry limits, and fail-closed behavior. QA results are external evidence and must not be fabricated by the planning model.

## Minimal example
```json
{
  "svml_version":"1.0",
  "job_id":"demo",
  "intent":"recreate",
  "output":{"aspect_ratio":"9:16"},
  "masters":{"product":{"description":"same product identity"}},
  "shots":[{
    "id":"SHOT_01",
    "semantic_function":"close product reveal",
    "presence":{"hand":true,"product":true,"clothing":false,"architecture":false,"text":false,"logo":false},
    "preserve":["one-hand product reveal"],
    "replace":["source branding"],
    "creative_delta":["new camera angle","new lighting"],
    "generation":{"capability":"image_generation","asset_count":1}
  }]
}
```

## Motion is first-class
A keyframe is not a motion specification. Video shots should carry a `motion_reference` or explicit motion design describing camera trajectory, subject movement, speed/easing, focal/zoom/focus change, depth/parallax, pose trajectory, and first/last states where available. See `MOTION_SPEC.md`.

## Audio is first-class
Dialogue, voice identity, timing, lip-sync requirement, SFX cues, BGM mood/beat markers, and subtitle timing belong in the storyboard/SVML timeline before final generation and assembly. See `AUDIO_TIMELINE_SPEC.md`.

## Per-shot lineage
Each shot should map to a versioned asset package. Downstream artifacts must retain dependency versions so upstream edits invalidate only affected assets. See `ASSET_DEPENDENCY_SPEC.md`.

## QA stages
Use separate gates for `script`, `image`, `video`, `audio`, and `final_film`. A generic visual PASS is not sufficient for the whole production.
