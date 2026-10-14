import json
from pathlib import Path
base = Path('fixtures/prosecution/labelled')
for f in sorted(base.glob('*.jsonl')):
    print(f'=== {f.name} ===')
    for line in f.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        fx = json.loads(line)
        print(f'  fixture_id={fx["fixture_id"]}, variant={fx["variant"]}, primary_class={fx["primary_class"]}')
        if fx['label']['present_classes']:
            for cls, info in fx['label']['present_classes'].items():
                print(f'    {cls}: proof_refs={info["proof_refs"]}')
