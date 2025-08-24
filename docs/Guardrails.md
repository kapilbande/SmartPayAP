# Guardrails for Agent Tool Misuse

We implemented two guardrails in `src/agent_tools.py` and updated orchestration to **fail closed**.

## 1) Input Validation — MatcherTool
- Required columns: `invoice_id, invoice_total, po_total, amount_diff, date_diff_days`
- Model features must be non-null: `amount_diff, amount_ratio, date_diff_days, vendor_match, item_count`
- Defensive bounds:
  - `|amount_ratio| ≤ 1e3`
  - `|amount_diff| ≤ 1e9`
  - `|date_diff_days| ≤ 3650`

**Outcome:** Raises `ValueError` before any model call on unsafe rows.

## 2) Output Safety — ExplainerTool
- Forbidden terms: `bank account`, `payment instruction`, `password`, `otp` (configurable)
- Redaction: e-mails → `[REDACTED_EMAIL]`, phone numbers → `[REDACTED_PHONE]`, IBAN-like → `[REDACTED_IBAN]`
- Output length bounded to 2,000 chars

**Outcome:** Raises `ValueError` on unsafe generations; otherwise returns a redacted, bounded draft.

## Orchestration
`scripts/run_workflow.py` wraps tool calls with `try/except` and returns:
- `{"status": "blocked", "reason": "<guardrail message>"}` when a guardrail fires
- `{"status": "ok", "result": {...}}` on success

## Verify
```bash
python -m pytest tests/test_guardrails.py -v
```
