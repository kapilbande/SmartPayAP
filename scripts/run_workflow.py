# scripts/run_workflow.py
import os, sys, argparse
import pandas as pd
from src.data_loader import load_raw, build_invoice_level
from src.features import build_features
from src.agent_tools import MatcherTool, ExplainerTool

def run_workflow(invoice_id):
    invoices, po_grn, mismatches = load_raw()
    inv_agg = build_invoice_level(invoices)
    df, feature_cols = build_features(inv_agg, po_grn, mismatches)

    row = df[df["invoice_id"] == invoice_id]
    if row.empty:
        print(f"Invoice {invoice_id} not found.")
        return

    row = row.iloc[0:1]
    matcher = MatcherTool(feature_cols=feature_cols)
    model_out = matcher.predict(row)

    print("Model output:", model_out)
    pred = model_out["pred"]
    prob = model_out["prob"]

    auto_threshold = 0.9
    if pred == 1 or prob < auto_threshold:
        explainer = ExplainerTool()
        evidence = {
            "invoice_id": row["invoice_id"].values[0],
            "vendor_name": row["vendor_name"].values[0] if "vendor_name" in row else "Vendor",
            "invoice_total": float(row["invoice_total"].values[0]),
            "po_total": float(row["po_total"].values[0]),
            "amount_diff": float(row["amount_diff"].values[0]),
            "date_diff_days": int(row["date_diff_days"].values[0])
        }
        expl = explainer.run(evidence, model_out)
        print("\nExplanation:\n", expl["explanation"])
        print("Reasons:")
        for r in expl["reasons"]:
            print(" ", r)
        print("\nDraft Email:")
        print("Subject:", expl["email"]["subject"])
        print(expl["email"]["body"])
        print("\nAwaiting human approval... (simulated)")
    else:
        print("Auto-approved: match detected with high confidence.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--invoice_id", required=True)
    args = parser.parse_args()
    run_workflow(args.invoice_id)
