# Audio and Timeline Specification

Audio is planned at storyboard time, not appended as an afterthought.

Each shot may define dialogue/narration text, speaker/voice identity, speech timing, lip-sync requirement, sound-effect cues, music mood, beat markers, ducking/mix intent, and subtitle timing.

## Where audio is produced (V2.2.1)
Dialogue/narration, SFX and BGM are **generated natively by the image-to-video step**, in sync with the picture. The video request carries the shot's audio plan:

- spoken lines (quoted, sized to the segment duration, about 4 Chinese characters per second) and the voice identity; mouth movement matches the line when the speaker is on screen, otherwise the line is narration;
- SFX cues tied to visible actions (the source video's detected SFX events may be used as reference);
- BGM: instrumental, no sung vocals, mood/genre/instruments similar to the source but newly composed, starting from the first frame, sitting under the voice, with accents on actions and camera changes;
- a silent source video yields a silent recreation.

The FFmpeg final edit **does not** generate or add voice, music or SFX. It keeps each segment's native audio, crossfades it at transitions, may layer **user-supplied** music when the user explicitly connects it, and normalises loudness.

## Sound continuity (声音衔接)
At the final edit: measure each segment's integrated loudness (EBU R128) and level it to a common target (−16 LUFS, max ±10 dB; near-silent segments are not boosted); apply 30 ms fades at every join; crossfade audio together with picture transitions. Loudness normalisation of the full mix follows. This smooths joins without adding new sound, so it also applies under the user-prompt-only rule.

## Subtitles
Subtitle text comes from the script (voice-over lines) or the user. Subtitle timing is derived from the speech actually present in each generated segment (ASR on the segment audio), with the shot window as a fallback. With word-level timestamps, long subtitle lines are split at punctuation and each phrase starts when its first word is spoken. When no speech exists and the user explicitly asks for captions, captions may be written per segment and spread over the segment windows.

Subtitle style (V2.2.7, applies to every workflow and every final edit):
- **No trailing full stop.** No subtitle line ends with 。/．/. ; a full stop between two sentences inside one line is replaced by a space. Question marks, exclamation marks and ellipses (……/...) are kept.
- **Fixed style and position (V2.2.8, supersedes the 2.2.7 one-third rule).** Reference frame 1080×1920:

  ```
  PlayResX 1080 / PlayResY 1920
  Style: Main,Noto Sans CJK SC(思源黑体 Bold),54,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,60,60,300,1
  ```

  - Size 54 px, bold.
  - White fill, black outline 3, shadow 1.
  - Bottom-centre (`Alignment=2`), `MarginV=300`, `MarginL/R=60`.
  - The bottom-left stays clear for the platform account, watermark and buttons; never closer than 250 px to the bottom.
  - Other output sizes scale size, outline, shadow and side margins by short side ÷ 1080, and MarginV by height ÷ 1920.
  - Lines wrap at about 14 CJK characters (portrait), so no line leaves the side margins.
  - On-screen copy recreated at the source text position (viral recreation) keeps its own position.
- **No ASR hallucinations.** On music-only or ambient audio, ASR may output platform stock phrases (请点赞 / 订阅 / 转发 / 打赏 / 感谢观看 / 字幕由…提供 / 明镜与点点 …). These segments are discarded and never become subtitles or dialogue in QA.
- **User switch.** In the edit-plan dialog, 「按视频里的台词自动生成字幕」 is on by default. When it is off, no dialogue subtitles are added even if the video has speech; shot subtitles the user typed in explicitly are kept.

## Beat-sync
Cut points may be snapped to strong onsets of the outgoing segment's own music, or of user-supplied music (trim of up to 0.6 s at the end of the outgoing segment). A cut must not interrupt a spoken line. Viral recreation keeps the source shot timing unless the user asks for beat-sync.

## Final checks
Final assembly must validate dialogue intelligibility, lip sync when required, SFX timing, BGM presence/absence as planned, clipping, loudness balance, subtitle sync, and intended silence.
