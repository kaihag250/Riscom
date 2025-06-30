def extract_selected_attributes(llm_output: str) -> str:
    # The fields you always want to extract (in this order)
    target_keys = [
        "risk_communication",
        "unrelated_risks",
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

    output_lines = []
    for key in target_keys:
        value = result.get(key, "null")
        output_lines.append(f"{key}: {value}")


    return "\n".join(output_lines)