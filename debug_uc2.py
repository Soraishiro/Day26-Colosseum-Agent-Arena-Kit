import json
from eval.prosecute import load_fixtures, prosecute, group_calls

fixtures = load_fixtures()
for fx in fixtures:
    if 'unflagged_conflict' in fx.get('label', {}).get('present_classes', {}):
        print(f"=== {fx['fixture_id']} ===")
        for g in group_calls(fx['trace']):
            if g.tool_result:
                p = g.tool_result.get('p', {})
                print(f"  seq={g.tool_result['seq']} tool_result: anchors={p.get('anchors')} rows={json.dumps(p.get('rows', []))[:200]}")
        answer = fx['answer']
        print(f"  answer.text: {answer.get('text','')[:120]}")
        print(f"  proof_refs: {fx['label']['present_classes']['unflagged_conflict']['proof_refs']}")
        print()
