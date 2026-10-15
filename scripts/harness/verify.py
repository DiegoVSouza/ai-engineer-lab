#!/usr/bin/env python3
"""Roda `make verify` de um projeto e salva evidência. Ausência de comando = incomplete."""
import argparse, json, subprocess, pathlib, datetime, hashlib, os, sys
ap = argparse.ArgumentParser(); ap.add_argument("--project", required=True); ap.add_argument("--root", default=".")
a = ap.parse_args(); root = pathlib.Path(a.root).resolve(); proj = root / "projects" / a.project
ev = root / "artifacts" / "evidence" / a.project; ev.mkdir(parents=True, exist_ok=True)
ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
rec = {"project": a.project, "ts": ts, "command": f"make -C projects/{a.project} verify", "status": "incomplete"}
if (proj / "Makefile").exists():
    env = {**os.environ, "LLM_MODE": "fake"}
    r = subprocess.run(["make", "-C", str(proj), "verify"], capture_output=True, text=True, env=env)
    out = r.stdout + r.stderr
    (ev / f"verify-{ts}.log").write_text(out)
    rec.update(exit_code=r.returncode, status="pass" if r.returncode == 0 else "fail",
               sha256=hashlib.sha256(out.encode()).hexdigest(), log=f"verify-{ts}.log")
else:
    rec["reason"] = "Makefile ausente"
(ev / f"verify-{ts}.json").write_text(json.dumps(rec, indent=2))
print(json.dumps(rec, indent=2)); sys.exit(0 if rec["status"] == "pass" else 1)
