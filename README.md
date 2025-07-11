# Riscom — Risk Communication Extractor

**Riscom** ist ein praxisorientiertes Forschungsprojekt, das ein feinjustiertes Large Language Model (LLM) mit einer Logik- und Plugin-Pipeline kombiniert, um Risikokommunikation aus Texten automatisch zu erkennen, zu quantifizieren und verständlich darzustellen.

##  Kernkomponenten
- **LLM + Adapter:** Eigenständig trainierte Adapter für Mistral 7B, quantisiert auf Q8, optimiert für BWCloud.
- **Server:** FastAPI-Server mit automatisierter Logik-Pipeline (`logik.py`), um LLM-Ausgaben in nutzbare Entscheidungshilfen zu übersetzen.
- **Browser-Plugin:** Chrome-Plugin, das markierte Texte über eine REST-Schnittstelle an den Server sendet und die Ergebnisse direkt in der UI darstellt.
- **Build-Tools:** Automatisierter Build-Workflow mit CMake für Merging, Konvertierung und Quantisierung.
- **Testdatensätze:** Laufend erweiterter und synthetisch angereicherter Datensatz für bessere Modell-Performance.

## Fortschritt (Stand W12)
- Erfolgreicher Umzug von RunPod auf BWCloud mit stabiler Runtime.
- Einführung von Q8-Quantisierung für performante Inferenz bei hoher Genauigkeit.
- Vollständig funktionierende Logik, die Extraktionsergebnisse validiert, berechnet und in verständliche Nachrichten übersetzt.
- Durchgängige Test-Pipeline vom Input über das Modell bis zur finalen Ausgabe im Plugin.
- Kontinuierliche Optimierung von Modell, Logik und Plugin für Produktivbetrieb.

## Struktur
- `server/` – FastAPI-Server mit LLM-Inferenz und Logik.
- `plugin/` – Chrome-Plugin (Manifest, Popup, Content Script).
- `research/` – Fine-Tuning-Notebooks, Adapter und Testdatensätze.
- `logbook/` – Wöchentliche Fortschrittsdokumentation (PDFs W1–W12).

---
