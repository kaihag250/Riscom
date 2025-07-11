from deserializer import get_risk_instance
from pydantic_model import Risk

# Ausgeschlossene Funktionalitäten bis dato:
# Umformulierung in gute Risikokommunikation via Textgenerierung 
# Reduktion von positive/ negative framing, e.g. 90% survival chance vs. 10% death risk 
# Reduktion von Framing durch Inhalte, e.g. mehr über Nutzen als über Schaden berichtet 

# Nicht abgedeckte Tabellen-Fälle: 
# Mehr als zwei Cases

# Grafische Implementierung? -> siehe Harding Center Infobox

class RiskProcessor:
    # Konstruktor
    def __init__(self, risk_instance: Risk):
        self.risk = risk_instance
        self.extract_variables()

    def extract_variables(self):
        # Grundklassifizierung
        self.risk_com = self.risk.risk_com
        self.one_case = self.risk.one_case

        # Absolute risks
        self.abs_risk_base = self.risk.absolute_risk_base
        self.abs_risk_new = self.risk.absolute_risk_new

        # Absolute numbers
        self.abs_number_base = self.risk.absolute_number_base
        self.abs_number_new = self.risk.absolute_number_new

        # Differences
        self.abs_risk_diff = self.risk.absolute_risk_difference
        self.abs_number_diff = self.risk.absolute_number_difference

        # Relative risk
        self.rel_risk = self.risk.relative_risk

        # Verbal risk descriptors
        self.verbal_desc_base = self.risk.verbal_risk_descriptor_base
        self.verbal_desc_new = self.risk.verbal_risk_descriptor_new
        self.verbal_desc_change = self.risk.verbal_risk_descriptor_change

        # Reference class size
        self.ref_class_size_base = self.risk.reference_class_size_base
        self.ref_class_size_new = self.risk.reference_class_size_new

        # Reference class description
        self.ref_class_desc_base = self.risk.reference_class_description_base
        self.ref_class_desc_new = self.risk.reference_class_description_new

        # Sources
        self.source_base = self.risk.source_base
        self.source_new = self.risk.source_new

        # Topic and unit
        self.topic_unit = self.risk.topic_and_unit

    def process(self):
        print("\n--- Risikoanalyse gestartet ---")
        
        # 1. Grundlegende Klassifizierung
        # 1.1 (-> Ausgabe). Riskokommunikation gegeben: nein -> break & Ausgabe 
        if self.risk_com == 0:
            print("1.1: Keine Risikokommunikation gegeben. Analyse beendet.")
            return # Methode ist fertig abgearbeitet, keine weitere Analyse
        print("1.1: Risikokommunikation erkannt.")

        # 1.2 (-> keine Ausgabe). Unterscheidung zwischen one case und two case -> bereits in Binärvariablen gespeichert
        if self.one_case == 1:
            print("1.2: Nur ein Fall erkannt.")
        else:
            print("1.2: Zwei Fälle erkannt: Vergleich von zwei Risikosituationen.")


        # 2. Berechnung aller fehlenden Größen, soweit möglich
        print("\n--- Schritt 2: Berechnungen ---")

        # 2.1. Absolute Zahlen aus absolute number und absolute number difference
        #    Wenn abs_number_diff und eine der beiden absolute_number-Werte gegeben ist
        if self.one_case == 0:
            if self.abs_number_diff is not None:
                if self.abs_number_base is not None and self.abs_number_new is None:
                    self.abs_number_new = self.abs_number_base - self.abs_number_diff
                    print(f"2.2: Berechnet Absolute Number (New) = {self.abs_number_new}")
                elif self.abs_number_new is not None and self.abs_number_base is None:
                    self.abs_number_base = self.abs_number_new + self.abs_number_diff
                    print(f"2.2: Berechnet Absolute Number (Base) = {self.abs_number_base}")

        # 2.2. Absolutes Risiko aus gegebener absolute number und reference class size -> HIER?: Vergleich einbauen, falls absolutes schon gegeben ist und sich dieses und das berechnete deckt oder nicht?
        if self.abs_number_base is not None and self.ref_class_size_base is not None:
            calculated_base = (self.abs_number_base / self.ref_class_size_base) * 100
            if self.abs_risk_base is None:
                self.abs_risk_base = calculated_base
                print(f"2.1: Berechnet Absolutes Risiko (Base) = {self.abs_risk_base:.2f}%")
        if self.abs_number_new is not None and self.ref_class_size_new is not None:
            calculated_new = (self.abs_number_new / self.ref_class_size_new) * 100
            if self.abs_risk_new is None:
                self.abs_risk_new = calculated_new
                print(f"2.1: Berechnet Absolutes Risiko (New) = {self.abs_risk_new:.2f}%")

        # 2.3. Absolutes Risiko aus abs_risk und rel_risk
        if self.rel_risk is not None:
            if self.abs_risk_base is not None and self.abs_risk_new is None:
                self.abs_risk_new = self.abs_risk_base * self.rel_risk
                print(f"2.2: Aus Relativem Risiko und Absoluten Risiko Base berechnet: Absolutes Risiko (New) = {self.abs_risk_new:.2f}%")
            elif self.abs_risk_new is not None and self.abs_risk_base is None:
                self.abs_risk_base = self.abs_risk_new / self.rel_risk
                print(f"2.2: Aus Relativem Risiko und Absoluten Risiko New berechnet: Absolutes Risiko (Base) = {self.abs_risk_base:.2f}%")
        # 2.4. Relatives Risiko, falls beide absoluten Risiken gegeben sind
        if self.abs_risk_base is not None and self.abs_risk_new is not None:
            calculated_rel = self.abs_risk_new / self.abs_risk_base if self.abs_risk_base != 0 else None
            if self.rel_risk is None and calculated_rel is not None:
                self.rel_risk = calculated_rel # Relatives Risiko erfolgreich berechnet und nun sel.rel_risk aktualisiert
                print(f"2.3: Berechnet Relatives Risiko = {self.rel_risk:.2f}")


        # 3. Bewertung von ja/nein Strings (sources, verbal risk descriptors, reference classes)
        print("\n--- Schritt 3: Qualitative Bewertung ---")
        # 3.1. Prüfung, ob Sources gegeben
        if self.source_base or self.source_new:
            print("3.1: Quellen angegeben – bitte überprüfen Sie diese:")
            if self.source_base:
                print(f"     • Source for base risk: {self.source_base}")
            if self.source_new:
                print(f"     • Source for new risk: {self.source_new}")
        else:
            print("3.1: Achtung: Keine Quellen angegeben.")

        # 3.2. Prüfung, ob verbale Risikodeskriptoren gegeben
        if self.verbal_desc_base or self.verbal_desc_new or self.verbal_desc_change:
            print("3.2: Achtung: Verbale Risikodeskriptoren vorhanden. Bitte überprüfen Sie, ob es eine genaue Definition(en) für folgende Risikodeskriptor(en) gibt:")
            if self.verbal_desc_base:
                print(f"     • verbal_risk_descriptor_base: {self.verbal_desc_base}")
            if self.verbal_desc_new:
                print(f"     • verbal_risk_descriptor_new:   {self.verbal_desc_new}")
            if self.verbal_desc_change:
                print(f"     • verbal_risk_descriptor_change: {self.verbal_desc_change}")
        else:
            print("3.2: Keine verbalen Risikodeskriptoren vorhanden.")

        # 3.3. Prüfung, ob reference class(es) gegeben sind
        if self.ref_class_desc_base or self.ref_class_desc_new:
            print("3.3: Referenzklassenbeschreibung vorhanden.")
        else:
            print("3.3: Achtung: Keine Referenzklasse angegeben – worauf beziehen sich Aussagen?")

        # 4. Bewertung, welche Größen nicht gegeben sind
        print("\n--- Schritt 4: Fehlende Größen prüfen ---")
        # 4.1. Absolute risk(s) berechenbar?
        if self.one_case == 1:
        # Ein-Fall: genügt, dass entweder Base oder New berechenbar ist
            if self.abs_risk_base is not None: #or self.abs_risk_new is not None
                print("4.1: Absolutes Risiko berechenbar.")
            else:
                print("4.1: Kein absolutes Risiko angegeben oder berechenbar – Risikokommunikation intransparent.")
        else:
        # Zwei-Fälle: beide absoluten Risiken prüfen und jeweils unterscheiden
            if self.abs_risk_base is not None and self.abs_risk_new is not None:
                print("4.1: Beide absoluten Risiken berechenbar.")
            elif self.abs_risk_base is None and self.abs_risk_new is not None:
                print("4.1: Fehlendes Basis-Risiko, aber neues Risiko ist gegeben.")
            elif self.abs_risk_base is not None and self.abs_risk_new is None:
                print("4.1: Basis-Risiko ist gegeben, aber neues Risiko fehlt.")
            else:
                print("4.1: Keines der beiden absoluten Risiken ist angegeben oder berechenbar – Risikokommunikation intransparent.")

        # 5. Transparente Risikodarstellung für den Endnutzer
        print("\n--- Schritt 5: Transparente Darstellung ---")
        # 5.1. Umrechnung und Ausgabe der absolute risk(s) in Prozentzahl und x in 100
        if self.abs_risk_base is not None:
            per_100_base = self.abs_risk_base  # schon in Prozent, pro 100 Personen entspricht Prozent
            print(f"5.1: Absolutes Risiko (Base): {self.abs_risk_base:.2f}% ({per_100_base:.2f} in 100)")
        if self.abs_risk_new is not None:
            per_100_new = self.abs_risk_new
            print(f"5.1: Absolutes Risiko (New): {self.abs_risk_new:.2f}% ({per_100_new:.2f} in 100)")
        #5.2. Ausgabe des relativen Risikos, falls vorhanden
        if self.rel_risk is not None:
            # Berechne die Veränderung in Prozent
            change_pct = abs((self.rel_risk - 1) * 100)

            if self.rel_risk < 1:
                print(f"5.2: The risk in the new case is {change_pct:.2f}% smaller than in the base case.")
            elif self.rel_risk > 1:
                print(f"5.2: The risk in the new case is {change_pct:.2f}% larger than in the base case.")
            else:
                print("5.2: The risk in the new case is the same as in the base case.")

        # Hinweis: Grafische Darstellung kann hier ergänzt werden (Matplotlib o.ä.).


# Hauptprogramm
if __name__ == "__main__":
    # Dies noch automatisieren -> für jede Inferenz wird Output-Datei erstellt, worauf die python-logik automatisch Zugriff hat
    file_path = "output/4risk_example.json"
    risk_instance = get_risk_instance(file_path)

    processor = RiskProcessor(risk_instance)
    processor.process()






# 2 (-> keine Ausgabe) & als loop mit n = 2 ?. Berechnung aller fehlenden Größen, soweit möglich 
# 2.1. Berechnung des absoluten Risikos aus gegebener absoluten number und reference class size
# 2.2. Berechnung absoluter Zahlen aus absolute number (base case bzw. new case) und absolute number difference 
# 2.2. Berechnung des absoluten Risikos (base case bzw. new case) aus absoluten Risiko (new case bzw. base case) und relativem Risiko 
# 2.3. Berechnung des relativen Risikos, falls beide absoluten Risiken gegeben sind (bzw. beide indirekt berechenbar sind)


# 3 (-> Ausgabe). Bewertung von ja/ nein Strings (sources, verbal risk descriptors, reference classes) -> für one und two case Fall 
# 3.1. Prüfung, ob Sources gegeben: ja -> Meldung zur Überprüfung, nein -> Meldung Achtung 
# 3.2. Prüfung, ob verbale Risikodeskriptoren gegegeben: ja -> Meldung Achtung, schauen ob genauer gegeben
# 3.3. Prüfung, ob reference class(es) gegeben sind: nein -> Meldung Achtung, worauf beziehen sich Aussagen 


# 4 (-> Ausgabe). Bewertung, welche Größen nicht gegeben sind 
# 4.1. Absolute risk(s) berechenbar?: nein -> Meldung, Risikokommunikation intransparent 

# 5 (-> Ausgabe). Transparente Risikodarstellung für den Endnutzer 
# 5.1. Umrechnung und Ausgabe der absolute risk(s) in (a) Prozentzahl und (b) x in 100 -> Reduzierung von ratio bias # Hier grafische Darstellung möglich
# 5.2. Ausgabe des relativen Risikos 
