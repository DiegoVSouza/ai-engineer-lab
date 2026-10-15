"""Configure isolated local Git repositories and install the lab commit skill."""
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def configure(root):
    root = root.resolve()
    if not (root / '.git').exists():
        git(root, 'init', '-b', 'main')
    else:
        # A partial setup may have initialized the repository before failing.
        # Preserve its history and normalize only the branch when it is unborn.
        branch = subprocess.run(['git', '-C', str(root), 'symbolic-ref', '--short', 'HEAD'], capture_output=True, text=True)
        if branch.returncode == 0 and branch.stdout.strip() != 'main':
            raise RuntimeError(f'Repository already has branch {branch.stdout.strip()!r}; refusing to rename it')
    if pathlib.Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root:
        raise RuntimeError(f'Wrong repository root: {root}')
    if git(root, 'config', '--local', '--get', 'core.hooksPath') if subprocess.run(['git', '-C', str(root), 'config', '--local', '--get', 'core.hooksPath'], capture_output=True).returncode == 0 else False:
        raise RuntimeError(f'Existing hooksPath needs review: {root}')
    for relative, source in [('.githooks/commit-msg', ROOT / 'harness-kit/git/commit-msg'), ('scripts/validate_commit.py', ROOT / 'harness-kit/git/validate_commit.py'), ('.agents/skills/lab-commits/SKILL.md', ROOT / 'harness/skills/lab-commits/SKILL.md')]:
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and destination.read_bytes() != source.read_bytes():
            raise RuntimeError(f'Refusing overwrite: {destination}')
        if not destination.exists():
            shutil.copyfile(source, destination)
    git(root, 'config', '--local', 'core.hooksPath', '.githooks')
    git(root, 'config', '--local', 'core.autocrlf', 'false')
    if root == ROOT:
        ignore = root / '.gitignore'
        lines = ignore.read_text(encoding='utf-8').splitlines() if ignore.exists() else []
        if 'projects/' not in lines:
            lines.append('projects/')
            ignore.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(root, git(root, 'config', 'user.name'), 'hooks=.githooks')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-dir', type=pathlib.Path)
    args = parser.parse_args()
    if args.project_dir:
        configure(args.project_dir)
    else:
        configure(ROOT)
        for project in sorted((ROOT / 'projects').iterdir()):
            if project.is_dir():
                configure(project)
