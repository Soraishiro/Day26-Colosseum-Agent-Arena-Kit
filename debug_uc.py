import json
from eval.prosecute import load_fixtures
fixtures = load_fixtures()
for fx in fixtures:
    if 'unflagged_conflict' in fx.get('label', {}).get('present_classes', {}):
        print(f"=== {fx['fixture_id']} ===")
        for ev in fx['trace']:
            t = ev.get('type')
            p = ev.get('p', {})
            seq = ev.get('seq')
            if t == 'tool_result':
                print(f"  seq={seq} tool_result: anchors={p.get('anchors')} rows={json.dumps(p.get('rows', []))[:300]}")
            elif t == 'answer':
                print(f"  seq={seq} answer: text={p.get('text','')[:120]}")
        print()
