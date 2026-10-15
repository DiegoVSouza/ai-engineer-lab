"""Configure isolated local Git repositories and install the lab commit skill."""
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]


def git(root, *args):
    return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def configure(root):
    root = root.resolve()
    if not (root / '.git').exists():
        git(root, 'init', '-b', 'main')
    else:
        # A partial setup may have initialized an empty repository on Git's
        # default branch. Normalize it to the required branch without touching
        # files or history.
        branch = subprocess.run(['git', 'symbolic-ref', '--short', 'HEAD'], cwd=root, capture_output=True, text=True)
        if branch.returncode == 0 and branch.stdout.strip() != 'main':
            head = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'], cwd=root, capture_output=True, text=True)
            if head.returncode == 0:
                existing_main = subprocess.run(['git', 'show-ref', '--verify', '--quiet', 'refs/heads/main'], cwd=root)
                if existing_main.returncode == 0:
                    raise RuntimeError(f'Cannot rename {branch.stdout.strip()!r} to main because a main branch already exists: {root}')
                git(root, 'branch', '-M', 'main')
            else:
                git(root, 'symbolic-ref', 'HEAD', 'refs/heads/main')
    if pathlib.Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root:
        raise RuntimeError(f'Wrong repository root: {root}')
    configured_hooks = subprocess.run(['git', 'config', '--local', '--get', 'core.hooksPath'], cwd=root, capture_output=True, text=True)
    if configured_hooks.returncode == 0 and configured_hooks.stdout.strip() not in ('.githooks',):
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
        if not any(line.lstrip('/') == 'projects/' for line in lines):
            lines.append('projects/')
            ignore.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    identity = subprocess.run(['git', 'var', 'GIT_AUTHOR_IDENT'], cwd=root, capture_output=True, text=True)
    if identity.returncode:
        raise RuntimeError(f'Git author identity is not configured for {root}: {identity.stderr.strip()}')
    print(root, identity.stdout.strip(), 'hooks=.githooks')


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
