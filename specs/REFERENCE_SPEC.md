# Reference Specification
References are role-scoped evidence, not unrestricted style/copy instructions.

1. Assign each reference an explicit role before generation.
2. Product references control product identity only when role includes `product_identity`.
3. Clothing references control clothing only when role includes `clothing_identity`.
4. Source frames normally control `semantic` and optional `composition`; source text, branding, UI and unrelated identities are not inherited.
5. When references conflict, master invariants outrank shot-level aesthetic suggestions; explicit user instructions outrank inferred reference traits.
6. Missing mandatory identity references must produce a blocked/fail-closed state rather than invented certainty.
