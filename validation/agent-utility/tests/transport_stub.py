"""TEST-ONLY fake model transport for adapter protocol tests. Never a model result.

Contract the adapter expects from any transport argv: reads the query file path,
prints the next canned reply to stdout, exits 0; nonzero exit when the canned reply
begins with __TRANSPORT_FAIL__. Logs one JSONL line per call to $AU_STUB_LOG.
"""
import json
import os
import sys

query_file = sys.argv[1]
replies_path = os.environ["AU_STUB_REPLIES"]
replies = json.loads(open(replies_path, encoding="utf-8").read())
# stateful: which reply index to serve next is tracked by a counter file beside replies
counter_path = replies_path + ".idx"
idx = int(open(counter_path).read()) if os.path.exists(counter_path) else 0
open(counter_path, "w").write(str(idx + 1))
reply = replies[min(idx, len(replies) - 1)]
with open(os.environ["AU_STUB_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps({"call": idx, "query_file": query_file}) + "\n")
if reply.startswith("__TRANSPORT_FAIL__"):
    sys.stderr.write(reply + "\n")
    sys.exit(1)
print(reply)
