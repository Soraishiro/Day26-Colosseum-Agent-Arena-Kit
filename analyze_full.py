import json
from kit.referee.rubric import DETERMINISTIC

all_fixtures = []
for fname in ['family_a_infrastructure.jsonl', 'family_b_truth.jsonl', 'family_c_safety.jsonl',
              'family_d_quality.jsonl', 'family_e_economy.jsonl']:
    with open(f'fixtures/prosecution/labelled/{fname}') as f:
        for line in f:
            line = line.strip()
            if line:
                all_fixtures.append(json.loads(line))

# For each deterministic class, show the full trace for the positive fixture
for cls in sorted(DETERMINISTIC):
    for fx in all_fixtures:
        present = fx.get('label', {}).get('present_classes', {})
        if cls in present and 'positive' in fx['fixture_id']:
            print(f'=== {cls} (positive: {fx["fixture_id"]}) ===')
            print(f'  proof_refs: {present[cls].get("proof_refs", [])}')
            for e in fx['trace']:
                p = e.get('p', {})
                t = e.get('type')
                seq = e.get('seq')
                if t == 'exchange_start':
                    print(f'  [{t} seq={seq}] defender={p.get("defender")} ask={p.get("ask")}')
                elif t == 'command':
                    print(f'  [{t} seq={seq}] server={p.get("server")} tool={p.get("tool")} args={p.get("args")} hdrs={p.get("headers")} ci={p.get("call_index")}')
                elif t == 'decision':
                    print(f'  [{t} seq={seq}] verdict={p.get("verdict")} quarantine={p.get("quarantine")}')
                elif t == 'enforced':
                    print(f'  [{t} seq={seq}] verdict_applied={p.get("verdict_applied")} charged={p.get("charged")}')
                elif t == 'mutation':
                    print(f'  [{t} seq={seq}] applied={p.get("applied")} class={p.get("class")} op={p.get("op")} trigger={p.get("trigger_matched")}')
                elif t == 'tool_call':
                    print(f'  [{t} seq={seq}] server={p.get("server")} tool={p.get("tool")} mask={p.get("mask")} lease={p.get("lease_used")} hdrs={p.get("headers")} replica={p.get("replica")}')
                elif t == 'tool_result':
                    print(f'  [{t} seq={seq}] ok={p.get("ok")} anchors={p.get("anchors")} n_rows={p.get("n_rows")}')
                    for row in p.get('rows', []):
                        print(f'    row: {row}')
                elif t == 'answer':
                    print(f'  [{t} seq={seq}] text={p.get("text","")[:100]}')
                    print(f'  [{t} seq={seq}] cited={p.get("cited_anchors")}')
                elif t == 'model_turn':
                    print(f'  [{t} seq={seq}] action={p.get("action_raw","")[:80]}')
                elif t == 'integrity':
                    print(f'  [{t} seq={seq}] kind={p.get("kind")}')
                else:
                    print(f'  [{t} seq={seq}] keys={sorted(p.keys())}')
            print()
