const SERVER_URL = "http://193.196.39.15:8000/extract-advice";

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

      // Spinner und Status anzeigen
      analyzeText.innerText = "Analysiere...";
      spinner.style.display = "inline-block";

      // ── Server-Request ───────────────────────────────────────────────
      fetch(SERVER_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: selectedText })
      })
        .then((res) => {
          if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
          return res.json();
        })
        .then((data) => {
          // Vorherige Klassen & Sichtbarkeit zurücksetzen
          [outputText, outputReference, outputVerbal, outputQuelle].forEach((el) => {
            el.classList.remove("Transparent", "Initially-Transparent", "Intransparent");
            el.style.display = "none";
          });

          // Serverantwort verarbeiten
          outputText.innerText = data.message_quant;
          outputReference.innerText = data.message_reference;
          outputVerbal.innerText = data.message_verbal;
          outputQuelle.innerText = data.message_source;

          outputText.style.display = "block";
          outputReference.style.display = "block";
          outputVerbal.style.display = "block";
          outputQuelle.style.display = "block";

          // Logik für NR und UR
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

          // Farblogik Quelle
          if (
            data.message_source.trim() === "Both sources are provided. Please validate." ||
            data.message_source.trim() === "A source is provided. Please validate."
          ) {
            outputQuelle.classList.add("Transparent");
          } else {
            outputQuelle.classList.add("Initially-Transparent");
          }

          // Farblogik Reference
          if (
            data.message_reference.trim() ===
            "Our tool could not detect any reference class descriptions in the given text extract."
          ) {
            outputReference.classList.add("Intransparent");
          } else {
            outputReference.classList.add("Transparent");
          }

          // Farblogik Verbal
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
            R1_2: "Transparent",
            R2_2: "Initially-Transparent",
            R3_2: "Intransparent",
            NN: "Intransparent"
          };

          const caseClass = caseToClass[data.eval_case];
          if (caseClass) {
            outputText.classList.add(caseClass);
          }
        })
        .catch((err) => {
          outputText.innerText = "❌ Fehler beim Serveraufruf: " + err.message;
          outputText.style.display = "block";
        })
        .finally(() => {
          analyzeBtn.disabled = false;
          analyzeText.innerText = "Analysieren";
          spinner.style.display = "none";
        });
    });
  });
});