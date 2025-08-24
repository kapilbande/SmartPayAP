# tests/test_workflow.py
import os, sys
import pandas as pd

# make repo importable
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.data_loader import load_raw, build_invoice_level
from src.features import build_features
from src.agent_tools import MatcherTool, ExplainerTool
from scripts.run_workflow import run_workflow

def test_matcher_predict():
    """Test that the MatcherTool loads the model and makes a prediction."""
    invoices, po_grn, mismatches = load_raw()
    inv_agg = build_invoice_level(invoices)
    df, feature_cols = build_features(inv_agg, po_grn, mismatches)

    row = df.iloc[0:1]
    matcher = MatcherTool(feature_cols=feature_cols)
    out = matcher.predict(row)
    assert "pred" in out
    assert "prob" in out
    assert isinstance(out["pred"], int)

def test_explainer_output():
    """Test that the ExplainerTool generates explanation and email draft."""
    evidence = {
        "invoice_id": "INV_TEST",
        "vendor_name": "VendorX",
        "invoice_total": 1000,
        "po_total": 1100,
        "amount_diff": 100,
        "date_diff_days": 5
    }
    model_out = {"feature_values": {"amount_diff": 100, "date_diff_days": 5, "vendor_match": 0}}
    expl = ExplainerTool().run(evidence, model_out)
    assert "email" in expl
    assert "subject" in expl["email"]
    assert "body" in expl["email"]

def test_run_workflow_end_to_end():
    """Test that the workflow runs end-to-end without crashing for one invoice."""
    invoices, po_grn, mismatches = load_raw()
    if not mismatches.empty:
        invoice_id = mismatches["invoice_id"].iloc[0]
        run_workflow(invoice_id)  # should print workflow steps without error
