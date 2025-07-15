from Risk_model import Risk
from ollama import chat
import json, os

# 1 Prompt für die Analyse vorbereiten
if risk_comm := input("Enter the sentence containing risk communication: "):
    prompt = f"""
You are a risk communication analysis assistant.

Please analyze the following risk communication text:

"{risk_comm}"

Your task is to extract the following fields from the text in JSON format.

Important:
- Only extract values that are explicitly stated in the text.
- If a value is not explicitly mentioned, set the field to null.
- Do NOT perform any mathematical calculations or transformations. If a risk is described as a ratio or fraction (e.g. '10 in 300'), please include it exactly as stated (e.g. '10/300' or 0.05).
- Always include all fields in the JSON output, even if they are null.

The fields are:
- risk_com: Binary variable (1 if the text contains risk communication, 0 otherwise).
- one_case: Binary variable (1 if the text contains only one case of risk and no alternative cases, 0 otherwise).
- absolute_risk_base: The absolute risk (%) in the base case.
- absolute_risk_new: The absolute risk (%) in the new case.
- absolute_number_base: The absolute number of cases in the base case.
- absolute_number_new: The absolute number of cases in the new case.
- absolute_risk_difference: The difference in absolute risk (%) between base and new case.
- relative_risk: The relative risk (%) comparing new and base case.
- absolute_number_difference: The difference in absolute number of cases between base and new case.
- verbal_risk_descriptor_base: The verbal risk descriptor in the base case.
- verbal_risk_descriptor_new: The verbal risk descriptor in the new case.
- verbal_risk_descriptor_change: The change in verbal risk descriptor from base to new case.
- reference_class_size_base: The reference class size (base case).
- reference_class_size_new: The reference class size (new case).
- reference_class_description_base: Description of the reference class (base case).
- reference_class_description_new: Description of the reference class (new case).
- source_base: Source information (base case).
- source_new: Source information (new case).
- topic_and_unit: Topic and unit of the risk communication.

Output requirements:
- Output a single JSON object only.
- Ensure that all fields from the schema are included in the JSON object, even if their value is null.

Example JSON output format for the sentence "The risk of a heart attack in the general population is 10%, as clinical trial A reveals. Clinical trial B, however, shows that patients receiving our medical treatment have a 5% risk of getting a heart attack.":
{{
    "risk_com": 1,
    "one_case": 0, 
    "absolute_risk_base": 10.0,
    "absolute_risk_new": 5.0,
    "absolute_number_base": null,
    "absolute_number_new": null,
    "absolute_risk_difference": null,
    "relative_risk": null,
    "absolute_number_difference": null,
    "verbal_risk_descriptor_base": null,
    "verbal_risk_descriptor_new": null,
    "verbal_risk_descriptor_change": null,
    "reference_class_size_base": null,
    "reference_class_size_new": null,
    "reference_class_description_base": "general population",
    "reference_class_description_new": "patients after treatment",
    "source_base": "clinical trial A",
    "source_new": "clinical trial B",
    "topic_and_unit": "risk of heart attack per person"
}}

Now, please analyze the provided text and respond only with the JSON object.
"""

    # 2 Request an das LLM senden
    response = chat(
        model="mistral:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={"temperature": 0.2},  # ausprobieren, wie sich Ergebnisse verhalten
        format=Risk.model_json_schema()
    )

    # 3 Antwort in das Pydantic-Modell laden -> habe jetzt ein Python-Objekt mit allen Werten 
    # Falls validate fehlschlägt, dann wirft Exception 
    classification = Risk.model_validate_json(response.message.content)
    print(classification)


# Kann diesen Schritt überspringen, falls ich keine JSON-Datei brauche 
    # 4 JSON-Datei erzeugen -> LLM Output als JSON gespeichert
    os.makedirs("output", exist_ok=True)
    file_name = "4risk_example"
    with open(f"output/{file_name}.json", "w") as f:
        f.write(classification.model_dump_json(exclude_none=False))


# example1: The risk of heart failure is 10%. By taking our medication, it decreases to 5%. 
# example2: The risk of heart failure is 10 in 200 people. By taking our medication, it is 50% smaller.
