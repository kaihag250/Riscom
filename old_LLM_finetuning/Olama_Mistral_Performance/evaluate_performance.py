import pandas as pd
import re

# === Load CSVs ===
ground_truth = pd.read_csv("ground_truth.csv")
predictions = pd.read_csv("model_outputs.csv")
merged = pd.merge(ground_truth, predictions, on="input", suffixes=("_true", "_pred"))

def parse_output(text):
    """Parses plain 'Field: value' output into a dictionary."""
    result = {}
    for line in str(text).strip().split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            result[key.strip().lower()] = value.strip()
    return result

def normalize_value(val):
    """Normalizes values for fair comparison."""
    val = str(val).strip().lower()
    val = val.replace(",", "").replace("approximately", "").replace("per ", "")
    
    if val in ["null", "n/a", "none", ""]:
        return "null"

    # Handle values like '3 in 1,000 or 0.003'
    if " or " in val:
        val = val.split(" or ")[0].strip()

    # Extract numeric values
    match = re.match(r"([0-9.]+)\s*(million|thousand)?", val)
    if match:
        num, unit = match.groups()
        num = float(num)
        if unit == "million":
            num *= 1_000_000
        elif unit == "thousand":
            num *= 1_000
        return str(int(num)) if num.is_integer() else str(num)

    return val

# === Compare field by field ===
field_stats = {}
results = []

for _, row in merged.iterrows():
    true_dict = parse_output(row["output_true"])
    pred_dict = parse_output(row["output_pred"])
    row_result = {"input": row["input"]}

    all_fields = set(true_dict) | set(pred_dict)
    for field in all_fields:
        pred_val = normalize_value(pred_dict.get(field, "null"))
        true_val = normalize_value(true_dict.get(field, "null"))
        correct = (pred_val == true_val)
        row_result[field] = "✅" if correct else f"❌ (pred: {pred_val})"
        
        if field not in field_stats:
            field_stats[field] = {"correct": 0, "total": 0}
        field_stats[field]["total"] += 1
        if correct:
            field_stats[field]["correct"] += 1

    results.append(row_result)

# === Output results ===
results_df = pd.DataFrame(results)

print("\n=== Sample Comparison ===")
print(results_df.head(3).to_string())

print("\n=== Field-wise Accuracy ===")
for field, stats in field_stats.items():
    acc = 100 * stats["correct"] / stats["total"]
    print(f"{field:50s} → {acc:.1f}% ({stats['correct']}/{stats['total']})")
