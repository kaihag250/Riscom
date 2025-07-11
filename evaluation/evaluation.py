import pandas as pd
import re
from sklearn.metrics import classification_report

#import data as csv -> hand labelled ground truth and model output for comparison
PREDICTION_FILE = "model_output.csv"
GROUND_TRUTH_FILE = "ground_truth.csv"

#categorize extraction: classification for classification metrics, numeric for accuracy and text for manual comparison
classification_columns = ["risk_communication", "unrelated_risks"]
numeric_columns = [
    "absolute_risk_base", "absolute_risk_new",
    "absolute_number_base", "absolute_number_new",
    "absolute_risk_difference", "relative_risk",
    "absolute_number_difference",
    "reference_class_size_base", "reference_class_size_new"
]
text_columns = [
    "verbal_descriptor_base", "verbal_descriptor_new", "verbal_descriptor_change",
    "reference_class_description_base", "reference_class_description_new",
    "source_base", "source_new", "topic_and_unit"
]

# deal with structure of outputs
pred_raw = pd.read_csv(PREDICTION_FILE)

def parse_output(text):
    result = {}
    if pd.isna(text):
        return result
    for line in text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            result[key.strip()] = val.strip()
    return result

parsed_outputs = pred_raw["output"].apply(parse_output)
pred_parsed = pd.json_normalize(parsed_outputs)

ground_truth = pd.read_csv(GROUND_TRUTH_FILE)

# 1: for classification category calculate F1, Precision, Recall
print("\n=== Klassifikation (F1, Precision, Recall) ===")
for col in classification_columns:
    try:
        gt = ground_truth[col].astype(str).str.strip().str.lower()
        pred = pred_parsed[col].astype(str).str.strip().str.lower()
        report = classification_report(gt, pred, zero_division=0)
        print(f"\n--- {col} ---")
        print(report)
    except Exception as e:
        print(f"Fehler bei {col}: {e}")

# 2. for numeric value calculate accuracy with robust format dealing
def clean_number(value):
    """
    normalize numeric values:
    - Accepts %, , or .
    - excludes white spaces 
    - Wandelt 'null', 'nan', '' in None um
    """
    if pd.isna(value):
        return None
    value = str(value).strip().lower()
    if value in ["", "null", "nan", "none"]:
        return None
    value = value.replace(",", ".")
    value = re.sub(r"[^0-9\.]", "", value)
    try:
        return float(value)
    except ValueError:
        return None

print("\nNumeric Values (Accuracy of Extraktion)")
for col in numeric_columns:
    correct = 0
    total = 0
    for gt_val, pred_val in zip(ground_truth[col], pred_parsed[col]):
        gt_clean = clean_number(gt_val)
        pred_clean = clean_number(pred_val)
        if gt_clean is None and pred_clean is None:
            correct += 1
        elif gt_clean is not None and pred_clean is not None and abs(gt_clean - pred_clean) < 1e-6:
            correct += 1
        total += 1
    acc = correct / total if total > 0 else 0
    print(f"{col}: Accuracy = {acc:.2%} ({correct}/{total})")

# === 3. Textfelder: Ausgabe zur manuellen Prüfung ===
print("\nTextfields for manual checking")
text_comparison = pd.DataFrame()
text_comparison["input"] = ground_truth.get("input", [""] * len(ground_truth))
for col in text_columns:
    text_comparison[f"{col}_ground_truth"] = ground_truth.get(col, "")
    text_comparison[f"{col}_prediction"] = pred_parsed.get(col, "")

text_comparison.to_csv("text_field_review.csv", index=False)
print("→ stored as: text_field_review.csv")
