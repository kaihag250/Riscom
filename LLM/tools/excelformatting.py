import pandas as pd

# Load Excel file
df = pd.read_excel("testing_groundtruth.xlsx")

# Define text and output fields
text_col = "Unnamed: 0"

output_fields = [
    'risk_communication',
    'unrelated_risks',
    'absolute_risk_base',
    'absolute_risk_new',
    'absolute_number_base',
    'absolute_number_new',
    'absolute_risk_difference',
    'relative_risk',
    'absolute_number_difference',
    'verbal_descriptor_base',
    'verbal_descriptor_new',
    'verbal_descriptor_change',
    'reference_class_size_base',
    'reference_class_size_new',
    'reference_class_description_base',
    'reference_class_description_new',
    'source_base',
    'source_new'
]
# format output string
def format_output(row):
    lines = []
    for col in output_fields:
        val = row.get(col)
        if pd.isna(val):
            lines.append(f"{col}: null")
        else:
            lines.append(f"{col}: {val}")
    return "\n".join(lines)

# Build training DataFrame
formatted_df = pd.DataFrame()
formatted_df["input"] = df[text_col]
formatted_df["output"] = df.apply(format_output, axis=1)

# Drop rows with missing input text
formatted_df = formatted_df.dropna(subset=["input"])

# === 5. Save to CSV ===
output_path = "ground_truth.csv"
formatted_df.to_csv(output_path, index=False)
print(f"Saved: {output_path} with 'input' and 'output' columns including nulls.")
