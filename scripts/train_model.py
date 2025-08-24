import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.data_loader import load_raw, build_invoice_level
from src.features import build_features
from src.model import train_model
def main():
    invoices, po_grn, mismatches = load_raw()
    inv_agg = build_invoice_level(invoices)
    df, feature_cols = build_features(inv_agg, po_grn, mismatches)
    train_model(df, feature_cols)
if __name__ == "__main__":
    main()
