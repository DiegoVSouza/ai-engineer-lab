from pathlib import Path

root = Path(__file__).resolve().parents[4]
source = (root / "scripts/harness/test_migrate_local_operation.py").read_text(encoding="utf-8")
source = source.replace("import migrate_local_operation as migration", "import migrate_p01_operation as migration")
source = source.replace('account.reserve("p00", "historical", "case", 1, 1, 1475, 256)', 'account.reserve("p00", "local-live-operation-v1", "case", 1, 1, 1475, 256)')
source = source.replace('"projects/p00/scripts/campaign_execution.py"', '"projects/p00/scripts/campaign_execution.py"')
(root / "scripts/harness/test_migrate_p01_operation.py").write_text(source, encoding="utf-8", newline="\n")
