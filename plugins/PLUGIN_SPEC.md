# Capability Plugin Specification

Plugins connect stable Video Agent capabilities to the upstream intelligent router or deterministic local tools. A plugin is replaceable infrastructure, not domain knowledge.

A plugin manifest declares: `plugin_id`, `version`, `capabilities`, input/output contract versions, execution kind (`upstream_router` or `local_deterministic`), optional feature flags, and health/failure semantics.

Core rules:
- Never hard-code provider/model names in Skill or SVML.
- New model/channel support is added behind a plugin/router mapping.
- Plugins normalize provider-specific responses into stable capability outputs.
- Missing required capability fails closed; optional capability may fall back only when contract-compatible.
- Plugin changes must not mutate the meaning of existing SVML fields.

V2.2.1 note: the `ffmpeg-media` plugin's `audio_mix` is limited to crossfades, an optional user-supplied music bed and loudness normalisation. Its `audio_stem_separation` is served by local sound-event classification (not true stems).
