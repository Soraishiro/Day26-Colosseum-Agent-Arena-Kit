import json
from eval.prosecute import load_fixtures

fixtures = load_fixtures()
for fx in fixtures:
    if 'non_responsive' in fx.get('label', {}).get('present_classes', {}):
        print(f"=== {fx['fixture_id']} ===")
        print(f"  card.ask: {json.dumps(fx['card'].get('ask', {}))}")
        print(f"  answer.text: {fx['answer'].get('text','')[:120]}")
        print(f"  answer.cited_anchors: {fx['answer'].get('cited_anchors', [])}")
        print()
