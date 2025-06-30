document.getElementById("analyze").addEventListener("click", () => {
 const outputText = document.getElementById("output-text");
 const outputVerbal = document.getElementById("output-verbal");
 const outputQuelle = document.getElementById("output-source");
 const analyzeBtn = document.getElementById("analyze");

  // Schritt 1: Text vom aktiven Tab holen
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { action: "getSelectedText" }, (response) => {
      const selectedText = response?.text?.trim();

      if (!selectedText) {
        output.innerText = "⚠️ Kein Text markiert.";
        return;
      }
      if (selectedText.length > 300) {
        output.innerText = `⚠️ Der markierte Text überschreitet die maximale Zeichenanzahl`;
        return;
      }
      // ✅ Fake-Serverantwort zum Testen (nur "Transparent")
      const data = {
        response: "☑️ Die Risikokommunikation ist transparent.",
        label: "Initially Transparent", // → du kannst hier auch "initially transparent" oder "intransparent" testen
        source:"",
        verbal:""
      };

      // Text anzeigen
      outputText.innerText = data.response;
      outputVerbal.innerText = data.verbal;
      outputQuelle.innerText = data.source;

      // Risiko-Label normalisieren
      const label = (data.label || "").trim();

      // Alte Klassen entfernen
      document.body.classList.remove("Transparent", "Initially-Transparent", "Intransparent");
      output.classList.remove("Transparent", "Initially-Transparent", "Intransparent");
      analyzeBtn.classList.remove("Transparent", "Initially-Transparent", "Intransparent");

      // Neue Klasse setzen
      if (["Transparent", "Initially Transparent", "Intransparent"].includes(label)) {
        const className = label.replace(/ /g, "-");
        document.body.classList.add(className);
        output.classList.add(className);
        analyzeBtn.classList.add(className);
      }
    });
  });
});