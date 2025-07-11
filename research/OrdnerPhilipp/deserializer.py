from pathlib import Path
from pydantic_model import Risk  # Dein separates Modell aus risk_processor.py

file_path = "output/3risk_example.json"

# Funktion zum Zugriff auf die risk instance, flexibel abhängig vom file name 
def get_risk_instance(file_path: str) -> Risk:
    json_str = Path(file_path).read_text()
    risk_instance = Risk.model_validate_json(json_str)
    return risk_instance

# Optional: Als Dictionary weiterverwenden -> empfohlen (warum?)
#risk_dict = risk_instance.model_dump()
#print(risk_dict)



# Wichtig: deserializer nur nötig, falls JSON-Brücke explizit gewollt. Ansonsten direkte 
#          Lösung über LLM -> pydantic -> Python-Objekt möglich 
