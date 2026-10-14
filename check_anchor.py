import json

with open('fixtures/prosecution/labelled/family_a_infrastructure.jsonl') as f:
    for line in f:
        fx = json.loads(line.strip())
        if fx['fixture_id'] == 'protocol_misuse__near_miss':
            print(f'=== {fx["fixture_id"]} ===')
            for ev in fx['trace']:
                t = ev.get('type')
                p = ev.get('p', {})
                seq = ev.get('seq')
                if t == 'command':
                    print(f'  seq={seq} command: {json.dumps(p)}')
                elif t == 'tool_call':
                    print(f'  seq={seq} tool_call: {json.dumps(p)}')
                elif t == 'tool_result':
                    print(f'  seq={seq} tool_result: {json.dumps(p)}')
                elif t == 'answer':
                    print(f'  seq={seq} answer: {json.dumps(p)}')

# Also check the Anchor class
print()
print("=== Anchor class ===")
try:
    from kit.world.anchor import Anchor, NAMESPACES
    print("NAMESPACES:", NAMESPACES)
    a = Anchor.parse("Frame:d8f95a7b/c/031")
    print(f"parsed: {a}")
    print(f"path_id: {a.path_id}")
    print(f"rev: {a.rev}")
    print(f"idx: {a.idx}")
except Exception as e:
    print(f"Anchor import failed: {e}")

# Check what kit.world is available
print()
print("=== kit.world contents ===")
import os
world_dir = 'kit/world/df8c55dabb35'
for f in os.listdir(world_dir):
    print(f"  {f}")
