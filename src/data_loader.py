import os, pandas as pd
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
def load_raw():
    invoices = pd.read_csv(os.path.join(DATA_DIR, "invoices.csv"))
    po_grn = pd.read_csv(os.path.join(DATA_DIR, "po_grn.csv"))
    mismatches = pd.read_csv(os.path.join(DATA_DIR, "labelled_mismatches.csv"))
    return invoices, po_grn, mismatches
def build_invoice_level(invoices: pd.DataFrame) -> pd.DataFrame:
    return invoices.groupby(
        ["invoice_id","invoice_date","vendor_id","vendor_name","currency"], as_index=False
    ).agg(invoice_total=("line_total","sum"), item_count=("line_item_number","nunique"))
