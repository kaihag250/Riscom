from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
from peft import PeftModel
import torch

BASE_MODEL = "mistralai/Mistral-7B-v0.1"
ADAPTER_PATH = "./adapters/adapter-11.07"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True
)

print("🚀 Lade Basis-Modell:", BASE_MODEL)
base = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype="auto"
)
base.eval()
base.gradient_checkpointing_disable()
base.config.use_cache = True

print("🔌 Lade LoRA-Adapter:", ADAPTER_PATH)
model = PeftModel.from_pretrained(base, ADAPTER_PATH)
model.eval()

tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
    torch_dtype="auto",
    max_new_tokens=300,
    do_sample=False,
    return_full_text=True,
    use_cache=True,
)

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
    "- source_base\n"
    "- source_new\n"
)

def run_inference(input_text: str) -> str:
    prompt = INSTRUCTION + f"\n### Input:\n{input_text.strip()}\n\n### Output:\n"
    outputs = pipe(prompt)
    result = outputs[0]["generated_text"]
    result = result.split("### Output:")[-1].strip()
    return result