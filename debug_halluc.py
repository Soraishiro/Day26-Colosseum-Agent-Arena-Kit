import json
from eval.prosecute import load_fixtures, _text_of_tool_results

fixtures = load_fixtures()
for fx in fixtures:
    if 'hallucination' in fx.get('label', {}).get('present_classes', {}):
        print(f"=== {fx['fixture_id']} ===")
        print(f"  answer: {fx['answer']['text'][:120]}")
        print(f"  source text: {_text_of_tool_results(fx['trace'])[:200]}")
        print()

# Also check the false positives
print("\n=== False positive checks ===")
for fid in ['ungrounded__positive', 'ungrounded__near_miss', 'unsupported_precision__positive', 'privacy_leak__positive']:
    for fx in fixtures:
        if fx['fixture_id'] == fid:
            print(f"--- {fid} ---")
            print(f"  answer: {fx['answer']['text'][:120]}")
            print(f"  source: {_text_of_tool_results(fx['trace'])[:200]}")
