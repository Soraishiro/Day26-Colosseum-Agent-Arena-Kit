import json
from eval.prosecute import load_fixtures, prosecute

fixtures = load_fixtures()
# Find false claims for remaining issues
issues = {
    'non_responsive': [],
    'stale_read': [],
    'unsupported_precision': [],
    'wasteful': [],
}

for fx in fixtures:
    result = prosecute(fx['trace'], fx['answer'], fx['card'])
    for claim in result['claims']:
        cls = claim['cls']
        present = fx.get('label', {}).get('present_classes', {})
        expected = cls in present
        if not expected and cls in issues:
            issues[cls].append(fx['fixture_id'])

for cls, fids in issues.items():
    if fids:
        print(f"\n=== FALSE {cls} on: {fids} ===")
        for fx in fixtures:
            if fx['fixture_id'] in fids:
                print(f"  --- {fx['fixture_id']} ---")
                print(f"    answer: {fx['answer'].get('text','')[:120]}")
                print(f"    card.ask: {json.dumps(fx['card'].get('ask', {}))[:150]}")

# Also check missing detections
print("\n=== MISSED detections ===")
for fx in fixtures:
    result = prosecute(fx['trace'], fx['answer'], fx['card'])
    claimed = {c['cls'] for c in result['claims']}
    for cls in fx.get('label', {}).get('present_classes', {}):
        if cls not in claimed:
            print(f"  MISSED {cls} on {fx['fixture_id']}")
            print(f"    answer: {fx['answer'].get('text','')[:120]}")
