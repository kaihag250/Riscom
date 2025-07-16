# inference_worker.py

from llama_cpp import Llama

MODEL_PATH = "/mnt/llm/mistral-7-7-Q8.gguf"

FIELDS_PROMPT = """
### Instruction:
Extract ONLY the following fields from the input text.
Format the output as newline-separated 'category: value' pairs.
Do NOT include any explanations, comments, or additional text of any kind.
DO NOT add extra information. Only fill in the fields exactly.

Fields to extract:
- risk_communication
- unrelated_risks
- absolute_risk_base
- absolute_risk_new
- absolute_number_base
- absolute_number_new
- absolute_risk_difference
- relative_risk
- absolute_number_difference
- verbal_descriptor_base
- verbal_descriptor_new
- verbal_descriptor_change
- population_size
- reference_class_description_base
- reference_class_description_new
- reference_class_size_base
- reference_class_size_new
- source_base
- source_new

"""

print("Lade GGUF-Modell ...")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=16,
    n_batch=128,
    verbose=False
)
print("Modell geladen!")

def run_inference(input_text: str) -> str:
    prompt = FIELDS_PROMPT + "\n" + input_text
    print("\n Prompt an LLM:\n", prompt)
    output = llm(prompt, max_tokens=220, stop=["</s>"])
    raw = output["choices"][0]["text"].strip()
    print("\n Roh-Output vom Modell:\n", raw)
    return raw

