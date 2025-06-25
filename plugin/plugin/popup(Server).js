document.getElementById("analyze").addEventListener("click", () => {
  const output = document.getElementById("output");

  // Schritt 1: Text vom aktiven Tab holen
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { action: "getSelectedText" }, (response) => {
      const selectedText = response?.text?.trim();

      if (!selectedText) {
        output.innerText = "⚠️ Kein Text markiert.";
        return;
      }

      // Prompt erstellen
      const prompt =`### Instruction:
Extract ONLY the following fields from the input text.
Format the output as newline-separated 'category: value' pairs.
Do NOT include any explanations, comments, or additional text of any kind.

Fields to extract:
- risk_communication
- single_case_base
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
- population_size
- reference_class_description_base
- reference_class_description_new
- reference_class_size_base
- reference_class_size_new
- source_base
- source_new
- topic_and_unit

Sample Text: ${selectedText}`;

      // API-Call
      fetch("https://6uir6d9csfxydu-8000.proxy.runpod.net/analyze", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: prompt })
})
  .then(res => {
    if (!res.ok) throw new Error(`HTTP-Fehler! Status: ${res.status}`);
    return res.json();
  })
  .then(data => {
    // Text anzeigen
    output.innerText = data.response || "Keine Antwort erhalten.";

    // Risiko-Label aus der Antwort (z.B. "gut", "mittel", "schlecht")
    const label = (data.label || "").toLowerCase().trim();

    // Alte Klassen entfernen (für visuellen Status)
    document.body.classList.remove("Transparent", "Initially-Transparent", "Intransparent");
    output.classList.remove("Transparent", "Initially-Transparent", "Intransparent");

    // Neue Klassen hinzufügen, falls Label bekannt
    if (["Transparent", "Initially Transparent", "Intransparent"].includes(label)) {
      document.body.classList.add(`risk-${label}`);
      output.classList.add(`risk-${label}`);
    } else {
      // Optional: Fallback-Klasse oder Entfernen aller Styles
      document.body.classList.remove("Transparent", "Initially-Transparent", "Intransparent");
      output.classList.remove("Transparent", "Initially-Transparent", "Intransparent");
    }
  })
  .catch(err => {
    output.innerText = "❌ Fehler beim Abrufen der API.";
    console.error("API Fehler:", err);
  });
});
});
});
