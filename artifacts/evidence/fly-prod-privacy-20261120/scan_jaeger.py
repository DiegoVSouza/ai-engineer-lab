"""Read Jaeger over the fly proxy and report keys and any probe content found in span tags or log fields. Values are never printed, only counts and key names."""
import json, re, urllib.request, collections, sys
needles = ["Please review my invoice", "DROP TABLE", "probe ", "customer-a", "agent-a", "agent-b", "approver-a", "Bearer ", "eyJ", "password", "client_secret", "@"]
out = {"services": {}, "hits": [], "keys": collections.Counter(), "log_keys": collections.Counter(), "exception_message_values": 0}
for svc in ("p05-runtime", "p05-mcp"):
    d = json.load(urllib.request.urlopen(f"http://localhost:16686/api/traces?service={svc}&limit=1500&lookback=2h", timeout=60))["data"]
    spans = 0; names = collections.Counter()
    for t in d:
        for s in t["spans"]:
            spans += 1; names[s["operationName"]] += 1
            for tag in s.get("tags", []):
                out["keys"][tag["key"]] += 1
                v = str(tag["value"])
                if tag["key"] == "exception.message" and v: out["exception_message_values"] += 1
                for n in needles:
                    if n in v: out["hits"].append((svc, s["operationName"], "tag", tag["key"], n))
            for lg in s.get("logs", []):
                for f in lg.get("fields", []):
                    out["log_keys"][f["key"]] += 1
                    v = str(f["value"])
                    for n in needles:
                        if n in v: out["hits"].append((svc, s["operationName"], "log", f["key"], n))
    out["services"][svc] = {"traces": len(d), "spans": spans, "top_operations": names.most_common(8)}
out["keys"] = dict(out["keys"]); out["log_keys"] = dict(out["log_keys"])
print(json.dumps(out, indent=1))
