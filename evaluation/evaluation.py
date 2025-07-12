import os
import pandas as pd
import re
from sklearn.metrics import classification_report

#this script is designed to evaluate the fine-tuned LLM in the context of the risk communication assistant team project
#the ground_truth.csv the code refers to is manually labelled data and the text data should be 
# carefully chosen, differing in quality and type of risk communication in order to get a representative evaluation


#the evaluation_log.csv created is for manual checking

#the text_field_review.csv is for manually comparing the test fields
#no automatic evaluation has been implemented here for text fields


# automatic path to folder of this python script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PREDICTION_FILE = os.path.join(SCRIPT_DIR, "model_output.csv")
GROUND_TRUTH_FILE = os.path.join(SCRIPT_DIR, "ground_truth.csv")

#list to have a log of the evaluation  
log_entries = []


#Column configuration: our model extracts three different types of data from text, classification, numeric values and text
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
    "source_base", "source_new"
]

# Parsing-functions: to only keep the necessary text and filter from the LLM-Output and the ground-truth
def parse_output_model(text):
    """Parser for Modell-Predictions with ### Output:"""
    result = {}
    if pd.isna(text):
        return result
    match = re.search(r"### Output:\s*(.+)", text, re.DOTALL)
    if not match:
        return result
    output_block = match.group(1).strip()
    for line in output_block.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            result[key.strip()] = val.strip()
    return result

def parse_output_groundtruth(text):
    """Parser for Ground Truth without ### Output:"""
    result = {}
    if pd.isna(text):
        return result
    for line in text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            result[key.strip()] = val.strip()
    return result

def clean_number(value):
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

# Read data and check
if not os.path.exists(PREDICTION_FILE):
    print(f"❌ Prediction file not found: {PREDICTION_FILE}")
    exit(1)
if not os.path.exists(GROUND_TRUTH_FILE):
    print(f"❌ Ground truth file not found: {GROUND_TRUTH_FILE}")
    exit(1)

pred_raw = pd.read_csv(PREDICTION_FILE)
ground_truth = pd.read_csv(GROUND_TRUTH_FILE)

# parse output columns
parsed_pred = pred_raw["Output"].apply(parse_output_model)
parsed_gt = ground_truth["output"].apply(parse_output_groundtruth)
pred_df = pd.json_normalize(parsed_pred)
gt_df = pd.json_normalize(parsed_gt)

# Find common extraction categories
common_columns = sorted(set(pred_df.columns) & set(gt_df.columns))
print(f"\n {len(common_columns)} extraction categories are being compared for the whole dataset\n")


##now the real evalutation starts for each of the three different categories:

# 1. Classifications: F1, Precision, Recall

#precision: is the percentage of predicted positives that were actually correct
# recall: is the percentage of actual positives that were successfully predicted
#f1-score:  is the harmonic mean of precision and recall, balancing both
#support:  is the number of true examples for each class in the dataset


print("Classifikation:")
for col in classification_columns:
    if col in common_columns:
        # common format string, trimm, lowercase
        gt_raw = gt_df[col].astype(str).str.strip().str.lower()
        pred_raw = pred_df[col].astype(str).str.strip().str.lower()

        print(f"\n--- {col} ---")
        if len(gt_raw) == 0:
            print("no comparison data found")
        else:
            print("→ classification (incl. null):")
            report = classification_report(gt_raw, pred_raw, zero_division=0, output_dict=True)
            print(classification_report(gt_raw, pred_raw, zero_division=0))

            # insert results in the log list created in the beginning
            for i, (gt_val, pred_val) in enumerate(zip(gt_raw, pred_raw)):
                log_entries.append({
                    "index": i,
                    "category": col,
                    "type": "classification",
                    "ground_truth": gt_val,
                    "prediction": pred_val,
                    "correct": str(gt_val) == str(pred_val)
                })
    else:
        print(f" Column {col} not found in both")


# 2. Numeric categories: Accuracy
print("\nNumeric categories (Accuracy):")
for col in numeric_columns:
    if col in common_columns:
        correct = 0
        total = 0
        for i, (gt_val, pred_val) in enumerate(zip(gt_df[col], pred_df[col])):
            gt_clean = clean_number(gt_val)
            pred_clean = clean_number(pred_val)

            is_correct = (
                (gt_clean is None and pred_clean is None) or
                (gt_clean is not None and pred_clean is not None and abs(gt_clean - pred_clean) < 1e-6)
            )

            # Logging:
            log_entries.append({
                "index": i,
                "category": col,
                "type": "numeric",
                "ground_truth": gt_val,
                "prediction": pred_val,
                "correct": is_correct
            })

            if is_correct:
                correct += 1
            total += 1

        acc = correct / total if total > 0 else 0
        print(f"{col}: Accuracy = {acc:.2%} ({correct}/{total})")
    else:
        print(f"  Column {col} Not found in both files.")


# 3. Textfields for manual checking
print("\nTextfields: Comparison-table created")
text_review = pd.DataFrame()
text_review["input"] = ground_truth.get("input", [""] * len(ground_truth))
for col in text_columns:
    if col in common_columns:
        text_review[f"{col}_ground_truth"] = gt_df[col]
        text_review[f"{col}_prediction"] = pred_df[col]

text_review.to_csv("text_field_review.csv", index=False)
print("→ File saved: text_field_review.csv")
log_df = pd.DataFrame(log_entries)
log_df.to_csv("evaluation_log.csv", index=False)
print("→ Evaluation Log saved as: evaluation_log.csv")