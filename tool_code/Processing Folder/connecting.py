outputstring ="""

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
def main():
    cutoutput = extract_selected_attributes(outputstring)

    risk_data = Dataextractor()
    risk_data.load_from_text(cutoutput)
    print(risk_data, "hallo")


    eval_result = risk_data.process()
    print()
    print(eval_result)


def extract_selected_attributes(llm_output: str) -> str:
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

    output_lines = []
    for key in target_keys:
        value = result.get(key, "null")
        output_lines.append(f"{key}: {value}")


    return "\n".join(output_lines)
class Dataextractor:
    def __init__(self):
        self.risk_communication = None
        self.single_case_base = None
        self.absolute_risk_base = None
        self.absolute_risk_new = None
        self.absolute_number_base = None
        self.absolute_number_new = None
        self.absolute_risk_difference = None
        self.relative_risk = None
        self.absolute_number_difference = None
        self.verbal_descriptor_base = None
        self.verbal_descriptor_new = None
        self.verbal_descriptor_change = None
        self.population_size = None
        self.reference_class_size_base = None
        self.reference_class_size_new = None
        self.reference_class_description_base = None
        self.reference_class_description_new = None
        self.source_base = None
        self.source_new = None
        self.topic_and_unit = None

    def load_from_text(self, raw_output: str):
        for line in raw_output.strip().splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Wert konvertieren
                if value.lower() == "null":
                    parsed_value = None
                else:
                    try:
                        parsed_value = float(value)
                    except ValueError:
                        parsed_value = value

                # Nur wenn Attribut existiert, setzen
                if hasattr(self, key):
                    setattr(self, key, parsed_value)

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in self.__dict__.items())
    
    def process(self):
        output = []

        if self.risk_communication == 0:
            output.append("No risk communication provided.")
            return "\n".join(output)

        if self.single_case_base == 1:
            output.append("Single Risk Scenario")
        else:
            output.append("Two Risk Scenarios")

        output.append("\n--- Calculating missing figures ---")

        if self.single_case_base == 0:
            if self.absolute_number_difference is not None:
                if self.absolute_number_base is not None and self.absolute_number_new is None:
                    self.absolute_number_new = self.absolute_number_base + self.absolute_number_difference
                    output.append(f"absolute number (new) = {self.absolute_number_new}")
                elif self.absolute_number_new is not None and self.absolute_number_base is None:
                    self.absolute_number_base = self.absolute_number_new - self.absolute_number_difference
                    output.append(f"absolute number (base) = {self.absolute_number_base}")

        if self.absolute_number_base is not None and self.reference_class_size_base is not None:
            calculated_base = (self.absolute_number_base / self.reference_class_size_base) * 100
            if self.absolute_risk_base is None:
                self.absolute_risk_base = calculated_base
                output.append(f"Calculated absolute risk (base) = {self.absolute_risk_base:.2f}%")
        if self.absolute_number_new is not None and self.reference_class_size_new is not None:
            calculated_new = (self.absolute_number_new / self.reference_class_size_new) * 100
            if self.absolute_risk_new is None:
                self.absolute_risk_new = calculated_new
                output.append(f"Calculated absolute risk (new) = {self.absolute_risk_new:.2f}%")

        if self.relative_risk is not None:
            if self.absolute_risk_base is not None and self.absolute_risk_new is None:
                self.absolute_risk_new = self.absolute_risk_base * self.relative_risk
                output.append(f"From relative risk and base absolute risk calculated: absolute risk (new) = {self.absolute_risk_new:.2f}%")
            elif self.absolute_risk_new is not None and self.absolute_risk_base is None:
                self.absolute_risk_base = self.absolute_risk_new / self.relative_risk
                output.append(f"From relative risk and new absolute risk calculated: absolute risk (base) = {self.absolute_risk_base:.2f}%")

        if self.absolute_risk_base is not None and self.absolute_risk_new is not None:
            calculated_rel = self.absolute_risk_new / self.absolute_risk_base if self.absolute_risk_base != 0 else None
            if self.relative_risk is None and calculated_rel is not None:
                self.relative_risk = calculated_rel
                output.append(f"Calculated relative risk difference = {self.relative_risk:.2f}")

        output.append("\n--- Qualitative Assessment ---")
        if self.source_base or self.source_new:
            output.append("Sources provided – please verify:")
            if self.source_base:
                output.append(f"     • Source for base risk: {self.source_base}")
            if self.source_new:
                output.append(f"     • Source for new risk: {self.source_new}")
        else:
            output.append("Warning: No sources provided.")

        if self.verbal_descriptor_base or self.verbal_descriptor_new or self.verbal_descriptor_change:
            output.append("Warning: Verbal risk descriptors present. Please verify definitions for:")
            if self.verbal_descriptor_base:
                output.append(f"     • verbal_risk_descriptor_base: {self.verbal_descriptor_base}")
            if self.verbal_descriptor_new:
                output.append(f"     • verbal_risk_descriptor_new: {self.verbal_descriptor_new}")
            if self.verbal_descriptor_change:
                output.append(f"     • verbal_risk_descriptor_change: {self.verbal_descriptor_change}")

        if not (self.reference_class_description_base or self.reference_class_description_new):
            output.append("Warning: No reference class provided. Please check the text for an explicit description.")

        output.append("\n--- Missing Values Check ---")
        if self.single_case_base == 1:
            if self.absolute_risk_base is not None:
                output.append("Absolute risk calculable.")
            else:
                output.append("Warning: No absolute risk provided or calculable – risk communication not transparent.")
        else:
            if self.absolute_risk_base is not None and self.absolute_risk_new is not None:
                output.append("Both absolute risks calculable. Risk communication transparent.")
            elif self.absolute_risk_base is None and self.absolute_risk_new is not None:
                output.append("Warning: Missing absolute risk for base case, but new absolute risk provided – risk communication not transparent.")
            elif self.absolute_risk_base is not None and self.absolute_risk_new is None:
                output.append("Warning: Base absolute risk provided, but new absolute risk missing – risk communication not transparent.")
            else:
                output.append("Warning: Neither absolute risk provided nor calculable – risk communication not transparent.")

        output.append("\n--- Transparent Presentation ---")
        if self.absolute_risk_base is not None:
            output.append(f"Absolute risk (base): {self.absolute_risk_base:.2f}% ({self.absolute_risk_base:.2f} per 100)")
        if self.absolute_risk_new is not None:
            output.append(f"Absolute risk (new): {self.absolute_risk_new:.2f}% ({self.absolute_risk_new:.2f} per 100)")
        if self.relative_risk is not None:
            change_pct = abs((self.relative_risk - 1) * 100)
            if self.relative_risk < 1:
                output.append(f"The risk in the new case is {change_pct:.2f}% lower than in the base case.")
            elif self.relative_risk > 1:
                output.append(f"The risk in the new case is {change_pct:.2f}% higher than in the base case.")
            else:
                output.append("The risk in the new case is the same as in the base case.")

        return "\n".join(output)
if __name__ == "__main__":
    main()
