from eval.prosecute import prosecute, load_fixtures, score_prosecutor
fixtures = load_fixtures()
report = score_prosecutor(prosecute, fixtures)
print(f"filed: {report['filed']} verified: {report['verified']} false: {report['false']} rejected: {report['rejected']}")
print()
for cls, stats in report['per_class'].items():
    if stats['present'] or stats['claimed']:
        print(f"{cls:<24} present={stats['present']} claimed={stats['claimed']} verified={stats['verified']} false={stats['false']} recall={stats['recall']:.2f}")
