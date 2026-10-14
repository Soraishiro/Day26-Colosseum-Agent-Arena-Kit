import json
from pathlib import Path
base = Path('fixtures/prosecution/labelled')
# Read stale_read positive and a few others to see event structure
targets = [
    ('family_a_infrastructure.jsonl', 'stale_read__positive'),
    ('family_b_truth.jsonl', 'ungrounded__positive'),
    ('family_c_safety.jsonl', 'authority_exceeded__positive'),
    ('family_d_quality.jsonl', 'incoherent__positive'),
    ('family_e_economy.jsonl', 'wasteful__positive'),
]
for fname, fid in targets:
    for line in (base / fname).read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        fx = json.loads(line)
        if fx['fixture_id'] == fid:
            print(f'=== {fid} ===')
            for e in fx['trace']:
                seq = e.get('seq', '?')
                t = e['type']
                p = e['p']
                # Print interesting fields
                if t == 'exchange_start':
                    print(f'  seq={seq} type={t} defender={p.get("defender")} ask.type={p.get("ask",{}).get("type")}')
                elif t == 'command':
                    print(f'  seq={seq} type={t} server={p.get("server")} tool={p.get("tool")} headers={p.get("headers")} lease_id={p.get("lease_id")} args={p.get("args")}')
                elif t == 'tool_call':
                    print(f'  seq={seq} type={t} server={p.get("server")} tool={p.get("tool")} mask={p.get("mask")}')
                elif t == 'tool_result':
                    print(f'  seq={seq} type={t} anchors={p.get("anchors")} partial={p.get("partial")} rows={p.get("rows")}')
                elif t == 'answer':
                    print(f'  seq={seq} type={t} cited={p.get("cited_anchors")} text={p.get("text")[:80]}')
                elif t == 'enforced':
                    print(f'  seq={seq} type={t} verdict_applied={p.get("verdict_applied")}')
                elif t == 'mutation':
                    print(f'  seq={seq} type={t} class={p.get("class")} applied={p.get("applied")}')
                else:
                    print(f'  seq={seq} type={t}')
            print(f'  answer_extra: {json.dumps(fx["answer"], ensure_ascii=False)[:200]}')
            print()
            break
