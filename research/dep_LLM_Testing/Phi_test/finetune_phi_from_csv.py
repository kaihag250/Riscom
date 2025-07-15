import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch

# CSV einlesen
df = pd.read_csv("Phi_test/train_data.csv")

# Modell & Tokenizer laden
model_id = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")

# Daten vorbereiten
inputs = tokenizer(list(df["prompt"]), padding=True, truncation=True, return_tensors="pt")
labels = tokenizer(list(df["response"]), padding=True, truncation=True, return_tensors="pt").input_ids
inputs["labels"] = labels

# Trainingsargumente
training_args = TrainingArguments(
    output_dir="./phi-finetuned",
    per_device_train_batch_size=1,
    num_train_epochs=3,
    logging_steps=1,
    save_strategy="epoch",
    report_to="none"
)

# Trainer definieren
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=inputs
)

# Training starten
trainer.train()

# Modell speichern
model.save_pretrained("./phi-finetuned")
tokenizer.save_pretrained("./phi-finetuned")