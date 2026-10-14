import json

all_fixtures = []
for fname in ['family_a_infrastructure.jsonl', 'family_b_truth.jsonl', 'family_c_safety.jsonl',
              'family_d_quality.jsonl', 'family_e_economy.jsonl']:
    with open(f'fixtures/prosecution/labelled/{fname}') as f:
        for line in f:
            line = line.strip()
            if line:
                all_fixtures.append(json.loads(line))

# Look at each positive fixture in detail
for fx in all_fixtures:
    present = fx.get('label', {}).get('present_classes', {})
    if not present:
        continue
    cls = list(present.keys())[0]
    if 'positive' not in fx['fixture_id']:
        continue
    
    print(f'=== {cls} (positive) ===')
    print(f'  fixture_id: {fx["fixture_id"]}')
    card = fx.get('card', {})
    print(f'  card.class={card.get("class")}, defense_event={card.get("defense_event")}')
    
    # Show the trace structure
    for e in fx['trace']:
        p = e.get('p', {})
        t = e.get('type')
        seq = e.get('seq')
        parts = [f'seq={seq}']
        if t == 'command':
            parts.append(f'server={p.get("server")} tool={p.get("tool")}')
            parts.append(f'args={p.get("args")}')
            parts.append(f'headers={p.get("headers")}')
        elif t == 'tool_call':
            parts.append(f'server={p.get("server")} tool={p.get("tool")}')
            parts.append(f'mask={p.get("mask")}')
            parts.append(f'replica={p.get("replica")} lease={p.get("lease_used")}')
            parts.append(f'headers={sorted(p.get("headers",{}).keys())}')
        elif t == 'tool_result':
            parts.append(f'ok={p.get("ok")} anchors={p.get("anchors")} n_rows={p.get("n_rows")}')
            if p.get('rows'):
                parts.append(f'rows_keys={list(p.get("rows")[0].keys()) if p.get("rows") else []}')
        elif t == 'enforced':
            parts.append(f'verdict={p.get("verdict_applied")} charged={p.get("charged")}')
        elif t == 'mutation':
            parts.append(f'applied={p.get("applied")} class={p.get("class")} op={p.get("op")}')
        elif t == 'answer':
            txt = p.get("text", "")[:60]
            parts.append(f'text={txt}')
            parts.append(f'cited={p.get("cited_anchors")}')
        elif t == 'exchange_start':
            parts.append(f'attacker={p.get("attacker")} defender={p.get("defender")}')
            parts.append(f'ask={p.get("ask")}')
        else:
            parts.append(f'p_keys={sorted(p.keys())}')
        print(f'  [{t}] {" ".join(parts)}')
    print()
