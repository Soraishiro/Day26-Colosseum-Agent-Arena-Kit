import json

for fname, ids in [
    ('family_a_infrastructure.jsonl', ['write_violation__positive', 'protocol_misuse__positive']),
    ('family_b_truth.jsonl', ['fabricated_citation__positive']),
    ('family_c_safety.jsonl', ['authority_exceeded__positive', 'privacy_leak__positive']),
]:
    with open(f'fixtures/prosecution/labelled/{fname}') as f:
        for line in f:
            fx = json.loads(line.strip())
            if fx['fixture_id'] in ids:
                print(f'=== {fx["fixture_id"]} ===')
                for ev in fx['trace']:
                    t = ev.get('type')
                    p = ev.get('p', {})
                    seq = ev.get('seq')
                    if t == 'tool_call':
                        print(f'  seq={seq} tool_call: headers={json.dumps(p.get("headers", {}))} fields={p.get("fields")} server={p.get("server")} tool={p.get("tool")}')
                    elif t == 'tool_result':
                        anchors = p.get('anchors', [])
                        partial = p.get('partial')
                        fields = p.get('fields')
                        n_rows = p.get('n_rows')
                        rows = p.get('rows', [])
                        private = p.get('private')
                        print(f'  seq={seq} tool_result: anchors={anchors} partial={partial} fields={fields} n_rows={n_rows} private={private}')
                        if rows:
                            print(f'    rows: {json.dumps(rows)[:300]}')
                    elif t == 'answer':
                        print(f'  seq={seq} answer: cited_anchors={p.get("cited_anchors")} text={p.get("text","")[:100]}')
                    elif t in ('command', 'decision', 'enforced'):
                        print(f'  seq={seq} {t}: {json.dumps(p)[:200]}')
                    elif t == 'mutation':
                        print(f'  seq={seq} mutation: {json.dumps(p)[:200]}')
                    else:
                        print(f'  seq={seq} {t}: {json.dumps(p)[:150]}')
                print()
