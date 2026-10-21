# Layered QA Specification

QA is evidence-based, stage-specific, and fail-closed. Do not invent PASS results.

## 1. Script QA
Check semantic coverage, hook/value/CTA logic when applicable, shot continuity, timing feasibility, dialogue/subtitle correctness, creative transformation, and required/forbidden elements.

## 2. Image QA
Check character/face/hand/product/clothing/style consistency, geometry, presence map, source semantic function, composition/safe zones, text correctness, artifacts/deformation, creative delta, sharpness (`FAIL_BLURRY`: subject out of focus, soft, smeared or low-detail; background blur per the planned lens is fine) look consistency against the film-wide look anchor when one was used (`FAIL_LOOK_DRIFT`), and lighting (`FAIL_LIGHTING`: against the shot's `lighting_plan` or contradictory light sources). Failed images may be locally edited or regenerated without advancing the shot.

## 3. Video QA
Check identity consistency over time, motion stability, camera trajectory, subject motion, temporal coherence, product geometry, anatomy, flicker/warping, sharpness (`FAIL_BLURRY`), first/last state, duration, prompt adherence, and source-motion preservation or intentional redesign. Because audio is generated with the video (V2.2.1), video QA also checks the native audio: planned lines spoken and intelligible, lip sync, SFX on the right actions, BGM present or absent as planned. Re-run only failed shots when possible. Reference implementation: sample the first/middle/last frames for visual checks; ASR the native track and compare it with planned lines by character overlap (tolerant of recognition errors); record BGM presence separately.

## 4. Audio QA
Run on the native audio of each segment and on the final edit. Check dialogue accuracy/intelligibility, speaker/voice continuity, lip sync when required, SFX timing, BGM beat alignment, clipping, noise, loudness balance, subtitle sync, and music/dialogue ducking.

## 5. Final-film QA
Check edit continuity, transitions (type as planned, no flash frames), beat-sync cuts not interrupting speech, timing/rhythm, subtitles, color consistency, audio mix, missing/duplicate shots, output specs, platform safe zones, compliance flags, and transformation/similarity policy.

Every result should identify `stage`, `shot_id` or final asset, `status`, `checks`, `fail_codes`, `evidence`, and `targeted_corrections`. A failure invalidates dependent downstream artifacts according to the asset dependency specification.
