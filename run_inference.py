import os
import torch
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from tqdm import tqdm

# === Paths (adjust to your user directory) ===
HOME = os.path.expanduser("~")

BASE_MODEL_PATH = os.path.join(HOME, "mistral-7b")
ADAPTER_PATH = os.path.join(HOME, "adapter-0507_nosource")
INPUT_CSV = os.path.join(HOME, "groundtruth.csv")
OUTPUT_CSV = os.path.join(HOME, "predictions.csv")


# === Fixed instruction prompt ===
INSTRUCTION = (
    "### Instruction:\n"
    "From the input text, extract the following fields ONLY.\n"
    "Format your response as newline-separated entries:\n\n"
    "category: value\n\n"
    "Do NOT include any additional text, headings, or explanations.\n\n"
    "Fields to extract:\n"
    "- risk_communication\n"
    "- unrelated_risks\n"
    "- absolute_risk_base\n"
    "- absolute_risk_new\n"
    "- absolute_number_base\n"
    "- absolute_number_new\n"
    "- absolute_risk_difference\n"
    "- relative_risk\n"
    "- absolute_number_difference\n"
    "- verbal_descriptor_base\n"
    "- verbal_descriptor_new\n"
    "- verbal_descriptor_change\n"
    "- reference_class_size_base\n"
    "- reference_class_size_new\n"
    "- reference_class_description_base\n"
    "- reference_class_description_new\n"
)

# === BitsAndBytes 4-bit QLoRA configuration ===
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

# === Load model and tokenizer from local files only ===
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_PATH,
    quantization_config=bnb_config,
    device_map="auto",
    local_files_only=True,
    trust_remote_code=True,
)
model = PeftModel.from_pretrained(model, ADAPTER_PATH, local_files_only=True)
model.eval()

# === Load the input CSV ===
df = pd.read_csv(INPUT_CSV)
assert "input" in df.columns, "Column 'input' not found in the CSV file."

# === Run inference ===
predictions = []
print("Running inference...")

for _, row in tqdm(df.iterrows(), total=len(df)):
    input_text = row["input"]
    full_prompt = f"{INSTRUCTION}\n\n{input_text.strip()}\n### Response:\n"

    inputs = tokenizer(full_prompt, return_tensors="pt", truncation=True, max_length=2048).to(model.device)

    with torch.no_grad():
        output_tokens = model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )
    decoded = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
    prediction = decoded.split("### Response:")[-1].strip()
    predictions.append(prediction)

# === Save results ===
df_out = pd.DataFrame({
    "input": df["input"],
    "prediction": predictions
})
df_out.to_csv(OUTPUT_CSV, index=False)
print(f"Done. Predictions saved to: {OUTPUT_CSV}")