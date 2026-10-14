import json
from pathlib import Path
base = Path('fixtures/prosecution/labelled')
targets = [
    ('family_c_safety.jsonl', 'privacy_leak__positive'),
    ('family_c_safety.jsonl', 'guardrail_breach__positive'),
    ('family_b_truth.jsonl', 'hallucination__positive'),
    ('family_b_truth.jsonl', 'unsupported_precision__positive'),
    ('family_d_quality.jsonl', 'unflagged_conflict__positive'),
    ('family_d_quality.jsonl', 'overreach__positive'),
    ('family_d_quality.jsonl', 'non_responsive__positive'),
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
                if t == 'exchange_start':
                    print(f'  seq={seq} type={t} ask.type={p.get("ask",{}).get("type")} ask.require={p.get("ask",{}).get("require")}')
                elif t == 'command':
                    print(f'  seq={seq} type={t} server={p.get("server")} tool={p.get("tool")} fields={p.get("fields")} headers={p.get("headers")}')
                elif t == 'tool_call':
                    print(f'  seq={seq} type={t} mask={p.get("mask")}')
                elif t == 'tool_result':
                    print(f'  seq={seq} type={t} anchors={p.get("anchors")} rows={p.get("rows")}')
                elif t == 'answer':
                    print(f'  seq={seq} type={t} cited={p.get("cited_anchors")}')
                    print(f'    answer.text={p.get("text")[:120]}')
            print(f'  answer_extra: {json.dumps(fx["answer"], ensure_ascii=False)[:300]}')
            print()
            break
