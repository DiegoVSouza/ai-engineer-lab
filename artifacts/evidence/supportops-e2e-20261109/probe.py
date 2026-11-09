"""Failure-mode probe for the SupportOps API through the console proxy. Usage: probe.py local|fly
Secrets stay in memory; output has statuses only."""
import json, subprocess, sys, time, base64, uuid
from pathlib import Path
import httpx

LAB = Path(__file__).resolve().parents[3]
target = sys.argv[1]
if target == "fly":
    sec = json.loads((LAB/"artifacts/checkpoints/pre-fly-final-20261023/fly-secrets.json").read_text(encoding="utf-8-sig"))
    pw = {"agent-a": sec["AGENT_A_PASSWORD"], "agent-b": sec["AGENT_B_PASSWORD"], "approver-a": sec["APPROVER_PASSWORD"]}
    API, TOKEN = "https://supportops-lab-web.fly.dev/api", "https://supportops-lab-idp.fly.dev/realms/supportops/protocol/openid-connect/token"
    CS = sec["SUPPORTOPS_CLIENT_SECRET"]
else:
    pw = {}
    API, TOKEN = "http://localhost:48080/api", None

c = httpx.Client(verify=False, timeout=60)
results = []

def rec(name, got, want):
    ok = got in want if isinstance(want, (set, tuple, list)) else got == want
    results.append((name, got, want, ok))
    print(("ok   " if ok else "FAIL ") + f"{name}: got {got} want {want}")

def tok(user):
    if target != "fly":
        o = subprocess.run([sys.executable, "scripts/stack.py", "token", user], cwd=LAB, capture_output=True, text=True).stdout.strip().splitlines()
        t = o[-1] if o else ""
        rec(f"token {user}", t.count(".") == 2, True)
        return t
    scope = "ticket:read task:read approval:decide" if user == "approver-a" else "ticket:read ticket:write task:read task:write triage:run billing:read crm:read refund:request feedback:write"
    r = c.post(TOKEN, data={"grant_type": "password", "client_id": "supportops-api", "client_secret": CS, "username": user, "password": pw[user], "scope": scope})
    rec(f"token {user}", r.status_code, 200)
    return r.json().get("access_token", "")

def H(t): return {"Authorization": f"Bearer {t}"}

t0 = time.time()
rec("healthz", c.get(API + "/healthz").status_code, 200)
rec("no token list", c.get(API + "/v1/tickets").status_code, 401)
rec("garbage token", c.get(API + "/v1/tickets", headers=H("garbage")).status_code, 401)
a, b, ap = tok("agent-a"), tok("agent-b"), tok("approver-a")
tam = a.split("."); p = json.loads(base64.urlsafe_b64decode(tam[1] + "=="))
p["preferred_username"] = "approver-a"; tam[1] = base64.urlsafe_b64encode(json.dumps(p).encode()).decode().rstrip("=")
rec("tampered payload", c.get(API + "/v1/tickets", headers=H(".".join(tam))).status_code, 401)
rec("alg none", c.get(API + "/v1/tickets", headers=H(base64.urlsafe_b64encode(b'{"alg":"none"}').decode().rstrip("=") + "." + tam[1] + ".")).status_code, 401)
rec("list as agent", c.get(API + "/v1/tickets", headers=H(a)).status_code, 200)

good = {"customer_id": "customer-a", "subject": f"probe {uuid.uuid4().hex[:8]}", "body": "Please review my invoice refund."}
r = c.post(API + "/v1/tickets", headers=H(a), json=good); rec("create ticket", r.status_code, 201)
tid = r.json().get("id", "")
for name, body, want in [("missing field", {"customer_id": "x"}, 422), ("empty subject", {**good, "subject": ""}, 422),
                         ("subject 201 chars", {**good, "subject": "s" * 201}, 422), ("body 10001 chars", {**good, "body": "b" * 10001}, 422),
                         ("wrong type", {**good, "subject": 5}, 422), ("extra field", {**good, "tenant_id": "other"}, {201, 422})]:
    rec(name, c.post(API + "/v1/tickets", headers=H(a), json=body).status_code, want)
rec("not json", c.post(API + "/v1/tickets", headers={**H(a), "content-type": "application/json"}, content=b"{nope").status_code, 422)
rec("no body", c.post(API + "/v1/tickets", headers=H(a)).status_code, 422)
rec("huge body 2MB", c.post(API + "/v1/tickets", headers=H(a), json={**good, "body": "x" * 2_000_000}).status_code, {413, 422})
rec("injection in subject", c.post(API + "/v1/tickets", headers=H(a), json={**good, "subject": "'; DROP TABLE tickets;--"}).status_code, 201)
rec("unicode body", c.post(API + "/v1/tickets", headers=H(a), json={**good, "body": "olá ✓ 你好 \u0000"}).status_code, {201, 422})

rec("get own ticket", c.get(API + f"/v1/tickets/{tid}", headers=H(a)).status_code, 200)
rec("other tenant get", c.get(API + f"/v1/tickets/{tid}", headers=H(b)).status_code, {403, 404})
rec("missing ticket", c.get(API + f"/v1/tickets/{uuid.uuid4()}", headers=H(a)).status_code, 404)
rec("non-uuid id", c.get(API + "/v1/tickets/not-a-uuid", headers=H(a)).status_code, {404, 422})
rec("path traversal id", c.get(API + "/v1/tickets/..%2f..%2fetc%2fpasswd", headers=H(a)).status_code, {400, 404, 422})
rec("other tenant listing excludes", tid not in [t["id"] for t in c.get(API + "/v1/tickets", headers=H(b)).json()], True)

rec("agent lists approvals", c.get(API + "/v1/approvals", headers=H(a)).status_code, 403)
rec("approver lists approvals", c.get(API + "/v1/approvals", headers=H(ap)).status_code, 200)
IK = uuid.uuid4().hex
rf = lambda amt, who=a, t=None, k=None: c.post(API + f"/v1/tickets/{t or tid}/refund-approvals", headers={**H(who), "Idempotency-Key": k or uuid.uuid4().hex}, json={"amount_cents": amt})
rec("refund without idempotency key", c.post(API + f"/v1/tickets/{tid}/refund-approvals", headers=H(a), json={"amount_cents": 100}).status_code, {400, 422})
rec("refund key 129 chars", rf(100, k="k"*129).status_code, {400, 422})
for name, amt, want in [("refund zero", 0, 422), ("refund negative", -5, 422), ("refund over cap", 5001, 422), ("refund float", 12.5, 422),
                        ("refund string", "12", {202, 422}), ("refund null", None, 422)]:
    rec(name, rf(amt).status_code, want)
rec("refund other tenant", rf(100, b).status_code, {403, 404})
rec("refund missing ticket", rf(100, a, str(uuid.uuid4()), uuid.uuid4().hex).status_code, {403, 404})
r1 = rf(1500, k=IK); rec("refund ok", r1.status_code, 202)
r2 = rf(1500, k=IK); rec("refund duplicate same key", r2.status_code, {202, 409})
r3 = rf(2500, k=uuid.uuid4().hex); rec("refund second key", r3.status_code, {202, 409})
print("   duplicate returns same id:", r1.json().get("id") == r2.json().get("id"))
aps = [x for x in c.get(API + "/v1/approvals", headers=H(ap)).json() if x["ticket_id"] == tid]
print("   approvals for ticket:", len(aps), [x["state"] for x in aps])
if aps:
    aid = aps[0]["id"]
    rec("agent decides own approval", c.post(API + f"/v1/approvals/{aid}/decision", headers=H(a), json={"decision": "approved"}).status_code, 403)
    rec("bad decision value", c.post(API + f"/v1/approvals/{aid}/decision", headers=H(ap), json={"decision": "maybe"}).status_code, {400, 409, 422})
    rec("decision missing approval", c.post(API + f"/v1/approvals/{uuid.uuid4()}/decision", headers=H(ap), json={"decision": "approved"}).status_code, {403, 404})
    d1 = c.post(API + f"/v1/approvals/{aid}/decision", headers=H(ap), json={"decision": "approved"}); rec("approve", d1.status_code, 200)
    d2 = c.post(API + f"/v1/approvals/{aid}/decision", headers=H(ap), json={"decision": "approved"}); rec("approve twice", d2.status_code, {200, 409})
    d3 = c.post(API + f"/v1/approvals/{aid}/decision", headers=H(ap), json={"decision": "rejected"}); rec("flip decision after approve", d3.status_code, {409, 422, 400})
    time.sleep(8)
    print("   final approval states:", [(x["state"]) for x in c.get(API + "/v1/approvals", headers=H(ap)).json() if x["ticket_id"] == tid])

rec("task missing ticket", c.post(API + "/v1/tasks", headers={**H(a), "Idempotency-Key": uuid.uuid4().hex}, json={"ticket_id": str(uuid.uuid4())}).status_code, {202, 404, 422})
rt = c.post(API + "/v1/tasks", headers={**H(a), "Idempotency-Key": uuid.uuid4().hex}, json={"ticket_id": tid}); rec("task create", rt.status_code, 202)
if rt.status_code == 202:
    task = rt.json()["id"]
    for _ in range(30):
        v = c.get(API + f"/v1/tasks/{task}", headers=H(a)).json()
        if v["status"] not in ("queued", "running", "pending"): break
        time.sleep(2)
    print("   task final:", v["status"], "attempts", v["attempts"], "error", v.get("error"))
    rec("task terminal", v["status"] in ("succeeded", "completed", "done", "failed", "needs_approval"), True)
    rec("task other tenant", c.get(API + f"/v1/tasks/{task}", headers=H(b)).status_code, {403, 404})
rec("demo runs public", c.get(API + "/v1/demo/runs").status_code, {200, 401, 404})
rec("method not allowed", c.delete(API + "/v1/tickets", headers=H(a)).status_code, {405, 404})
rec("unknown route", c.get(API + "/v1/nope", headers=H(a)).status_code, 404)
opt = c.options(API + "/v1/tickets", headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "GET"})
print("   CORS evil origin allow:", opt.headers.get("access-control-allow-origin"))
hd = c.get(API + "/").headers
print("   headers:", {k: (v[:60]) for k, v in hd.items() if k.lower() in ("content-security-policy", "x-content-type-options", "strict-transport-security", "x-frame-options", "referrer-policy")})
print(f"\n{sum(1 for r in results if r[3])}/{len(results)} expectations met in {time.time()-t0:.0f}s")
sys.exit(0 if all(r[3] for r in results) else 1)
