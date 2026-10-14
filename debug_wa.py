import json
from eval.prosecute import load_fixtures, group_calls
fixtures = load_fixtures()
for fx in fixtures:
    if 'wrong_answer' in fx.get('label', {}).get('present_classes', {}):
        print(f"=== {fx['fixture_id']} ===")
        for g in group_calls(fx['trace']):
            if g.tool_result:
                p = g.tool_result.get('p', {})
                print(f"  tool_result seq={g.tool_result['seq']}: anchors={p.get('anchors')} rows={json.dumps(p.get('rows', []))[:200]}")
        print(f"  answer: {fx['answer']['text']}")
        print(f"  proof_refs: {fx['label']['present_classes']['wrong_answer']['proof_refs']}")
        print()
