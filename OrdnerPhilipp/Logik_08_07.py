# Version 04_07
# NOCH UMZUSETZEN:
# Verbesserung der Sätze -> sollen weniger technisch wirken, bei Nico nochmal anschauen

# Änderungen im Vergleich zu 02_07: 
# Rausstreichen von topic_and_unit
# Absolute risk difference --> ausgegeben, wenn beide absolute risks berechenbar oder keins 

# Änderungen im Vergleich zu 01_07:
# UMGESETZT:
# Single_Case_New rausgestrichen und immer Warnung bei einem Case -> 2. Baum anpassen
# Neues Handling der reference class descriptions -> PRÜFEN !!!
# Relative risk wird zusätzlich zu relative risk increase/ decrease ausgegeben
# Berechnungslogik erweitern: wenn absolute risk difference und relative risk -> berechenbar
# Berechnungslogik läuft als n=2 Loop

class RiskEvaluator:
    def __init__(self):
        # Originale LLM-Werte
        self.risk_communication = None
        self.unrelated_risks = None
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

        # LLM-Werte als Dictionary speichern
        # -> Evtl. die Werte direkt ins Dicitionary packen anstatt Klassenvariablen
        self.llm_values = {
            "risk_communication": self.risk_communication,
            "unrelated_risks": self.unrelated_risks,
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
            "source_new": self.source_new
        }

        # Arbeitskopie
        self.working_values = self.llm_values.copy()

        # Ergebnis-Output
        self.output = {
            "eval_1": None,
            "eval_2": None,
            "eval_3_abs_base": None, 
            "eval_3_abs_new": None, 
            "eval_3_abs_diff": None,
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
            "unrelated_risks": self.unrelated_risks,
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
            "source_new": self.source_new
        }

        self.working_values = self.llm_values.copy()


    # Vergleicht, was berechnet wurde und was nicht 
    def was_berechnet(self, varname):
        return (
            self.llm_values.get(varname) is None
            and self.working_values.get(varname) is not None
        )
    
    @staticmethod
    def format_risk(value: float) -> str:
        if value is None:
            return "null"
        if value * 100 < 1:
            # Kleiner als 1% → als x/100000
            per_100k = value * 100000
            return f"{per_100k:.0f} in 100.000 or {value * 100:.2f}%"
        else:
            # Ab 1% → mit zwei Nachkommastellen
            return f"{value * 100:.2f}%"

    # Case Zuordnung und Berechnungen 
    def evaluate(self):
        w = self.working_values  # Alias für bessere Lesbarkeit

    # 1. BAUM -----------------------------------------------------------------------------
        # 1. Check: Risiko-Kommunikation vorhanden?
        if not w["risk_communication"]:
            self.output["eval_1"] = "NR"
        
        # 2. Check: Unrelated risks im selektierten Textausschnitt?
        elif w["unrelated_risks"]:
            self.output["eval_1"] = "UR"
        
        # 3. Keine Zahleninformationen vorhanden?
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
                "absolute_risk_new", "absolute_number_new", "reference_class_size_new", "verbal_descriptor_new"]):
                self.output["eval_2"] = "SB"
            else: 
                self.output["eval_2"] = "S2"
    
    # 3. BAUM -----------------------------------------------------------------------------
        # Berechnungslogik, falls Case != NR, UR, NN
        if self.output["eval_1"] != "NR" and self.output["eval_1"] != "UR" and self.output["eval_1"] != "NN":
            for _ in range(2):
                # Absolute Zahlen ergänzen, wenn Differenz bekannt
                if w["absolute_number_difference"] is not None:
                    if w["absolute_number_base"] is not None and w["absolute_number_new"] is None:
                        w["absolute_number_new"] = w["absolute_number_base"] + w["absolute_number_difference"]
                    elif w["absolute_number_new"] is not None and w["absolute_number_base"] is None:
                        w["absolute_number_base"] = w["absolute_number_new"] - w["absolute_number_difference"]

                # Absolute Risiken berechnen aus Zahlen + Referenzgrößen -> aber nicht gegebenes absolutes Risiko überschreiben
                if w["absolute_number_base"] is not None and w["reference_class_size_base"] is not None and w["reference_class_size_base"] != 0 and w["absolute_risk_base"] is None:
                    w["absolute_risk_base"] = w["absolute_number_base"] / w["reference_class_size_base"]
                if w["absolute_number_new"] is not None and w["reference_class_size_new"] is not None and w["reference_class_size_new"] != 0 and w["absolute_risk_new"] is None:
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

                # Absolute Risiken berechnen aus absolute_risk_difference und relative_risk
                if w["absolute_risk_difference"] is not None and w["relative_risk"] is not None:
                    if w["relative_risk"] != 1:
                        w["absolute_risk_base"] = w["absolute_risk_difference"] / (w["relative_risk"] - 1)

                # Absolute Risikodifferenzberechnen
                if w["absolute_risk_base"] is not None and w["absolute_risk_new"] is not None:
                        w["absolute_risk_difference"] = w["absolute_risk_new"] - w["absolute_risk_base"] # Konsistenz überprüfen !!!
            

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
            # Absolute_risk_difference
            if self.llm_values.get("absolute_risk_difference") is not None:
                self.output["eval_3_abs_diff"] = "G"
            elif self.was_berechnet("absolute_risk_difference"):
                self.output["eval_3_abs_diff"] = "C"
            else:
                self.output["eval_3_abs_diff"] = "N"
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
            message_quant += "The selected text does not contain any detectable risk communication.\n"
            self.output["eval_case_overall"] = "NR"
        # eval_1 != NR -> Risk communication detected
        else: 
            message_quant += "Risk communication has been detected in the selected text passage.\n\n"

        # eval_1 == UR -> unrelated risks
        if self.output["eval_1"] == "UR":
            message_quant += (
                "However, there are two or more unrelated risks in the selected text passage.\n"
                "Please select a different text passage.\n"
                "For more information about unrelated risks, refer to the user manual.\n" # Hier tool tip einbauen!!!
            )
            self.output["eval_case_overall"] = "UR" ##########################

        # Unrelated risk und No risk muss von allem zukünftigen ausgeschlossen werden
        if self.output["eval_1"] != "UR" and self.output["eval_1"] != "NR":
            # eval_1 == NN -> Quantitative information?
            if self.output["eval_1"] == "NN":
                message_quant += "Warning: The selected text lacks numerical risk information, which prevents transparent risk assessment\n\n"
                self.output["eval_case_overall"] = "NN" ##############################
            else:
                message_quant += "The tool identified numerical risk information.\n\n"
            
            # eval_2 Add-on zur Nachricht -> Single Case Base, New or Two Cases?
            if self.output["eval_2"] == "S2":
                message_quant += "The tool detected two distinct risk situations being described.\n"
                message_quant += "For clarity, they will be referred to as the base case and the new case.\n\n"
            elif self.output["eval_2"] == "SB":
                message_quant += "The text describes a single base risk scenario.\n"
                message_quant += "Caution: The text may not provide a comparison to an overall or baseline risk.\n"
                message_quant += "See the user manual to understand why this may be insufficient for interpretation.\n\n"

            # Ausgabe der quantitativen Zahlen -> eval_1 != NN 
            if self.output["eval_1"] == "NG":
                # SINGLE CASE
                # Angabe für eval_2 == SB
                if self.output["eval_2"] == "SB":
                    if self.output["eval_3_abs_base"] == "G":
                        message_quant += f"The absolute risk is: {self.format_risk(self.llm_values.get('absolute_risk_base'))}\n"
                        self.output["eval_case_overall"] = "R1.1" #################
                    elif self.output["eval_3_abs_base"] == "C":
                        message_quant += "The tool calculated the absolute risk with the extracted information.\n"
                        message_quant += f"The calculated absolute risk for the given reference group is: {self.format_risk(w['absolute_risk_base'])}\n"
                        self.output["eval_case_overall"] = "R2.1" #################
                    elif self.output["eval_3_abs_base"] == "N":
                        message_quant += "Attention: The absolute risk was neither given nor calculable.\n"
                        self.output["eval_case_overall"] = "R3.1" #################

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
                    if self.was_berechnet("absolute_risk_difference"):
                        calculated.append("absolute risk difference")
                    if calculated:
                        calculated_string += "The tool calculated the following values: " + ", ".join(calculated) + ".\n"

                    # Initial Transparent (L1)
                    # Beide absoluten Risiken und relatives Risiko gegeben
                    if self.output["eval_3_abs_base"] == "G" and self.output["eval_3_abs_new"] == "G" and self.output["eval_3_relative"] == "G":
                        message_quant += f"The absolute risk in the base case is: {self.format_risk(self.llm_values.get('absolute_risk_base'))}\n"
                        message_quant += f"The absolute risk in the new case is: {self.format_risk(self.llm_values.get('absolute_risk_new'))}\n"
                        if self.output["eval_3_abs_diff"] == "G":
                            message_quant += f"The absolute risk difference is: {self.format_risk(self.llm_values.get('absolute_risk_difference'))}\n"
                        elif self.output["eval_3_abs_diff"] == "C":
                            message_quant += f"The (calculated) absolute risk difference is: {self.format_risk(w['absolute_risk_difference'])}\n"
                        message_quant += f"The relative risk is: {self.llm_values.get('relative_risk'):.4g}\n"
                        relative_risk_percent = (self.llm_values.get("relative_risk") - 1) * 100
                        direction = "increase" if relative_risk_percent > 0 else "decrease"
                        message_quant += f"The relative risk {direction} is {abs(relative_risk_percent):.2f}%\n"
                        self.output["eval_case_overall"] = "L1" #################
                    # Beide absoluten Risiken gegeben, aber relatives Risiko berechnet
                    elif self.output["eval_3_abs_base"] == "G" and self.output["eval_3_abs_new"] == "G" and self.output["eval_3_relative"] == "C":
                        message_quant += f"The absolute risk in the base case is: {self.format_risk(self.llm_values.get('absolute_risk_base'))}\n"
                        message_quant += f"The absolute risk in the new case is: {self.format_risk(self.llm_values.get('absolute_risk_new'))}\n"
                        if self.output["eval_3_abs_diff"] == "G":
                            message_quant += f"The absolute risk difference is: {self.format_risk(self.llm_values.get('absolute_risk_difference'))}\n"
                        elif self.output["eval_3_abs_diff"] == "C":
                            message_quant += f"The (calculated) absolute risk difference is: {self.format_risk(w['absolute_risk_difference'])}\n"
                        message_quant += f"The (calculated) relative risk is: {w['relative_risk']:.4g}\n"
                        relative_risk_percent = (w["relative_risk"] - 1) * 100
                        direction = "increase" if relative_risk_percent > 0 else "decrease"
                        message_quant += f"The (calculated) relative risk {direction} is {abs(relative_risk_percent):.2f}%\n"
                        self.output["eval_case_overall"] = "L1" #################
                    
                    # Initial NICHT transparent (L2)
                    # Beide absoluten Risiken berechenbar, aber min. eins davon nicht initial gegeben
                    elif self.output["eval_3_abs_base"] in ["G", "C"] and self.output["eval_3_abs_new"] in ["G", "C"]:
                        message_quant += calculated_string
                        if self.output["eval_3_abs_base"] == "G":
                            message_quant += f"The absolute risk in the base case is: {self.format_risk(self.llm_values.get('absolute_risk_base'))}\n"
                        elif self.output["eval_3_abs_base"] == "C":
                            message_quant += f"The (calculated) absolute risk in the base case is: {self.format_risk(w['absolute_risk_base'])}\n"
                        if self.output["eval_3_abs_new"] == "G":
                            message_quant += f"The absolute risk in the new case is: {self.format_risk(self.llm_values.get('absolute_risk_new'))}\n"
                        elif self.output["eval_3_abs_new"] == "C":
                            message_quant += f"The (calculated) absolute risk in the new case is: {self.format_risk(w['absolute_risk_new'])}\n"
                        if self.output["eval_3_abs_diff"] == "G":
                            message_quant += f"The absolute risk difference is: {self.format_risk(self.llm_values.get('absolute_risk_difference'))}\n"
                        elif self.output["eval_3_abs_diff"] == "C":
                            message_quant += f"The (calculated) absolute risk difference is: {self.format_risk(w['absolute_risk_difference'])}\n"
                        if self.output["eval_3_relative"] == "G":
                            message_quant += f"The relative risk is: {self.llm_values.get('relative_risk'):.4g}\n"
                            relative_risk_percent = (self.llm_values.get("relative_risk") - 1) * 100
                            direction = "increase" if relative_risk_percent > 0 else "decrease"
                            message_quant += f"The relative risk {direction} is {abs(relative_risk_percent):.2f}%\n"
                        elif self.output["eval_3_relative"] == "C":
                            message_quant += f"The (calculated) relative risk is: {w['relative_risk']:.4g}\n"
                            relative_risk_percent = (w["relative_risk"] - 1) * 100
                            direction = "increase" if relative_risk_percent > 0 else "decrease"
                            message_quant += f"The (calculated) relative risk {direction} is {abs(relative_risk_percent):.2f}%\n"
                        self.output["eval_case_overall"] = "L2" #################

                    # Intransparent (L3) -> nur Absolute risk Base berechenbar
                    elif self.output["eval_3_abs_base"] in ["G", "C"] and self.output["eval_3_abs_new"] == "N":
                        if self.output["eval_3_abs_base"] == "G":
                            message_quant += f"The absolute risk in the base case is: {self.format_risk(self.llm_values.get('absolute_risk_base'))}\n"
                            message_quant += "Absolute risk in the new case: MISSING\n"
                        elif self.output["eval_3_abs_base"] == "C":
                            message_quant += "The tool was able to calculate the absolute risk in the base case.\n"
                            message_quant += f"The (calculated) absolute risk in the base case is: {self.format_risk(w['absolute_risk_base'])}\n"
                            message_quant += "Absolute risk in the new case: MISSING\n"
                        self.output["eval_case_overall"] = "L3" #################
                    # Intransparent (L3) -> nur Absolute risk New berechenbar
                    elif self.output["eval_3_abs_new"] in ["G", "C"] and self.output["eval_3_abs_base"] == "N":
                        if self.output["eval_3_abs_new"] == "G":
                            message_quant += "Absolute risk in the base case: MISSING\n"
                            message_quant += f"The absolute risk in the new case is: {self.format_risk(self.llm_values.get('absolute_risk_new'))}\n"
                        elif self.output["eval_3_abs_new"] == "C":
                            message_quant += "The tool was able to calculate the absolute risk in the new case.\n"
                            message_quant += "Absolute risk in the base case: MISSING\n"
                            message_quant += f"The (calculated) absolute risk in the new case is: {self.format_risk(w['absolute_risk_new'])}\n"
                        self.output["eval_case_overall"] = "L3" #################
                    # Intransparent (L4) -> kein absolute risk berechenbar!
                    elif self.output["eval_3_abs_base"] == "N" and self.output["eval_3_abs_new"] == "N":
                        message_quant += "The tool could neither extract nor calculate any absolute risk.\n"
                        if self.output["eval_3_relative"] == "G":
                            message_quant += "However, the tool was able to extract a relative risk.\n"
                            message_quant += f"The relative risk is: {self.llm_values.get('relative_risk'):.4f}\n"
                            relative_risk_percent = (self.llm_values.get('relative_risk') - 1) * 100
                            direction = "increase" if relative_risk_percent > 0 else "decrease"
                            message_quant += f"The relative risk {direction} is {abs(relative_risk_percent):.2f}%\n"
                            message_quant += "Attention: Solely interpreting the relative risk can be misleading!"
                        if self.llm_values.get("absolute_risk_difference") is not None:
                            message_quant += "However, the tool was able to extract an absolute risk difference.\n"
                            message_quant += f"The absolute risk difference is: {self.llm_values.get('absolute_risk_difference')*100:.2f}%\n"
                            message_quant += "Attention: Solely interpreting the absolute risk difference can be misleading!"
                        self.output["eval_case_overall"] = "L4" #################
        self.output["message_quant"] = message_quant

    # 5. BAUM -----------------------------------------------------------------------------
        # Referenzklassenevaluation --> Hier evtl. Einschränkung für SB und SN einführen !!!
        message_reference = ""
        # Reference class description dranhängen -> für alle Fälle außer UR und NR
        if self.output["eval_1"] != "NR" and self.output["eval_1"] != "UR":
            if self.reference_class_description_base is None and self.reference_class_description_new is None:
                message_reference += "\nThe tool did not identify any reference class description in the selected text.\n"
            elif self.reference_class_description_base is not None and self.reference_class_description_new is not None:
                message_reference += "\nThe tool detected the following reference class descriptions in the selected text:\n"
                message_reference += f"- Base case: {self.reference_class_description_base}\n"
                if self.output["eval_1"] != "SB":
                    message_reference += f"- New case: {self.reference_class_description_new}\n"
            elif self.reference_class_description_base is not None and self.reference_class_description_new is None:
                message_reference += "\nThe tool detected the following reference class descriptions in the selected text:\n"
                message_reference += f"- Base case: {self.reference_class_description_base}\n"
            elif self.reference_class_description_base is None and self.reference_class_description_new is not None:
                if self.output["eval_1"] == "SB":
                    message_reference += "\nThe tool did not identify any reference class description in the selected text.\n"
                else:
                    message_reference += "\nThe tool detected the following reference class descriptions in the selected text:\n"
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
                message_verbal_desc += "\nThe tool detected one or more verbal risk descriptors. Please interpret them with caution!\n"
                message_verbal_desc += "Detected descriptor(s): " + ", ".join(descriptors) + "\n"

        self.output["message_verbal"] = message_verbal_desc

    # 7. BAUM -----------------------------------------------------------------------------
        # Quellenevaluation
        message_source = ""

        if self.output["eval_1"] != "NR" and self.output["eval_1"] != "UR":
            if self.output["eval_2"] == "SB":
                if w["source_base"] is not None:
                    message_source += "A source is provided. Please review its credibility.\n"
                    message_source += f"Found source: {w['source_base']}\n"
                else: 
                    message_source += "Caution: No source was found in the selected text.\n"
                    message_source += "Please check whether the original text cites a credible reference.\n"
            else: 
                if w["source_base"] is not None and w["source_new"] is not None:
                    message_source += "Sources for both the base and new case were identified. Please review their credibility.\n"
                    message_source += f"Source for the base case: {w['source_base']}\n"
                    message_source += f"Source for the new case: {w['source_new']}\n"
                elif w["source_base"] is not None:
                    message_source += "Caution: A source is provided for the base case, but missing for the new case!\n"
                    message_source += f"Source for the base case: {w['source_base']}\n"
                elif w["source_new"] is not None:
                    message_source += "Caution: A source is provided for the new case, but missing for the base case!\n"
                    message_source += f"Source for the new case: {w['source_new']}\n"
                else:
                    message_source += "Caution: No sources were found in the selected text.\n" 
                    message_source += "Please check whether the original text cites a credible reference.\n"

        self.output["message_source"] = message_source 
    
### Diese Methode anpassen an LLM-Output    
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
            "source_new"
        ]

        in_output_section = False
        result = {key: None for key in target_keys}

        for line in llm_output.splitlines():
            line = line.strip()

            # Hier anpassen
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


def run_pipeline(input:str): 
    risk_data = RiskEvaluator()
    output = extract_selected_attributes(input)
    risk_data.load_from_text(output)
    risk_data.evaluate()
    print(risk_data.working_values)
    return {
        "message_quant": risk_data.output.get("message_quant"),
        "message_reference": risk_data.output.get("message_reference"),
        "message_verbal": risk_data.output.get("message_verbal"),
        "message_source": risk_data.output.get("message_source"),
        "eval_case_overall": risk_data.output.get("eval_case_overall"),
    }




# Zum Testen
# text = """### Instruction:
# From the input text, extract the following fields ONLY.
# Format your response as newline-separated entries:

# category: value

# Do NOT include any additional text, headings, or explanations.

# Fields to extract:
# - risk_communication
# - unrelated_risks
# - absolute_risk_base
# - absolute_risk_new
# - absolute_number_base
# - absolute_number_new
# - absolute_risk_difference
# - relative_risk
# - absolute_number_difference
# - verbal_descriptor_base
# - verbal_descriptor_new
# - verbal_descriptor_change
# - reference_class_description_base
# - reference_class_description_new
# - reference_class_size_base
# - reference_class_size_new
# - source_base
# - source_new

# ### Input:
# Save the Children estimates that if emissions continue, 80% of the 120 million children born in 2020 could be subjected to unprecedented extreme heat events throughout their lives.

# ### Output:
# risk_communication: 1
# unrelated_risks: 0
# absolute_risk_base: 0.001
# absolute_risk_new: null
# absolute_number_base: null
# absolute_number_new: null
# absolute_risk_difference: null
# relative_risk: 2
# absolute_number_difference: 200
# verbal_descriptor_base: low risk
# verbal_descriptor_new: null
# verbal_descriptor_change: significantly increases
# reference_class_size_base: null
# reference_class_size_new: 1000
# reference_class_description_base: people globally
# reference_class_description_new: null
# source_base: WHO
# source_new: null
# """
# result = run_pipeline(text)
# print(result["message_quant"])
# print(result["message_reference"])
# print(result["message_verbal"])
# print(result["message_source"])
# print(result["eval_case_overall"])







