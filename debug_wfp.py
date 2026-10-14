import json
from eval.prosecute import load_fixtures
fixtures = load_fixtures()
for fx in fixtures:
    if fx['fixture_id'] == 'wasteful__positive':
        print(f"ask: {json.dumps(fx['card'].get('ask', {}))}")
        print(f"answer: {fx['answer']['text']}")
        print(f"cited: {fx['answer'].get('cited_anchors')}")
