import json
from eval.prosecute import load_fixtures
fixtures = load_fixtures()
for fx in fixtures:
    if fx['fixture_id'] in ('incoherent__positive', 'stale_read__positive'):
        print(f"{fx['fixture_id']}:")
        print(f"  answer keys: {list(fx['answer'].keys())}")
        print(f"  answer.fresher: {fx['answer'].get('fresher')}")
        print(f"  answer.c_anchor: {fx['answer'].get('c_anchor')}")
        print(f"  answer.cited_anchors: {fx['answer'].get('cited_anchors')}")
        print()
