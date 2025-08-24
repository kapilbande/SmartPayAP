# SmartPay AP – AI-Driven Invoice Matching

Production-ready blueprint for Accounts Payable automation: data ingestion, tabular ML, and GenAI agents with Responsible AI guardrails.

## Quick Start
```bash
# setup
pip install -r requirements.txt
# (optional dev tools)
pip install -r requirements-dev.txt

# run the workflow on one invoice id
python scripts/run_workflow.py --invoice_id INV0134 --csv data/invoices.csv

# run tests
python -m pytest -v
```

## Project Structure
```text
data/                 # sample or synthetic inputs
docs/                 # design notes and compliance docs
models/               # trained model artifacts (e.g., models/matcher.pkl)
scripts/              # runnable scripts for demo / E2E flow
src/                  # library code (tools, model serving, agents)
tests/                # unit tests
```

## Guardrails (Agent Tool Misuse) ✅
We enforce **two guardrails** to keep tools safe and predictable:

1. **Input Validation (MatcherTool)** – blocks model runs on unsafe inputs.  
   - Verifies required fields: `invoice_id, invoice_total, po_total, amount_diff, date_diff_days`  
   - Ensures no nulls in model features: `amount_diff, amount_ratio, date_diff_days, vendor_match, item_count`  
   - Bounds checks: `|amount_ratio| ≤ 1e3`, `|amount_diff| ≤ 1e9`, `|date_diff_days| ≤ 3650`

2. **Output Safety (ExplainerTool)** – prevents unsafe email drafts.  
   - Forbids terms: `bank account`, `payment instruction`, `password`, `otp`  
   - Redacts emails, phone numbers, IBAN-like strings  
   - Truncates body > 2,000 chars

👉 Details in **[docs/Guardrails.md](docs/Guardrails.md)**. Run `python -m pytest tests/test_guardrails.py -v` to verify.

## Multi-Cloud & GDPR
- Deploy on **Azure AKS** and **AWS EKS** behind API Gateway with AuthN/Z.  
- **Common MLOps** layer (MLflow, CI/CD, monitoring) shared across clouds.  
- **GDPR/CCPA** alignment: data residency, PII redaction, audit trail.

## Notes
- The dataset is synthetic for POC. Extend features and evaluation as needed.
- If you reuse open-source code, cite the repo and license in `docs/`.
```
