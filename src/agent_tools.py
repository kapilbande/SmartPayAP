# src/agent_tools.py
import joblib

class MatcherTool:
    def __init__(self, model_path="models/matcher.pkl", feature_cols=None):
        import joblib
        self.model = joblib.load(model_path)
        self.feature_cols = feature_cols

    def predict(self, row):
        # Ensure correct shape: DataFrame with one row
        X = row[self.feature_cols].astype("float32")
        
        # no need to wrap in []
        pred = int(self.model.predict(X)[0])
        prob = float(self.model.predict_proba(X)[0][pred])
        return {"pred": pred, "prob": prob}


class ExplainerTool:
    def __init__(self, llm_client=None):
        self.llm = llm_client

    def run(self, evidence: dict, model_output: dict):
        # Template-based explanation
        reasons = []
        fv = model_output.get("feature_values", {})
        if fv.get("amount_diff", 0) > 1e-2:
            reasons.append(f"- Amount differs by {fv['amount_diff']:.2f}.")
        if abs(fv.get("date_diff_days", 0)) > 3:
            reasons.append(f"- Date difference is {fv['date_diff_days']} days.")
        if fv.get("vendor_match", 1) == 0:
            reasons.append(f"- Vendor mismatch.")
        if not reasons:
            reasons.append("- Flagged by combined heuristics.")

        email_subject = f"Clarification required – Invoice {evidence.get('invoice_id')}"
        email_body = f"Dear {evidence.get('vendor_name', 'Vendor')},\n\nWe noted a mismatch for Invoice {evidence.get('invoice_id')}:\n" + "\n".join(reasons) + "\n\nPlease advise.\n\nBest,\nAP Team"
        return {"explanation": "Invoice flagged as mismatch.", "reasons": reasons, "email": {"subject": email_subject, "body": email_body}}
