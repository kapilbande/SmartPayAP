import os, sys, joblib
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.data_loader import load_raw, build_invoice_level
from src.features import build_features
from sklearn.metrics import classification_report, confusion_matrix
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "matcher.pkl")
def main():
    invoices, po_grn, mismatches = load_raw()
    inv_agg = build_invoice_level(invoices)
    df, feature_cols = build_features(inv_agg, po_grn, mismatches)
    model = joblib.load(MODEL_PATH)
    y_pred = model.predict(df[feature_cols])
    print("Evaluation Report (Full Set):\n", classification_report(df["label"], y_pred, digits=4))
    print("Confusion Matrix:\n", confusion_matrix(df["label"], y_pred))
if __name__ == "__main__":
    main()
