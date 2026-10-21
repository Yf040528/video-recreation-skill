# Video Agent V2.2 Architecture

## Three stable layers
**Knowledge / Skill**: director knowledge, industry workflows, constraints, QA and transformation policy. Evolves frequently.

**Language / SVML**: stable provider-neutral intermediate representation and JSON Schemas. It is the compatibility boundary.

**Execution / Runtime**: compiler, validator, dependency/retry logic and capability plugins. It executes contracts and avoids embedding creative policy.

## Data flow
User/Canvas → Skill reasoning → validated SVML → compiler → capability/plugin registry → upstream intelligent router or deterministic tool → normalized result → layered QA → dependency-aware retry → assembly/export.

## Synchronization model
Speech text owns stable word IDs. Timeline-sensitive events attach to word anchors. Alignment produces derived timecodes for video/audio tools and FFmpeg. Script edits trigger reflow rather than manual timeline repair.

## Extension model
A new provider/model is mapped behind the upstream router. A genuinely new capability is registered as a plugin with a manifest and stable contracts. Existing Skill/SVML remain untouched unless the capability requires a deliberate language-version extension.
