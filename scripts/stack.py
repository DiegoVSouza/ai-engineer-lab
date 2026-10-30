"""Operate only the root SupportOps Compose application."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
COMPOSE = ['docker', 'compose', '--project-directory', str(ROOT), '-f', str(ROOT/'docker-compose.yml')]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['checkout','up','down','status','logs','stop','start','check','persistence','credentials','token','ca'])
    parser.add_argument('extra',nargs='*')
    args=parser.parse_args()
    if args.action=='checkout':
        manifest=json.loads((ROOT/'ops/stack/projects.lock.json').read_text())
        for name,item in manifest.items():
            target=ROOT/'projects'/name
            if not target.exists():
                subprocess.run(['git','clone','--no-checkout',item['url'],str(target)],check=True)
                subprocess.run(['git','-C',str(target),'checkout','--detach',item['commit']],check=True)
            actual=subprocess.check_output(['git','-C',str(target),'rev-parse','HEAD'],text=True).strip()
            if actual!=item['commit']:
                raise RuntimeError(f'{name} differs from projects.lock.json; preserve existing work and select its revision explicitly')
            print(f'{name}: pinned checkout verified')
        return 0
    if args.action=='up':
        command=COMPOSE+['up','-d','--build','--wait','--wait-timeout','300']
    elif args.action=='down':
        # Removes only this Compose application's containers and networks. Named
        # volumes survive unless the caller passes --volumes explicitly, so
        # `down` followed by `up` is a non-destructive restart.
        command=COMPOSE+['down','--remove-orphans']+args.extra
    elif args.action in {'check','persistence','credentials','token','ca'}:
        command=COMPOSE+['--profile','tools','run','--rm','--no-deps','tools',args.action]+args.extra
    elif args.action=='status':
        command=COMPOSE+['ps','--all']
    elif args.action=='logs':
        command=COMPOSE+['logs','--tail','80']+args.extra
    else:
        command=COMPOSE+[args.action]+args.extra
    return subprocess.run(command,cwd=ROOT).returncode


if __name__=='__main__':
    sys.exit(main())
