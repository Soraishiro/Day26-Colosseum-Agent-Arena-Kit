import json
from eval.prosecute import load_fixtures, group_calls
fixtures = load_fixtures()
for fx in fixtures:
    if fx['fixture_id'] in ['ungrounded__positive', 'ungrounded__near_miss']:
        print(f"=== {fx['fixture_id']} ===")
        for g in group_calls(fx['trace']):
            if g.command and g.command.get('p', {}).get('tool') == 'get_frame':
                cmd_p = g.command.get('p', {})
                tc_p = g.tool_call.get('p', {}) if g.tool_call else {}
                print(f"  cmd fields={cmd_p.get('fields')} mask={cmd_p.get('mask')}")
                print(f"  tc fields={tc_p.get('fields')} mask={tc_p.get('mask')}")
        print(f"  answer: {fx['answer']['text'][:100]}")
        print()
