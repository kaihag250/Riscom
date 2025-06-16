
def extract_selected_attributes(llm_output: str) -> dict:
    # The fields you always want to extract (in this order)
    target_keys = [
        "risk_communication",
        "single_case_base",
        "absolute_risk_base",
        "absolute_risk_new",
        "absolute_number_base",
        "absolute_number_new",
        "absolute_risk_difference",
        "relative_risk",
        "absolute_number_difference",
        "verbal_descriptor_base",
        "verbal_descriptor_new",
        "verbal_descriptor_change",
        "population_size",
        "reference_class_size_base",
        "reference_class_size_new",
        "reference_class_description_base",
        "reference_class_description_new",
        "source_base",
        "source_new",
        "topic_and_unit"
    ]

    in_output_section = False
    result = {key: None for key in target_keys}

    for line in llm_output.splitlines():
        line = line.strip()

        if line.startswith("### Output:"):
            in_output_section = True
            continue
        elif in_output_section and line.startswith("###"):
            break  # Exit once another section starts

        if in_output_section and ":" in line:
            key, value = map(str.strip, line.split(":", 1))
            if key in target_keys:
                result[key] = value

    return result


outputBeispiel = """
### Output:
risk_communication: 1.0
single_case_base: 1.0
absolute_risk_base: 0.1
absolute_risk_new: null
absolute_number_base: null
absolute_number_new: null
absolute_risk_difference: null
relative_risk: null
absolute_number_difference: null
verbal_descriptor_base: null
verbal_descriptor_new: null
verbal_descriptor_change: null
population_size: null
reference_class_size_base: null
reference_class_size_new: null
reference_class_description_base: people who dont smoke
reference_class_description_new: smokers
source_base: null
source_new: null
topic_and_unit: risk of developing lung cancer in % over a lifetime of smokers compared to non-smokers

### Reference:
null

### Features:
null

### Example:
null

### Date:
2020-05-01 08:00:00.0

### Detection language:
null

### Detection type:
null

### Sentiment:
null

### Sentiment score:
null

### Confidence:
null
"""
print(extract_selected_attributes(outputBeispiel))