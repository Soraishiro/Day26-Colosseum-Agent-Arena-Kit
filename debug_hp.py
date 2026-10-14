import json
from eval.prosecute import load_fixtures, prosecute

fixtures = load_fixtures()
for fx in fixtures:
    result = prosecute(fx['trace'], fx['answer'], fx['card'])
    for claim in result['claims']:
        if claim['cls'] in ('hallucination', 'unsupported_precision'):
            present = fx.get('label', {}).get('present_classes', {})
            expected = claim['cls'] in present
            if not expected:
                print(f"FALSE {claim['cls']} on {fx['fixture_id']}: proof_refs={claim['evidence']}")
                print(f"  answer: {fx['answer'].get('text','')[:120]}")
                print()
