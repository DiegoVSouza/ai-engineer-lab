"""Read phase triples and preserve every unchecked item in an audit inventory."""
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[3]
rows = []
for number in range(9):
    project = root / 'projects' / f'p{number:02}'
    for phase_root in (project / '.planning/phases', project / 'docs/harness/phases'):
        if not phase_root.exists():
            continue
        for verify in sorted(phase_root.rglob('VERIFY.md')):
            lines = verify.read_text(encoding='utf-8-sig').splitlines()
            rows.append(dict(project=project.name, path=verify.relative_to(root).as_posix(),
                             missing=[name for name in ('SPEC.md', 'PLAN.md') if not (verify.parent / name).is_file()],
                             open_items=[dict(line=i, text=line) for i, line in enumerate(lines, 1) if re.search(r'\[ \]', line)]))
result = dict(phase_count=len(rows), open_file_count=sum(bool(row['open_items']) for row in rows),
              open_item_count=sum(len(row['open_items']) for row in rows), phases=rows)
out = pathlib.Path(__file__).with_name('inventory.json')
out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps({key: value for key, value in result.items() if key != 'phases'}))
