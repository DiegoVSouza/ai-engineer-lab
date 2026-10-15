"""Prepare P00-P05 scaffolds without implementing portfolio products."""
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('harness_init', ROOT / 'harness-kit/bootstrap/harness_init.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

PROFILES = {'p00': 'workflow-automation', 'p01': 'agent-app', 'p02': 'eval-infra', 'p03': 'eval-infra', 'p04': 'workflow-automation', 'p05': 'agent-saas'}

for pid, profile in PROFILES.items():
    project = ROOT / 'projects' / pid
    project.mkdir(exist_ok=True)
    if any(project.iterdir()):
        raise RuntimeError(f'Expected empty project directory: {project}')
    config = yaml.safe_load((ROOT / f'harness-kit/profiles/{profile}.yaml').read_text(encoding='utf-8'))
    config['project']['name'] = pid
    if pid == 'p01':
        config['product']['multi_agent'] = 'research-orchestrator'
    if pid == 'p05':
        config['product']['rag'] = True
    (project / 'harness.yaml').write_text(yaml.safe_dump(config, sort_keys=False), encoding='utf-8')
    module.initialize(project)
    (project / '.gitignore').write_text('__pycache__/\n*.py[cod]\n.venv/\n.env\n.env.*\n!.env.example\n*.pem\n*.key\n.pytest_cache/\n.ruff_cache/\n', encoding='utf-8')
    brief = next((ROOT / 'specs').glob(f'{pid.upper()}-*.md'))
    (project / 'docs/intake').mkdir(parents=True)
    shutil.copyfile(brief, project / 'docs/intake/ORIGINAL-BRIEF.md')
    with (project / 'AGENTS.md').open('a', encoding='utf-8') as stream:
        stream.write('\n## Lab project rules\n\nRead ../../AGENTS.md and .agents/skills/lab-commits/SKILL.md. This directory is the only authorized product write root. Adapt docs/intake/ORIGINAL-BRIEF.md into local SDD phases before implementation; original root-relative paths must be mapped inside this repository. Keep all planning, sources.lock.json, evidence, knowledge docs, and code here. Commit each completed logical task locally using Conventional Commits. Never import a sibling source tree; use versioned packages or documented local test doubles until integration. The generated check_full.py is a placeholder: it cannot satisfy a product gate.\n')
    subprocess.run([sys.executable, str(ROOT / 'scripts/harness/setup-project-git.py'), '--project-dir', str(project)], check=True)
    subprocess.run(['git', '-C', str(project), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(project), 'commit', '-m', f'chore({pid}): initialize independent project harness'], check=True)
