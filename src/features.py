import pandas as pd
def _to_dt(s):
    return pd.to_datetime(s, errors="coerce", dayfirst=True)
def build_features(inv_agg: pd.DataFrame, po_grn: pd.DataFrame, mismatches: pd.DataFrame):
    df = mismatches.merge(inv_agg, on="invoice_id", how="left")
    df = df.merge(po_grn, on="po_number", how="left", suffixes=("_inv","_po"))
    df["amount_diff"]  = (df["invoice_total"] - df["po_total"]).abs()
    df["amount_ratio"] = df["invoice_total"] / (df["po_total"].abs() + 1e-5)
    df["invoice_date"] = _to_dt(df["invoice_date"]); df["po_date"] = _to_dt(df["po_date"])
    df["date_diff_days"] = (df["invoice_date"] - df["po_date"]).dt.days
    df["vendor_match"] = 0
    if "vendor_id" in df.columns and "vendor_id_po" in df.columns:
        df["vendor_match"] = (df["vendor_id"] == df["vendor_id_po"]).astype(int)
    df["currency_match"] = 1
    if "currency" in df.columns and "currency_po" in df.columns:
        df["currency_match"] = (df["currency"] == df["currency_po"]).astype(int)
    df["label"] = (df["difference"].fillna(0) != 0).astype(int)
    df["item_count"] = df.get("item_count", 1)
    df = df.dropna(subset=["invoice_total","po_total","invoice_date","po_date"])
    feature_cols = ["amount_diff","amount_ratio","date_diff_days","vendor_match","currency_match","item_count"]
    return df, feature_cols
