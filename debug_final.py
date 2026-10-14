import json
from eval.prosecute import load_fixtures, prosecute

fixtures = load_fixtures()
for fx in fixtures:
    result = prosecute(fx['trace'], fx['answer'], fx['card'])
    for claim in result['claims']:
        cls = claim['cls']
        present = fx.get('label', {}).get('present_classes', {})
        expected = cls in present
        if not expected:
            print(f"FALSE {cls} on {fx['fixture_id']}: evidence={claim['evidence']}")
            print(f"  answer: {fx['answer'].get('text','')[:100]}")
            print(f"  card.ask: {json.dumps(fx['card'].get('ask', {}))[:150]}")
            print()
