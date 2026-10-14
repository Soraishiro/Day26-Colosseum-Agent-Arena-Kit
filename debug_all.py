import json
from eval.prosecute import load_fixtures, prosecute

fixtures = load_fixtures()
# Find all non-responsive false claims
for fx in fixtures:
    result = prosecute(fx['trace'], fx['answer'], fx['card'])
    for claim in result['claims']:
        if claim['cls'] == 'non_responsive':
            present = fx.get('label', {}).get('present_classes', {})
            expected = 'non_responsive' in present
            if not expected:
                print(f"FALSE non_responsive on {fx['fixture_id']}: require={fx['card'].get('ask',{}).get('require')}")
                print(f"  answer text: {fx['answer'].get('text','')[:100]}")
                print()

# Check ungrounded
print("\n=== UNFELTUNGROUNDED ===")
for fx in fixtures:
    result = prosecute(fx['trace'], fx['answer'], fx['card'])
    for claim in result['claims']:
        if claim['cls'] == 'ungrounded':
            present = fx.get('label', {}).get('present_classes', {})
            expected = 'ungrounded' in present
            status = "OK" if expected else "FALSE"
            print(f"{status} ungrounded on {fx['fixture_id']}")
            for ev in fx['trace']:
                if ev.get('type') == 'command':
                    print(f"  cmd: tool={ev['p'].get('tool')} fields={ev['p'].get('fields')}")
                elif ev.get('type') == 'tool_call':
                    print(f"  tool_call: tool={ev['p'].get('tool')} mask={ev['p'].get('mask')}")
