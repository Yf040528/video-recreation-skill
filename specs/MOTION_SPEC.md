# Motion Reference Specification

Keyframes define appearance and composition; they do not fully encode motion. Every recreated video shot should preserve or intentionally redesign motion as a separate production layer.

## Motion extraction
For each source shot, record where available: camera motion (push/pull/pan/tilt/truck/pedestal/orbit/handheld/static), subject motion, motion direction, speed, acceleration/easing, focal-length or zoom change, focus change, depth/parallax, pose trajectory, start/end states, and important motion beats.

Derived motion references may include optical flow, depth maps, pose/keypoint tracks, camera trajectory, motion masks/brushes, first/last frames, or source-video motion reference. These are guidance assets, not appearance/identity masters.

## Video generation contract
A recreated shot should use: approved recreated image/keyframe + shot prompt + motion_reference when available + first/last frame or trajectory constraints when supported + the shot's audio plan (dialogue, SFX, BGM), generated natively with the picture.

Prefer video-to-video transformation when preserving complex motion is materially more important than pure image-to-video reconstruction and the upstream capability supports it.

If a provider does not support a requested motion control, the upstream router must return capability limitations rather than silently discarding the constraint.
