class RiskEvaluator:
    def __init__(self):
        # Originale LLM-Werte
        self.risk_communication = None
        self.unrelated_risk = None
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
        self.reference_class_size_base = None
        self.reference_class_size_new = None
        self.reference_class_description_base = None
        self.reference_class_description_new = None
        self.source_base = None
        self.source_new = None
        self.topic_and_unit = None

        # LLM-Werte als Dictionary speichern
        # -> Evtl. die Werte direkt ins Dicitionary packen anstatt Klassenvariablen
        self.llm_values = {
            "risk_communication": self.risk_communication,
            "unrelated_risk": self.unrelated_risk,
            "absolute_risk_base": self.absolute_risk_base,
            "absolute_risk_new": self.absolute_risk_new,
            "absolute_number_base": self.absolute_number_base,
            "absolute_number_new": self.absolute_number_new,
            "absolute_risk_difference": self.absolute_risk_difference,
            "relative_risk": self.relative_risk,
            "absolute_number_difference": self.absolute_number_difference,
            "verbal_descriptor_base": self.verbal_descriptor_base,
            "verbal_descriptor_new": self.verbal_descriptor_new,
            "verbal_descriptor_change": self.verbal_descriptor_change,
            "reference_class_size_base": self.reference_class_size_base,
            "reference_class_size_new": self.reference_class_size_new,
            "reference_class_description_base": self.reference_class_description_base,
            "reference_class_description_new": self.reference_class_description_new,
            "source_base": self.source_base,
            "source_new": self.source_new,
            "topic_and_unit": self.topic_and_unit,
        }

        # Arbeitskopie
        self.working_values = self.llm_values.copy()

        # Ergebnis-Output
        self.output = {
            "eval_1": None,
            "eval_2": None,
            "eval_3_abs_base": None, 
            "eval_3_abs_new": None, 
            "eval_3_relative": None,
            "message_quant": None,
            "message_reference": None,
            "message_verbal": None,
            "message_source": None,
            "eval_case_overall": None
        }
    

    # Extrahiert Variablen aus dem String
    def load_from_text(self, raw_output: str):
        for line in raw_output.strip().splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Wert konvertieren
                if value.lower() == "null":
                    parsed_value = None
                elif value.endswith('%'):
                    try:
                        value = value.replace(",", ".")  # Komma in Punkt wandeln
                        parsed_value = float(value.strip('%')) / 100
                    except ValueError:
                        parsed_value = value
                else:
                    try:
                        value = value.replace(",", ".")  # Komma in Punkt wandeln
                        # Wert als Zahl oder Ausdruck parsen (z.B. 2/100 → 0.02)
                        parsed_value = eval(value, {"__builtins__": {}})
                        if not isinstance(parsed_value, (int, float)):
                            parsed_value = value
                    except:
                        parsed_value = value

                # Nur wenn Attribut existiert, setzen
                if hasattr(self, key):
                    setattr(self, key, parsed_value)
        # NEU !!!!!!!!
        self.update_value_dictionaries()

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in self.__dict__.items())
    
    # NEUE Methode !!!!!!!!
    def update_value_dictionaries(self):
        self.llm_values = {
            "risk_communication": self.risk_communication,
            "unrelated_risk": self.unrelated_risk,
            "absolute_risk_base": self.absolute_risk_base,
            "absolute_risk_new": self.absolute_risk_new,
            "absolute_number_base": self.absolute_number_base,
            "absolute_number_new": self.absolute_number_new,
            "absolute_risk_difference": self.absolute_risk_difference,
            "relative_risk": self.relative_risk,
            "absolute_number_difference": self.absolute_number_difference,
            "verbal_descriptor_base": self.verbal_descriptor_base,
            "verbal_descriptor_new": self.verbal_descriptor_new,
            "verbal_descriptor_change": self.verbal_descriptor_change,
            "reference_class_size_base": self.reference_class_size_base,
            "reference_class_size_new": self.reference_class_size_new,
            "reference_class_description_base": self.reference_class_description_base,
            "reference_class_description_new": self.reference_class_description_new,
            "source_base": self.source_base,
            "source_new": self.source_new,
            "topic_and_unit": self.topic_and_unit,
        }

        self.working_values = self.llm_values.copy()


    # Vergleicht, was berechnet wurde und was nicht 
    def was_berechnet(self, varname):
        return (
            self.llm_values.get(varname) is None
            and self.working_values.get(varname) is not None
        )

    # Case Zuordnung und Berechnungen 
    def evaluate(self):
        w = self.working_values  # Alias für bessere Lesbarkeit

    # 1. BAUM -----------------------------------------------------------------------------
        # 1. Check: Risiko-Kommunikation vorhanden?
        if not w["risk_communication"]:
            self.output["eval_1"] = "NR"
        
        # 2. Check: Unrelated risks im selektierten Textausschnitt?
        elif w["unrelated_risk"]:
            self.output["eval_1"] = "UR"
        
        # 3. Keine Zahleninformationen vorhanden? -> AUSBAUEN zu NN2, NNB, NNN
        elif all(w[key] is None for key in [
            "absolute_risk_base", "absolute_risk_new", "relative_risk", "absolute_number_base",
            "absolute_number_new", "absolute_risk_difference",
            "absolute_number_difference",
            "reference_class_size_base", "reference_class_size_new"]):
            self.output["eval_1"] = "NN"
        else:
            self.output["eval_1"] = "NG"
    
    # 2. BAUM -----------------------------------------------------------------------------
        # Nur gestartet, falls Risikoinformation und keine unrelated risk
        if self.output["eval_1"] != "NR" and self.output["eval_1"] != "UR":
            if all(w[key] is None for key in [
                "absolute_risk_difference", "relative_risk", "absolute_number_difference", "verbal_descriptor_change", 
                "absolute_risk_new", "absolute_number_new", "reference_class_size_new", 
                "reference_class_description_new", "verbal_descriptor_new"]):
                self.output["eval_2"] = "SB"
            elif all(w[key] is None for key in [
                "absolute_risk_difference", "relative_risk", "absolute_number_difference", "verbal_descriptor_change", 
                "absolute_risk_base", "absolute_number_base", "reference_class_size_base", 
                "reference_class_description_base", "verbal_descriptor_base"]):
                self.output["eval_2"] = "SN"
            else: 
                self.output["eval_2"] = "S2"
    
    # 3. BAUM -----------------------------------------------------------------------------
        # Berechnungslogik, falls Case != NR, UR, NN
        if self.output["eval_1"] != "NR" and self.output["eval_1"] != "UR" and self.output["eval_1"] != "NN":
            # Absolute Zahlen ergänzen, wenn Differenz bekannt
            if w["absolute_number_difference"] is not None:
                if w["absolute_number_base"] is not None and w["absolute_number_new"] is None:
                    w["absolute_number_new"] = w["absolute_number_base"] + w["absolute_number_difference"]
                elif w["absolute_number_new"] is not None and w["absolute_number_base"] is None:
                    w["absolute_number_base"] = w["absolute_number_new"] - w["absolute_number_difference"]

            # Absolute Risiken berechnen aus Zahlen + Referenzgrößen -> aber nicht gegebenes absolutes Risiko überschreiben
            if w["absolute_number_base"] is not None and w["reference_class_size_base"] is not None and w["absolute_risk_base"] is None:
                w["absolute_risk_base"] = w["absolute_number_base"] / w["reference_class_size_base"]
            if w["absolute_number_new"] is not None and w["reference_class_size_new"] is not None and w["absolute_risk_new"] is None:
                w["absolute_risk_new"] = w["absolute_number_new"] / w["reference_class_size_new"]

            # Absolute Risiko aus anderem absolutem Risiko und absolute risk difference
            if w["absolute_risk_base"] is not None and w["absolute_risk_difference"] is not None and w["absolute_risk_new"] is None:
                w["absolute_risk_new"] = w["absolute_risk_base"] + w["absolute_risk_difference"]
            if w["absolute_risk_new"] is not None and w["absolute_risk_difference"] is not None and w["absolute_risk_base"] is None:
                w["absolute_risk_base"] = w["absolute_risk_new"] - w["absolute_risk_difference"]

            # Relatives Risiko → berechne fehlende absolute Risiken
            if w["relative_risk"] is not None:
                if w["absolute_risk_base"] is not None and w["absolute_risk_new"] is None:
                    w["absolute_risk_new"] = w["absolute_risk_base"] * (w["relative_risk"]) # Konsistenz überprüfen !!!
                elif w["absolute_risk_new"] is not None and w["absolute_risk_base"] is None:
                    w["absolute_risk_base"] = w["absolute_risk_new"] / (w["relative_risk"]) # Konsistenz überprüfen !!!

            # Relatives Risiko berechnen, falls möglich
            if w["absolute_risk_base"] and w["absolute_risk_new"] and w["relative_risk"] is None:
                w["relative_risk"] = (w["absolute_risk_new"] / w["absolute_risk_base"]) # Konsistenz prüfen !!!
            

            # Überprüfung was berechnet wurde und was nicht
            # Absolute_risk base 
            if self.llm_values.get("absolute_risk_base") is not None:
                self.output["eval_3_abs_base"] = "G"
            elif self.was_berechnet("absolute_risk_base"):
                self.output["eval_3_abs_base"] = "C"
            else:
                self.output["eval_3_abs_base"] = "N"
            # Absolute_risk new 
            if self.llm_values.get("absolute_risk_new") is not None:
                self.output["eval_3_abs_new"] = "G"
            elif self.was_berechnet("absolute_risk_new"):
                self.output["eval_3_abs_new"] = "C"
            else:
                self.output["eval_3_abs_new"] = "N"
            # Relative risk
            if self.llm_values.get("relative_risk") is not None:
                self.output["eval_3_relative"] = "G"
            elif self.was_berechnet("relative_risk"):
                self.output["eval_3_relative"] = "C"
            else:
                self.output["eval_3_relative"] = "N"
    
    # 4. BAUM ----------------------------------------------------------------------------------------------------------------------------
        # Zusammensetzen der Informationen zu einer Nachricht
        message_quant = ""

        # eval_1 == NR
        if self.output["eval_1"] == "NR":
            message_quant += "No risk communication detected in the given text extract.\n"
            self.output["eval_case_overall"] = "NR"
        # eval_1 != NR -> Risk communication detected
        else: 
            message_quant += "Risk communication detected\n\n"

        # eval_1 == UR -> unrelated risks
        if self.output["eval_1"] == "UR":
            message_quant += (
                "There are two unrelated risks in the selected text.\n"
                "Please select a new text extract.\n"
            )
            self.output["eval_case_overall"] = "UR" ##########################

        # Unrelated risk und No risk muss von allem zukünftigen ausgeschlossen werden
        if self.output["eval_1"] != "UR" and self.output["eval_1"] != "NR":
            # eval_1 == NN -> Quantitative information?
            if self.output["eval_1"] == "NN":
                message_quant += "ATTENTION: No quantitative risk information is included.\n"
                self.output["eval_case_overall"] = "NN" ##############################
            else:
                message_quant += "The tool detected quantitative risk information.\n"
            
            # eval_2 Add-on zur Nachricht -> Single Case Base, New or Two Cases?
            if self.output["eval_2"] == "S2":
                message_quant += "Two risk scenarios for different treatment groups detected.\n\n"
            elif self.output["eval_2"] == "SB":
                message_quant += "The text describes one base risk scenario.\n\n"
            elif self.output["eval_2"] == "SN":
                message_quant += "ATTENTION: The text describes a risk for a subgroup but does not provide a comparison to the overall or baseline risk.\n\n"

            # Ausgabe der quantitativen Zahlen -> eval_1 != NN 
            if self.output["eval_1"] == "NG":
                # SINGLE CASE
                # Angabe für eval_2 == SB
                if self.output["eval_2"] == "SB":
                    if self.output["eval_3_abs_base"] == "G":
                        message_quant += f"The absolute risk is: {self.llm_values.get('absolute_risk_base') * 100:.4g}%\n"
                        self.output["eval_case_overall"] = "R1.1" #################
                    elif self.output["eval_3_abs_base"] == "C":
                        message_quant += "The tool calculated the absolute risk with the extracted information.\n"
                        message_quant += f"The calculated absolute risk for the given reference group is: {w['absolute_risk_base'] * 100:.4g}%\n"
                        self.output["eval_case_overall"] = "R2.1" #################
                    elif self.output["eval_3_abs_base"] == "N":
                        message_quant += "ATTENTION: The absolute risk was neither given nor calculable.\n"
                        self.output["eval_case_overall"] = "R3.1" #################
                # Angabe für eval_2 == SN
                elif self.output["eval_2"] == "SN":
                    if self.output["eval_3_abs_new"] == "G":
                        message_quant += f"The absolute risk is: {self.llm_values.get('absolute_risk_new') * 100.0:.4g}%\n"
                        self.output["eval_case_overall"] = "R1.2" #################
                        print("TEST")
                    elif self.output["eval_3_abs_new"] == "C":
                        message_quant += "The tool calculated the absolute risk with the extracted information.\n"
                        message_quant += f"The calculated absolute risk for the given reference group is: {w['absolute_risk_base'] * 100:.4g}%\n"
                        self.output["eval_case_overall"] = "R2.2" #################
                    elif self.output["eval_3_abs_new"] == "N":
                        message_quant += "ATTENTION: The absolute risk was neither given nor calculable.\n"
                        self.output["eval_case_overall"] = "R3.2" #################

                # TWO CASES
                # Angabe für eval_2 = S2
                elif self.output["eval_2"] == "S2":
                    # Für TWO CASE Fall-Asugabe, was berechnet wurde
                    calculated = []
                    calculated_string = ""
                    if self.was_berechnet("absolute_risk_base"):
                        calculated.append("absolute risk in the base case")
                    if self.was_berechnet("absolute_risk_new"):
                        calculated.append("absolute risk in the new case")
                    if self.was_berechnet("relative_risk"):
                        calculated.append("relative risk")
                    if calculated:
                        calculated_string += "The tool calculated the following values: " + ", ".join(calculated) + ".\n"

                    # Initial Transparent (L1)
                    # Beide absoluten Risiken und relatives Risiko gegeben
                    if self.output["eval_3_abs_base"] == "G" and self.output["eval_3_abs_new"] == "G" and self.output["eval_3_relative"] == "G":
                        message_quant += f"The absolute risk in the base case is: {self.llm_values.get('absolute_risk_base') * 100:.4g}%\n"
                        message_quant += f"The absolute risk in the new case is: {self.llm_values.get('absolute_risk_new') * 100:.4g}%\n"
                        relative_risk_percent = (self.llm_values.get("relative_risk") - 1) * 100
                        direction = "increase" if relative_risk_percent > 0 else "decrease"
                        message_quant += f"The relative risk {direction} is {abs(relative_risk_percent):.4g}%\n"
                        self.output["eval_case_overall"] = "L1" #################
                    # Beide absoluten Risiken gegeben, aber relatives Risiko berechnet
                    elif self.output["eval_3_abs_base"] == "G" and self.output["eval_3_abs_new"] == "G" and self.output["eval_3_relative"] == "C":
                        message_quant += "The tool calculated the relative risk.\n"
                        message_quant += f"The absolute risk in the base case is: {self.llm_values.get('absolute_risk_base') * 100:.4g}%\n"
                        message_quant += f"The absolute risk in the new case is: {self.llm_values.get('absolute_risk_new') * 100:.4g}%\n"
                        relative_risk_percent = (w["relative_risk"] - 1) * 100
                        direction = "increase" if relative_risk_percent > 0 else "decrease"
                        message_quant += f"The (calculated) relative risk {direction} is {abs(relative_risk_percent):.4g}%\n"
                        self.output["eval_case_overall"] = "L1" #################
                    
                    # Initial NICHT transparent (L2)
                    # Beide absoluten Risiken berechenbar, aber min. eins davon nicht initial gegeben
                    elif self.output["eval_3_abs_base"] in ["G", "C"] and self.output["eval_3_abs_new"] in ["G", "C"]:
                        message_quant += calculated_string
                        if self.output["eval_3_abs_base"] == "G":
                            message_quant += f"The absolute risk in the base case is: {self.llm_values.get('absolute_risk_base') * 100:.4g}%\n"
                        elif self.output["eval_3_abs_base"] == "C":
                            message_quant += f"(Calculated) absolute risk in the base case: {w['absolute_risk_base'] * 100:.4g}%\n"
                        if self.output["eval_3_abs_new"] == "G":
                            message_quant += f"The absolute risk in the base case is: {self.llm_values.get('absolute_risk_new') * 100:.4g}%\n"
                        elif self.output["eval_3_abs_new"] == "C":
                            message_quant += f"(Calculated) absolute risk in the base case: {w['absolute_risk_new'] * 100:.4g}%\n"
                        if self.output["eval_3_relative"] == "G":
                            relative_risk_percent = (self.llm_values.get("relative_risk") - 1) * 100
                            direction = "increase" if relative_risk_percent > 0 else "decrease"
                            message_quant += f"The relative risk {direction} is {abs(relative_risk_percent):.4g}%\n"
                        elif self.output["eval_3_relative"] == "C":
                            relative_risk_percent = (w["relative_risk"] - 1) * 100
                            direction = "increase" if relative_risk_percent > 0 else "decrease"
                            message_quant += f"The relative risk {direction} is {abs(relative_risk_percent):.4g}%\n"
                        self.output["eval_case_overall"] = "L2" #################

                    # Intransparent (L3) -> nur Absolute risk Base berechenbar
                    elif self.output["eval_3_abs_base"] in ["G", "C"] and self.output["eval_3_abs_new"] == "N":
                        if self.output["eval_3_abs_base"] == "G":
                            message_quant += f"The absolute risk in the base case is: {self.llm_values.get('absolute_risk_base') * 100:.4g}%\n"
                            message_quant += "Absolute risk in the new case: MISSING\n"
                        elif self.output["eval_3_abs_base"] == "C":
                            message_quant += "The tool was able to calculate the absolute risk in the base case\n"
                            message_quant += f"(Calculated) absolute risk in the base case: {w['absolute_risk_base'] * 100:.4g}%\n"
                            message_quant += "Absolute risk in the new case: MISSING\n"
                        self.output["eval_case_overall"] = "L3" #################
                    # Intransparent (L3) -> nur Absolute risk New berechenbar
                    elif self.output["eval_3_abs_new"] in ["G", "C"] and self.output["eval_3_abs_base"] == "N":
                        if self.output["eval_3_abs_new"] == "G":
                            message_quant += "Absolute risk in the base case: MISSING\n"
                            message_quant += f"The absolute risk in the new case is: {self.llm_values.get('absolute_risk_new') * 100:.4g}%\n"
                        elif self.output["eval_3_abs_new"] == "C":
                            message_quant += "The tool was able to calculate the absolute risk in the new case\n"
                            message_quant += "Absolute risk in the new case: MISSING\n"
                            message_quant += f"(Calculated) absolute risk in the new case: {w['absolute_risk_new'] * 100:.4g}%\n"
                        self.output["eval_case_overall"] = "L3" #################
                    
                    elif self.output["eval_3_abs_base"] == "N" and self.output["eval_3_abs_new"] == "N":
                        message_quant += "The tool could neither extract nor calculate any absolute risk"
                        if self.output["eval_3_relative"] == "G":
                            message_quant += "However, the tool was able to extract a relative risk."
                            relative_risk_percent = (self.llm_values.get('relative_risk') - 1) * 100
                            direction = "increase" if relative_risk_percent > 0 else "decrease"
                            message_quant += f"The relative risk {direction} is {abs(relative_risk_percent):.4g}%\n"
                            message_quant += "ATTENTION: Solely interpreting the relative risk is misleading!"
                        self.output["eval_case_overall"] = "L4" #################
        self.output["message_quant"] = message_quant

    # 5. BAUM -----------------------------------------------------------------------------
        # Referenzklassenevaluation
        message_reference = ""
        # Reference class description dranhängen -> für alle Fälle außer UR und NR
        if self.output["eval_1"] != "NR" and self.output["eval_1"] != "UR":
            if self.reference_class_description_base is None and self.reference_class_description_new is None:
                message_reference += "\nOur tool could not detect any reference class descriptions in the given text extract.\n"
            elif self.reference_class_description_base is not None and self.reference_class_description_new is not None:
                message_reference += "\nOur tool detected the following reference class descriptions in the given text extract:\n"
                message_reference += f"- Base case: {self.reference_class_description_base}\n"
                message_reference += f"- New case: {self.reference_class_description_new}\n"
            elif self.reference_class_description_base is not None and self.reference_class_description_new is None:
                message_reference += "\nOur tool detected the following reference class descriptions in the given text extract:\n"
                message_reference += f"- Base case: {self.reference_class_description_base}\n"
            elif self.reference_class_description_base is None and self.reference_class_description_new is not None:
                message_reference += "\nOur tool detected the following reference class descriptions in the given text extract:\n"
                message_reference += f"- New case: {self.reference_class_description_new}\n"
        
        self.output["message_reference"] = message_reference

    # 6. BAUM -----------------------------------------------------------------------------
        # Verbale Risikodeskriptoren
        message_verbal_desc = ""
        if self.output["eval_1"] != "UR" and self.output["eval_1"] != "NR":
            descriptors = []

            if self.verbal_descriptor_base:
                descriptors.append(f'"{self.verbal_descriptor_base}"')

            if self.verbal_descriptor_change:
                descriptors.append(f'"{self.verbal_descriptor_change}"')

            if self.verbal_descriptor_new:
                descriptors.append(f'"{self.verbal_descriptor_new}"')

            if descriptors:
                message_verbal_desc += "\nThe tool detected verbal risk descriptor(s). Be careful when interpreting their meaning!\n"
                message_verbal_desc += "Verbal risk descriptor(s): " + ", ".join(descriptors) + "\n"

        self.output["message_verbal"] = message_verbal_desc

    # 7. BAUM -----------------------------------------------------------------------------
        # Quellenevaluation
        message_source = ""

        if self.output["eval_1"] != "NR" and self.output["eval_1"] != "UR":
            if self.output["eval_2"] == "SB" or self.output["eval_2"] == "SN":
                if w["source_base"] is not None:
                    message_source += "A source is provided. Please validate.\n"
                else: 
                    message_source += "ATTENTION: No source is provided!\n"
            else: 
                if w["source_base"] is not None and w["source_new"] is not None:
                    message_source += "Both sources are provided. Please validate.\n"
                elif w["source_base"] is not None:
                    message_source += "ATTENTION: source for the base risk situation is provided, but not for the new risk situation\n"
                elif w["source_new"] is not None:
                    message_source += "ATTENTION: source for the new risk situation is provided, but not for the base risk situation\n"
                else:
                    message_source += "ATTENTION: No sources detected!\n"    

        self.output["message_source"] = message_source 
    
    
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







input = """### Instruction:
From the input text, extract the following fields ONLY.
Format your response as newline-separated entries:

category: value

Do NOT include any additional text, headings, or explanations.

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
- reference_class_description_base
- reference_class_description_new
- reference_class_size_base
- reference_class_size_new
- source_base
- source_new
- topic_and_unit

### Input:
Save the Children estimates that if emissions continue, 80% of the 120 million children born in 2020 could be subjected to unprecedented extreme heat events throughout their lives.

### Output:
risk_communication: 1
unrelated_risks: 0.0
absolute_risk_base: 0.8
absolute_risk_new: null
absolute_number_base: null
absolute_number_new: null
absolute_risk_difference: null
relative_risk: null
absolute_number_difference: null
verbal_descriptor_base: null
verbal_descriptor_new: null
verbal_descriptor_change: null
reference_class_size_base: 120000000
reference_class_size_new: null
reference_class_description_base: could be subjected to unprecedented extreme heat events throughout their lives
reference_class_description_new: null
source_base: Save the Children
source_new: null
topic_and_unit: Amount of children facing unprecedented extreme heat in absolute numbers and % during their lifetime in % and absolute numbers due to climate change in % and absolute numbers due to climate change in % and absolute numbers due to climate change in % and absolute numbers due to climate change in % and absolute numbers due to climate change in"""



risk_data = RiskEvaluator()

def run_pipeline(llm_output: str) -> tuple[str, str, str, str]:
    output = extract_selected_attributes(llm_output)
    risk_data = RiskEvaluator()
    risk_data.load_from_text(output)
    risk_data.evaluate()

    message_quant = str(risk_data.output.get("message_quant") or "")
    message_reference = str(risk_data.output.get("message_reference") or "")
    message_verbal = str(risk_data.output.get("message_verbal") or "")
    eval_case_overall = str(risk_data.output.get("eval_case_overall") or "")

    return message_quant.strip(), message_reference.strip(), message_verbal.strip(), eval_case_overall.strip()


print(run_pipeline(input))








