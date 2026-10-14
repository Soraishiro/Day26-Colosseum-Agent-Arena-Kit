import json

# Look at all fixtures for specific classes more carefully
for fname, ids in [
    ('family_a_infrastructure.jsonl', ['write_violation__near_miss', 'write_violation__positive']),
    ('family_b_truth.jsonl', ['ungrounded__positive', 'unsupported_precision__positive', 'wrong_answer__positive']),
    ('family_c_safety.jsonl', ['guardrail_breach__positive']),
    ('family_d_quality.jsonl', ['incoherent__positive', 'unflagged_conflict__positive']),
    ('family_e_economy.jsonl', ['wasteful__positive']),
]:
    with open(f'fixtures/prosecution/labelled/{fname}') as f:
        for line in f:
            fx = json.loads(line.strip())
            if fx['fixture_id'] in ids:
                print(f'=== {fx["fixture_id"]} ===')
                print(f'  description: {fx.get("description", "")}')
                print(f'  proof_refs: {fx["label"]["present_classes"][fx["primary_class"]]["proof_refs"]}')
                for ev in fx['trace']:
                    t = ev.get('type')
                    p = ev.get('p', {})
                    seq = ev.get('seq')
                    if t == 'command':
                        print(f'  seq={seq} command: server={p.get("server")} tool={p.get("tool")} args={json.dumps(p.get("args"))} headers={json.dumps(p.get("headers"))} fields={p.get("fields")}')
                    elif t == 'tool_call':
                        print(f'  seq={seq} tool_call: server={p.get("server")} tool={p.get("tool")} headers={json.dumps(p.get("headers", {}))} fields={p.get("fields")}')
                    elif t == 'tool_result':
                        anchors = p.get('anchors', [])
                        rows = p.get('rows', [])
                        partial = p.get('partial')
                        fields = p.get('fields')
                        print(f'  seq={seq} tool_result: anchors={anchors} partial={partial} fields={fields}')
                        if rows:
                            for r in rows:
                                print(f'    row: {json.dumps(r)[:200]}')
                    elif t == 'answer':
                        print(f'  seq={seq} answer: text={p.get("text","")[:120]}')
                    elif t in ('decision', 'enforced'):
                        print(f'  seq={seq} {t}: {json.dumps(p)[:150]}')
                    elif t == 'mutation':
                        print(f'  seq={seq} mutation: applied={p.get("applied")} trigger_matched={p.get("trigger_matched")} class={p.get("class")}')
                    elif t == 'exchange_start':
                        print(f'  seq={seq} exchange_start: defender={p.get("defender")} ask={json.dumps(p.get("ask"))[:150]}')
                    elif t == 'model_turn':
                        print(f'  seq={seq} model_turn: {json.dumps(p)[:150]}')
                print()
