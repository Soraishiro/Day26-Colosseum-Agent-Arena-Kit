import json

all_fixtures = []
for fname in ['clean.jsonl', 'family_a_infrastructure.jsonl', 'family_b_truth.jsonl',
              'family_c_safety.jsonl', 'family_d_quality.jsonl', 'family_e_economy.jsonl']:
    with open(f'fixtures/prosecution/labelled/{fname}') as f:
        for line in f:
            line = line.strip()
            if line:
                all_fixtures.append(json.loads(line))

# For each class, show both positive and near_miss side by side
by_class = {}
for fx in all_fixtures:
    for cls in fx.get('label', {}).get('present_classes', {}):
        by_class.setdefault(cls, []).append(fx)

for cls in sorted(by_class.keys()):
    if cls in ('enforcement_failure',):  # already implemented
        continue
    fxs = by_class[cls]
    print(f'=== {cls} ===')
    for fx in fxs:
        present = fx['label']['present_classes'][cls]
        proof_refs = present.get('proof_refs', [])
        card = fx.get('card', {})
        print(f'  [{fx["fixture_id"]}] proof_refs={proof_refs}')
        # Show tool_call and answer details
        for e in fx['trace']:
            p = e.get('p', {})
            t = e.get('type')
            seq = e.get('seq')
            if t == 'tool_call':
                print(f'    [{t} seq={seq}] server={p.get("server")} tool={p.get("tool")} mask={p.get("mask")} lease={p.get("lease_used")} hdrs={sorted(p.get("headers",{}).keys())}')
            elif t == 'answer':
                print(f'    [{t} seq={seq}] text={p.get("text","")[:80]}')
                print(f'    [{t} seq={seq}] cited={p.get("cited_anchors")}')
            elif t == 'enforced':
                print(f'    [{t} seq={seq}] verdict={p.get("verdict_applied")}')
            elif t == 'mutation':
                print(f'    [{t} seq={seq}] applied={p.get("applied")} op={p.get("op")} class={p.get("class")}')
            elif t == 'exchange_start':
                print(f'    [{t} seq={seq}] defender={p.get("defender")} ask={p.get("ask")}')
        print()
