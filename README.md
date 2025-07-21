# Riscom — Risk Communication Extractor

**Riscom** ist ein praxisorientiertes Forschungsprojekt, das ein feinjustiertes **Large Language Model (LLM)** mit einer **Logik- und Plugin-Pipeline** kombiniert, um Risikokommunikation aus Texten **automatisch zu erkennen, zu quantifizieren und verständlich darzustellen**.

---

## **Kernkomponenten**

### **LLM & Adapter**
- Eigenständig trainierte **Adapter für das Mistral 7B Basismodell**, spezialisiert auf Risikokommunikation.
- **Quantisierte Variante (Q8)** für effizienten Betrieb auf CPU-Infrastrukturen (z.B. **BWCloud**).
- Enthält **Jupyter Notebooks** für Fine-Tuning-Prozesse auf Basis unserer **2000 Datensätze**.
- Tools zur **synthetischen Erzeugung zusätzlicher Trainingsdaten**.
- **Evaluations-Tools** zur Messung der Qualität und Effektivität des trainierten Modells.

### **Server**
- **FastAPI-basierter Inferenzserver** zur Bereitstellung des LLM und der nachgeschalteten Logik-Pipeline.
- **Unterscheidung zwischen GPU-Infrastruktur (RunPod) und CPU-Infrastruktur (BWCloud)** mit entsprechenden Deployment-Anleitungen und Dateien.
- **Automatisierte Logik-Komponente (`logik.py`)**, die Ergebnisse des LLMs in **klare, nutzbare Entscheidungshilfen** für die Risikodarstellung im Plugin transformiert.

### **Browser-Plugin**
- Einfach zu importierendes **Chrome-Plugin** zur direkten Interaktion mit dem Server.
- Ermöglicht das **Markieren von Texten im Webbrowser**, die an den Inferenzserver gesendet und unmittelbar ausgewertet werden.
- **Darstellung der ausgewerteten Ergebnisse** direkt in der Benutzeroberfläche des Browsers zur optimalen Nutzerfreundlichkeit.

### **Build-Tools**
- **Automatisierter Workflow mittels CMake** für:
  - **Merging der Adapter** mit dem Mistral-Basismodell.
  - **Konvertierung und Quantisierung (Q8)** des Modells.

### **Research**
- **Experimente und Analysen** zum Fine-Tuning sowie zu logischen Komponenten, um die Verbindung zwischen Modell-Output und Plugin-Darstellung weiter zu verbessern.
- Entwicklung der **Logik zur automatischen Generierung von Hinweisen** aus den Daten des LLM für klare Risikokommunikation.

---

## **Struktur**

- LLM/ – Adapter für Mistral, Notebooks für Fine-Tuning, Tools zur Evaluierung und Datengenerierung.
- server/ – FastAPI-Server mit LLM-Inferenz und Logik.
- plugin/ – Chrome-Plugin (Manifest, Popup, Content Script).
- research/ – Fine-Tuning-Notebooks, Adapter und Testdatensätze.
- logbook/ – Wöchentliche Fortschrittsdokumentation (PDFs W1–W12).

---