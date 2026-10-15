# AU-v1 trusted adapter — real Hermes CLI transport

`hermes_cli_jsonl_adapter.py` is the trusted JSONL broker adapter for the frozen
AU-v1 protocol: it spawns the authorized Hermes CLI per model decision and gives the
tested model zero tools — corpus content reaches it only as broker `read_result`
text relayed through the adapter's stdout/stdin protocol. See
`adapter-feasibility-results.json` for verified evidence and the exact cohort command.

## How it works

- One fresh `hermes chat --query-file <transcript> --oneshot -Q --format stream-json
  --provider <P> -m <model> -t bot_room --safe-mode --run-budget <s> --source tool`
  process per model decision (`bot_room` is a registered toolset that resolves to
  **zero** tool schemas; verified against the shipped runtime — see feasibility
  record). `--safe-mode` ignores user config/rules/memory/skills/plugins/MCP.
- The model's visible context is exactly: the frozen start JSON (scenario, prompt,
  settings, inventory, read contract) + the adapter's one-line protocol instruction +
  its own prior replies + broker read excerpts. Each stateless call re-sends the full
  transcript, so every scenario is a fresh conversation with no resume path.
- stdout is exclusively canonical JSONL: `ready` (with `fresh_context`,
  `broker_only`, `settings_sha256`, `identity`, and an honest
  `settings_enforcement` attestation) → `read_file` requests → `final`. All logging
  goes to stderr (harness-discarded). Oversize chunks and exhausted remaining budgets
  are steered locally before the broker's fail-closed branch; finals over
  `max_final_chars`/`max_message_bytes` abort nonzero rather than truncate.
- Integrity guards: transport-reported model ≠ pinned model → abort (catches silent
  provider fallback); `--model` conflicting with a start-pinned model → abort before
  any attestation; transport failure twice → abort. No simulated responses exist in
  this codebase.
- Credentials: the adapter never reads, prints or forwards secret material. It names
  the operator's own Hermes home (`--hermes-home`, passed to the child as
  `HERMES_HOME`) so the authorized CLI uses its existing credential store; the child
  environment is otherwise minimal.

## Tests

`../tests/test_adapter_protocol.py` (13 tests) drives the adapter against a scripted
fake transport and in-memory broker; `../tests/transport_stub.py` is test-only. The
harness strips `AU_ADAPTER_TRANSPORT_CMD`, so operator-launched cohort runs always
take the real transport path. Protocol fixture replies are never model results.

## Probe

`transport_probe.py` runs one NON-BENCHMARK end-to-end check (synthetic mini-corpus,
fictional task) and writes a JSON evidence file. Never place its output in a cohort
results directory and never score it.

## Limitation (attested per run)

`temperature=0`, `seed=1729`, `max_output_tokens=4500` are frozen in settings and
hashed, but the Hermes CLI exposes no sampling/seed/output-cap flags and
`request_overrides` would require config changes this cohort forbids. The adapter
therefore attests model pinning and budget/wall enforcement precisely, and these three
as "frozen-declared, provider-default-on-wire". Hard wire enforcement requires an
external OS-sandboxed raw-API adapter (instructions in the feasibility record); do
not claim otherwise.
