from transformers import BartTokenizer, BartForConditionalGeneration

# Modell und Tokenizer laden (hier: 'facebook/bart-large')
model_name = "facebook/bart-large"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Beispieltext – kann durch Text mit schlechter Risikokommunikation ersetzt werden
text = "Only 10% of patients die after the treatment. It greatly reduces cancer risk."

# Tokenisierung
inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)

# Generierung – hier optional 'summarize:' als Prefix, falls ihr T5 gewohnt seid
summary_ids = model.generate(inputs["input_ids"], max_length=100, num_beams=4, early_stopping=True)

# Ergebnis decodieren
output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print("fuxk uff:")
print(text)
print("\nGenerierter Text:")
print(output)

#push Kai
#lol adri