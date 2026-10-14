import json
from eval.prosecute import load_fixtures, _parse_frame_anchor

fixtures = load_fixtures()
for fx in fixtures:
    if 'stale_read' in fx.get('label', {}).get('present_classes', {}):
        print(f"=== {fx['fixture_id']} ===")
        answer = fx['answer']
        print(f"  answer.cited_anchors: {answer.get('cited_anchors')}")
        print(f"  answer.fresher: {answer.get('fresher')}")
        print(f"  answer.c_anchor: {answer.get('c_anchor')}")
        print(f"  answer.w_anchor: {answer.get('w_anchor')}")
        card_ask = fx['card'].get('ask', {})
        print(f"  card.ask: {json.dumps(card_ask)[:200]}")
        for a in answer.get('cited_anchors') or []:
            parsed = _parse_frame_anchor(a)
            print(f"  parsed {a}: {parsed}")
        print()
