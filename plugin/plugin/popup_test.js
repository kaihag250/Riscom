function formatTextBold(text, includeNumbers = false) {
  const keywords = [
    "Caution",
    "Attention",
    "Warning",
    
  ];

  // Keywords fett machen
  keywords.forEach(word => {
    const regex = new RegExp(`\\b(${word})\\b`, "gi");
    text = text.replace(regex, "<b>$1</b>");
  });

  // Optional: Zahlen + Prozentzahlen fett
  if (includeNumbers) {
    text = text.replace(/(\d+(\.\d+)?%?)/g, "<b>$1</b>");
  }

  return text;
}


document.getElementById("analyze").addEventListener("click", () => {
  const outputText = document.getElementById("outputText");
  const outputReference = document.getElementById("outputReference");
  const outputVerbal = document.getElementById("outputVerbal");
  const outputQuelle = document.getElementById("outputQuelle");
  const analyzeBtn = document.getElementById("analyzeText");
  const spinner = document.getElementById("spinner");

  analyzeBtn.disabled = true;
 
  // Text holen
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { action: "getSelectedText" }, (response) => {
      const selectedText = response?.text?.trim();

      if (!selectedText) {
        outputText.innerText = "⚠️ No text selected.";
        outputText.style.display = "block";
        analyzeBtn.disabled = false;
        analyzeText.innerText = "Analyze";
        spinner.style.display = "none";
        return;
      }

      if (selectedText.length > 650) {
        outputText.innerText = `⚠️ The selected text exceeds the maximum text length.`;
        outputText.style.display = "block";
        analyzeBtn.disabled = false;
        analyzeText.innerText = "Analyze";
        spinner.style.display = "none";
        return;
      }
      analyzeText.innerText = "Analyze...";
      spinner.style.display = "inline-block";
      // Beispiel-Daten (Platzhalter für echte Analyse)
      const data = {
        message_quant: `Risk communication detected

The tool detected quantitative risk information.
Two risk scenarios detected.

The tool could neither extract nor calculate any absolute risk.
However, the tool was able to extract a relative risk.
The relative risk decrease is 100/100000
ATTENTION: Solely interpreting the relative risk is misleading!`,
       message_source: `Both sources are provided. Please validate.
Source (base case): CDC estimates
Source (new case): CDC estimates`,
        message_reference: `Our tool detected the following reference class descriptions in the given text extract:
- Base case: people who died of overdose in the US in 2023
- New case: people who died of overdose in the US in 2024`,
        message_verbal: ``,
        eval_case: "L3"
      };
      // ⏱️ Künstliche Ladezeit: 2000 Millisekunden (2 Sekunden)
      setTimeout(() => {
       // Vorherige Klassen entfernen
       ["outputText", "outputVerbal", "outputQuelle", "outputReference"].forEach(id => {
         const el = document.getElementById(id);
          el.classList.remove("Transparent", "Initially-Transparent", "Intransparent");
       });
       // Sichtbar machen
       outputText.style.display="block";
       outputReference.style.display = "block";
       outputVerbal.style.display = "block";
       outputQuelle.style.display = "block";
       // Farblogik für Quelle – prüfe Rohtext!
        if (
          data.message_source.trim().includes("Both sources are provided. Please validate.") || 
          data.message_source.trim().includes("A source is provided. Please validate.")
        ) {
         outputQuelle.classList.add("Transparent");
       } else {
         outputQuelle.classList.add("Initially-Transparent");
        }

       // Farblogik für Reference
       if (
         data.message_reference.trim() ===
         "The tool did not identify any reference class description in the selected text."
       ) {
         outputReference.classList.add("Initially-Transparent");
       } else {
         outputReference.classList.add("Transparent");
       }

       // Farblogik für Verbal
       if (data.message_verbal.trim()) {
         outputVerbal.classList.add("Initially-Transparent");
       } else {
         outputVerbal.style.display = "none";
       }

       // Mapping eval_case → CSS-Klasse
       const caseToClass = {
         L1: "Transparent",
         L2: "Initially-Transparent",
         L3: "Intransparent",
         L4: "Intransparent",
         R1_1: "Transparent",
         R2_1: "Initially-Transparent",
         R3_1: "Intransparent",
         NN: "Intransparent",
         UR: "Initially-Transparent"
       };

       const caseClass = caseToClass[data.eval_case];
       if (caseClass) {
         outputText.classList.add(caseClass);
        }

  // Ergebnis einfügen – fettgedruckt formatieren
  outputText.innerHTML = formatTextBold(data.message_quant,true);
  outputReference.innerHTML = formatTextBold(data.message_reference);
  outputVerbal.innerHTML = formatTextBold(data.message_verbal);
  outputQuelle.innerHTML = formatTextBold(data.message_source);

  // Logik für Sonderfälle NR / UR
  if (data.eval_case === "NR" || data.eval_case === "UR") {
    outputText.innerHTML = formatTextBold(data.message_quant);
    outputReference.style.display = "none";
    outputVerbal.style.display = "none";
    outputQuelle.style.display = "none";
  }

  // Spinner & Button zurücksetzen
  analyzeBtn.disabled = false;
  analyzeText.innerText = "Analyze";
  spinner.style.display = "none";
      }, 2000);
    }); // Ende chrome.tabs.sendMessage
  });   // Ende chrome.tabs.query
});     // Ende addEventListener