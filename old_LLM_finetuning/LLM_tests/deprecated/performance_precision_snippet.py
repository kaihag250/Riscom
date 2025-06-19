import pandas as pd
import re

# === Step 1: Save ground truth from your original DataFrame ===
df[["input", "output"]].to_csv("ground_truth.csv", index=False)

# === Step 2: Use model to predict outputs ===
pred_outputs = []
from tqdm import tqdm  # Optional: progress bar
for text in tqdm(df["input"], desc="Generating predictions"):
    input_ids = tokenizer(text, return_tensors="pt", truncation=True).input_ids.to(model.device)
    output_ids = model.generate(input_ids, max_length=512)
    decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    pred_outputs.append(decoded)

# Save predictions
pred_df = pd.DataFrame({
    "input": df["input"],
    "output": pred_outputs
})
pred_df.to_csv("model_outputs.csv", index=False)
print("✅ Saved ground_truth.csv and model_outputs.csv")

# === Step 3: Evaluate predictions field-by-field ===

# Load both files
ground_truth = pd.read_csv("ground_truth.csv")
predictions = pd.read_csv("model_outputs.csv")
merged = pd.merge(ground_truth, predictions, on="input", suffixes=("_true", "_pred"))

def parse_output(text):
    result = {}
    for line in str(text).strip().split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            result[key.strip()] = value.strip()
    return result

def normalize_value(val):
    val = val.lower().strip()
    if val in ["null", "n/a", "none", ""]:
        return "null"
    val = val.replace(",", "")
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

field_stats = {}
results = []

for _, row in merged.iterrows():
    true_dict = parse_output(row["output_true"])
    pred_dict = parse_output(row["output_pred"])
    row_result = {"input": row["input"]}

    for field in true_dict:
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

# Show sample and summary
results_df = pd.DataFrame(results)
print("\n=== Sample Comparison ===")
print(results_df.head(3).to_string())

print("\n=== Field-wise Accuracy ===")
for field, stats in field_stats.items():
    acc = 100 * stats["correct"] / stats["total"]
    print(f"{field:50s} → {acc:.1f}% ({stats['correct']}/{stats['total']})")