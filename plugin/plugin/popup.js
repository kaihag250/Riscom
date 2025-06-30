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
        outputText.innerText = "⚠️ Kein Text markiert.";
        outputText.style.display = "block";
        analyzeBtn.disabled = false;
        analyzeText.innerText = "Analysieren";
        spinner.style.display = "none";
        return;
      }

      if (selectedText.length > 650) {
        outputText.innerText = `⚠️ Der markierte Text überschreitet die maximale Zeichenanzahl.`;
        outputText.style.display = "block";
        analyzeBtn.disabled = false;
        analyzeText.innerText = "Analysieren";
        spinner.style.display = "none";
        return;
      }
      analyzeText.innerText = "Analysiere...";
      spinner.style.display = "inline-block";
      // Beispiel-Daten (Platzhalter für echte Analyse)
      const data = {
        message_quant: `Risk communication detected
The tool detected quantitative risk information.
Two risk scenarios for different treatment groups detected.
The tool calculated the relative risk.
The absolute risk in the base case is: 20.0%
The absolute risk in the new case is: 30.0%
The (calculated) relative risk increase is 50.0%`,
        message_reference: "test",
        message_source: `ATTENTION: source for the base risk situation is provided, but not for the new risk situation`,
        message_verbal: "test",
        eval_case: "L1_1"
      };
      // ⏱️ Künstliche Ladezeit: 2000 Millisekunden (2 Sekunden)
      setTimeout(() => {
      // HIER beginnt dein bisheriger Code mit Einfügen & Sichtbarkeit
 
      // Vorherige Klassen entfernen
      ["outputText", "outputVerbal", "outputQuelle", "outputReference"].forEach(id => {
        const el = document.getElementById(id);
        el.classList.remove("Transparent", "Initially-Transparent", "Intransparent");
      });

      // Ergebnis einfügen
      outputText.innerText = data.message_quant;
      outputReference.innerText = data.message_reference;
      outputVerbal.innerText = data.message_verbal;
      outputQuelle.innerText = data.message_source;

      // Sichtbar machen
      outputText.style.display = "block";
      outputReference.style.display = "block";
      outputVerbal.style.display = "block";
      outputQuelle.style.display = "block";

      // Logik für Sonderfälle NR / UR
      if (data.eval_case === "NR") {
        outputText.innerText = "No Risk Communication detected";
        outputReference.style.display = "none";
        outputVerbal.style.display = "none";
        outputQuelle.style.display = "none";
      }

      if (data.eval_case === "UR") {
        outputText.innerText = "Unrelated risks within the selected text. Please reselect different passage.";
        outputReference.style.display = "none";
        outputVerbal.style.display = "none";
        outputQuelle.style.display = "none";
      }
      // Farblogik für Quelle
      if (
        data.message_source.trim() === "Both sources are provided. Please validate." ||
        data.message_source.trim() === "A source is provided. Please validate."
      ) {
        outputQuelle.classList.add("Transparent");
      } else {
        outputQuelle.classList.add("Initially-Transparent");
      }

      // Farblogik für Reference
      if (
        data.message_reference.trim() ===
        "Our tool could not detect any reference class descriptions in the given text extract."
      ) {
        outputReference.classList.add("Intransparent");
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
        L1_1: "Transparent",
        L1_2: "Transparent",
        L2: "Initially-Transparent",
        L3: "Intransparent",
        L4: "Intransparent",
        R1_1: "Intransparent", // Achtung: war doppelt!
        R2_1: "Initially-Transparent",
        R3_1: "Intransparent",
        R4_1: "Intransparent",
        R2_2: "Intransparent",
        R3_2: "Intransparent",
        R4_2: "Intransparent",
        NN2: "Intransparent",
        NNB: "Intransparent",
        NNN: "Intransparent"
      };

      const caseClass = caseToClass[data.eval_case];
      if (caseClass) {
        outputText.classList.add(caseClass);
      }

      // Spinner & Button zurücksetzen
      analyzeBtn.disabled = false;
      analyzeText.innerText = "Analysieren";
      spinner.style.display = "none";
      }, 2000);
    }); // Ende chrome.tabs.sendMessage
  });   // Ende chrome.tabs.query
});     // Ende addEventListener