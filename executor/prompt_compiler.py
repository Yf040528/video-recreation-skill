def yn(v): return "YES" if v else "NO"

def compile_prompt(t):
    p=t["presence_map"]; gm=t["global_master"]
    hand=gm.get("hand_master",{})
    product=gm.get("product_master",{})
    clothing=gm.get("clothing_master",{})
    env=gm.get("environment_master",{})
    lines=[
f"""[OUTPUT CONTRACT]
Generate exactly ONE independent vertical image for {t['task_id']}.
ASSET_COUNT = 1.
NO collage. NO triptych. NO split-screen. NO contact sheet. NO comparison board.
Do not add labels or task names into the image.

[SOURCE SEMANTIC FUNCTION]
{t['semantic_function']}

[PRESENCE MAP — HARD GATE]
HAND = {yn(p['hand'])}
PRODUCT = {yn(p['product'])}
CLOTHING = {yn(p['clothing'])}
TEMPLE = {yn(p['temple'])}

Presence rules override Master availability.
A GLOBAL MASTER does NOT authorize an element to appear.
If PRESENCE = NO, that element MUST NOT appear in the output.
"""
    ]
    if p["hand"]:
        lines.append(f"""[HAND MASTER — ACTIVE]
{hand.get('description','')}
AUTHORIZED_HAND_COUNT = {hand.get('authorized_hand_count',1)}
No extra hands, detached fingers, duplicated limbs or anatomy errors.""")
    else:
        lines.append("[HAND — FORBIDDEN]\nNo human hand, arm, wrist, fingers or nails may appear.")

    if p["product"]:
        lines.append(f"""[PRODUCT MASTER — ACTIVE]
{product.get('description','')}
Use TARGET PRODUCT only.
Source product reappearance is forbidden.
Preserve product component structure, order, material, geometry and physical fit.""")
    else:
        lines.append("[PRODUCT — FORBIDDEN]\nNo bracelet, jewelry product, product charm or product display may appear.")

    if p["clothing"]:
        lines.append(f"""[CLOTHING MASTER — ACTIVE]
{clothing.get('description','')}
Use TARGET CLOTHING only. Source clothing reappearance is forbidden.""")
    else:
        lines.append("[CLOTHING — NOT REQUIRED]\nDo not invent sleeves or garments merely because a clothing master exists.")

    if p["temple"]:
        lines.append(f"""[ENVIRONMENT / TEMPLE — ACTIVE]
{env.get('temple_description','Create a clearly recreated temple/architecture environment while preserving the shot function.')}
No hand or product may be introduced unless Presence Map explicitly enables them.""")
    else:
        lines.append("[TEMPLE — NOT REQUIRED]\nDo not force temple architecture into this shot.")

    lines.append("[MANDATORY REPLACEMENTS]\n"+"\n".join("- "+x for x in t.get("mandatory_replacements",[])))
    lines.append("[PRESERVE]\n"+"\n".join("- "+x for x in t.get("preserve",[])))
    lines.append("[CREATIVE DELTA]\n"+"\n".join("- "+x for x in t.get("creative_delta",[])))
    lines.append("""[FINAL NEGATIVE CONSTRAINTS]
Never infer that every Master must appear in every shot.
Never turn an environment-only source into a product shot.
Never generate more than one output image.
Never create a multi-panel layout.
No unauthorized text.

[FINAL]
ONE TASK -> ONE IMAGE -> ONE OUTPUT ASSET.""")
    return "\n\n".join(lines)
