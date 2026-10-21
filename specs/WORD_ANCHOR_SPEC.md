# Word-Level Anchoring Specification

## Purpose
Synchronised production events attach to semantic words/tokens rather than fragile absolute timeline positions. Timecodes are derived by compilation from the latest speech/alignment result.

## Stable IDs
Each spoken unit has a stable `word_id` within a dialogue/narration segment. An anchor targets `word_id` plus an optional boundary: `before`, `start`, `center`, `end`, `after`, or a bounded offset.

## Anchorable events
Subtitles/captions, SFX, visual overlays, cut/edit cues, camera emphasis, lip-sync markers, BGM ducking, beat accents, animation triggers, and other synchronized events may reference word anchors.

## Reflow rule
When script text, TTS voice, speaking rate, or alignment changes:
1. Preserve stable word IDs for semantically retained words when possible.
2. Re-run speech/alignment for affected segments.
3. Recompile anchored events into derived timestamps.
4. Mark only dependent rendered assets stale.
5. Never manually propagate old absolute timestamps as authoritative truth.

## Anchor loss
If an edited script deletes an anchored word, the compiler resolves according to `fallback`: nearest surviving word, segment start/end, explicit manual review, or fail-closed. Critical events default to manual review/fail-closed.

## Timecode boundary
External generators and FFmpeg may require seconds/frames. The compiler materializes those values at execution time. They remain derived data with lineage to the anchor and alignment version.
