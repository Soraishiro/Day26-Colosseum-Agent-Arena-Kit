import json
from collections import Counter

all_fixtures = []
for fname in ['clean.jsonl', 'family_a_infrastructure.jsonl', 'family_b_truth.jsonl',
              'family_c_safety.jsonl', 'family_d_quality.jsonl', 'family_e_economy.jsonl']:
    with open(f'fixtures/prosecution/labelled/{fname}') as f:
        for line in f:
            line = line.strip()
            if line:
                all_fixtures.append(json.loads(line))

# Group by class
by_class = {}
for fx in all_fixtures:
    for cls in fx.get('label', {}).get('present_classes', {}):
        by_class.setdefault(cls, []).append(fx)

for cls, fxs in sorted(by_class.items()):
    print(f'=== {cls} ({len(fxs)} fixtures) ===')
    for fx in fxs:
        card = fx.get('card', {})
        present = fx['label']['present_classes']
        proof_refs = present[cls].get('proof_refs', [])
        detail = present[cls].get('detail', '')[:80]
        mut = card.get('mutation', {}) or {}
        print(f'  {fx["fixture_id"]}')
        print(f'    proof_refs: {proof_refs}')
        print(f'    detail: {detail}')
        print(f'    card.class={card.get("class")} op={mut.get("op")} defense_event={card.get("defense_event")}')

print("\n=== ALL present_classes across fixtures ===")
all_classes = Counter()
for fx in all_fixtures:
    for cls in fx.get('label', {}).get('present_classes', {}):
        all_classes[cls] += 1
for cls, count in sorted(all_classes.items()):
    print(f'  {cls}: {count}')
