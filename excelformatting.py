import pandas as pd

# === 1. Load the Excel file ===
df = pd.read_excel("Excel_version1506.xlsx")

# === 2. Define the text and output fields ===
text_col = "Unnamed: 0"

output_fields = [
    'risk_communication',
    'single_case_base',
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
    'population_size',
    'reference_class_size_base',
    'reference_class_size_new',
    'reference_class_description_base',
    'reference_class_description_new',
    'source_base',
    'source_new',
    'topic_and_unit'
]
# === 3. Format output string ===
def format_output(row):
    lines = []
    for col in output_fields:
        val = row.get(col)
        if pd.isna(val):
            lines.append(f"{col}: null")
        else:
            lines.append(f"{col}: {val}")
    return "\n".join(lines)

# === 4. Build training DataFrame ===
formatted_df = pd.DataFrame()
formatted_df["input"] = df[text_col]
formatted_df["output"] = df.apply(format_output, axis=1)

# Drop rows with missing input text
formatted_df = formatted_df.dropna(subset=["input"])

# === 5. Save to CSV ===
output_path = "risk_data_formatted.csv"
formatted_df.to_csv(output_path, index=False)
print(f"✅ Saved: {output_path} with 'input' and 'output' columns including nulls.")
