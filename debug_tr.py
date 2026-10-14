import json
from eval.prosecute import load_fixtures
fixtures = load_fixtures()
for fid in ['ungrounded__positive', 'ungrounded__near_miss']:
    for fx in fixtures:
        if fx['fixture_id'] == fid:
            print(f"=== {fx['fixture_id']} ===")
            for ev in fx['trace']:
                t = ev.get('type')
                p = ev.get('p', {})
                if t == 'tool_result':
                    print(f"  seq={ev['seq']} tool_result: {json.dumps(p)[:300]}")
                elif t == 'tool_call':
                    print(f"  seq={ev['seq']} tool_call: {json.dumps(p)[:200]}")
            print()
