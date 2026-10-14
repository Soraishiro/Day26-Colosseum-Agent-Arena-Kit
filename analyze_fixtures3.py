import json

for fname, keys in [
    ('family_a_infrastructure.jsonl', ['stale_read__near_miss', 'write_violation__near_miss', 'protocol_misuse__near_miss']),
    ('family_b_truth.jsonl', ['hallucination__near_miss', 'ungrounded__near_miss', 'unsupported_precision__near_miss', 'wrong_answer__near_miss', 'fabricated_citation__near_miss']),
    ('family_c_safety.jsonl', ['guardrail_breach__near_miss', 'privacy_leak__near_miss', 'authority_exceeded__near_miss']),
    ('family_d_quality.jsonl', ['incoherent__near_miss', 'unflagged_conflict__near_miss', 'overreach__near_miss', 'non_responsive__near_miss']),
]:
    with open(f'fixtures/prosecution/labelled/{fname}') as f:
        for line in f:
            fx = json.loads(line.strip())
            if fx['fixture_id'] in keys:
                print(f'=== {fx["fixture_id"]} ===')
                print(f'  description: {fx.get("description", "")}')
                for ev in fx['trace']:
                    t = ev.get('type')
                    p = ev.get('p', {})
                    seq = ev.get('seq')
                    if t == 'command':
                        print(f'  seq={seq} command: server={p.get("server")} tool={p.get("tool")} args={json.dumps(p.get("args"))} headers={json.dumps(p.get("headers"))} fields={p.get("fields")}')
                    elif t == 'tool_call':
                        print(f'  seq={seq} tool_call: server={p.get("server")} tool={p.get("tool")} headers={json.dumps(p.get("headers", {}))} fields={p.get("fields")} replica={p.get("replica")} lease={p.get("lease_used")}')
                    elif t == 'tool_result':
                        anchors = p.get('anchors', [])
                        rows = p.get('rows', [])
                        partial = p.get('partial')
                        print(f'  seq={seq} tool_result: anchors={anchors} partial={partial} fields_mask={p.get("fields")} n_rows={p.get("n_rows")}')
                        if rows:
                            for r in rows[:1]:
                                print(f'    row: {json.dumps(r)[:300]}')
                    elif t == 'answer':
                        print(f'  seq={seq} answer: text={p.get("text","")[:120]} spans={p.get("spans")} cited={p.get("cited_anchors")}')
                    elif t in ('decision', 'enforced'):
                        print(f'  seq={seq} {t}: {json.dumps(p)[:150]}')
                    elif t == 'mutation':
                        print(f'  seq={seq} mutation: applied={p.get("applied")} trigger_matched={p.get("trigger_matched")}')
                    elif t == 'exchange_start':
                        print(f'  seq={seq} exchange_start: defender={p.get("defender")} ask={json.dumps(p.get("ask"))[:150]}')
                print()
