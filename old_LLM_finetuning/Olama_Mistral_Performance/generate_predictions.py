import pandas as pd
from tqdm import tqdm
from ollama import chat

# === Step 1: Load your labeled dataset ===
df = pd.read_csv("risk_data_formatted.csv")  # <-- replace with your real CSV filename
df[["input", "output"]].to_csv("ground_truth.csv", index=False)

# === Step 2: Define prompt construction ===
def build_prompt(text):
    return f"""
You are a risk communication analysis assistant.

Your task is to analyze the following text and extract structured risk communication data.

First, determine if the text contains risk communication. If it does, set "Risk communication: 1". Otherwise, set it to "Risk communication: 0" and return null for all other fields.

Return the result as plain text using the format:  
Field name: value  
Use one field per line, and write "null" if the value is not available.

Here are the fields you should extract, along with a short explanation:

- Risk communication: 1 if the sentence communicates risk; otherwise 0  
- Absolute risk (base case): % or ratio before any intervention (e.g. "10%" or "30 in 1000")  
- Absolute risk (new case): % or ratio after intervention or change  
- Absolute number (base case): count of affected individuals before change  
- Absolute number (new case): count of affected individuals after change  
- Absolute risk difference: difference between base and new risk (e.g. "5%")  
- Relative risk: relative change (e.g. "10% increase", "50% reduction")  
- Absolute number difference: change in absolute numbers (e.g. "500 fewer")  
- Verbal risk descriptor (base case): qualitative risk term before change (e.g. "rare")  
- Verbal risk descriptor (new situation): qualitative term after change (e.g. "high risk")  
- Verbal risk descriptor (change from base to new): e.g. "significantly higher"  
- Reference class size (base case: absolute number): total population size for base case  
- Reference class size (new case: absolute number): total population size for new case  
- Reference class description (base case): group description (e.g. "general population")  
- Reference class description (new case): changed group (e.g. "patients on aspirin")  
- Population (übergeordnete Grundgesamtheit): higher-level population the risk applies to  
- Source (base case): where the base risk data comes from (e.g. "CDC")  
- Source (new situation): source for the changed/new risk (e.g. "NHS")  
- Topic and unit: what the risk is about, and the time or unit it refers to (e.g. "lung cancer per year")

---

Example:

Text:  
"The risk of heart failure is 10%. By taking our medication, it decreases to 5%. This result comes from a study on 100,000 patients from the general population."

Output:  
Risk communication: 1  
Absolute risk (base case): 10%  
Absolute risk (new case): 5%  
Absolute number (base case): null  
Absolute number (new case): null  
Absolute risk difference: 5%  
Relative risk: 50%  
Absolute number difference: null  
Verbal risk descriptor (base case): null  
Verbal risk descriptor (new situation): null  
Verbal risk descriptor (change from base to new): null  
Reference class size (base case: absolute number): 100000  
Reference class size (new case: absolute number): 100000  
Reference class description (base case): general population  
Reference class description (new case): general population  
Population (übergeordnete Grundgesamtheit): null  
Source (base case): null  
Source (new situation): null  
Topic and unit: heart failure risk per person

Now analyze the following text:  
\"\"\"{text}\"\"\"
"""

# === Step 3: Generate predictions ===
pred_outputs = []

for text in tqdm(df["input"], desc="Generating predictions"):
    response = chat(
        model="mistral",
        messages=[{"role": "user", "content": build_prompt(text)}],
        options={"temperature": 0.0}  # deterministic
    )
    raw_output = response["message"]["content"].strip()

    # Remove markdown-style fences if they exist (e.g. ```json ... ```)
    if raw_output.startswith("```"):
        raw_output = raw_output.split("```")[-2].strip()

    pred_outputs.append(raw_output)

# === Step 4: Save predictions ===
pred_df = pd.DataFrame({
    "input": df["input"],
    "output": pred_outputs
})
pred_df.to_csv("model_outputs.csv", index=False)

print("✅ Saved ground_truth.csv and model_outputs.csv")
