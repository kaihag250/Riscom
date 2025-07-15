from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Modell & Tokenizer laden
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Prompt definieren
prompt = (
    "Please extract the following information, if possible and only if it is directly given in the sentence. "
    "The base risk, the new absolute risk, and the relative risk. "
    "Name the name of the number and then the number itself. "
    "If the number is not directly given, write 'number not directly given'. "
    "Sentence: The risk of heart failure is 10%. Alcohol doubles this risk."
)

# Tokenisieren
inputs = tokenizer(prompt, return_tensors="pt")

# Ausgabe generieren
outputs = model.generate(
    **inputs,
    max_length=128,
    num_beams=4,
    early_stopping=True
)

# Ausgabe dekodieren
output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Ergebnisse anzeigen
print("📥 Prompt:")
print(prompt)
print("\n🧠 Modellantwort:")
print(output_text)

#push Kai