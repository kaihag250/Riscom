const SERVER_URL = "http://193.196.39.15:8000/extract-advice";

function formatTextBold(text, includeNumbers = false) {
  const keywords = [
    "Caution",
    "Attention",
    "Warning"
  ];

  keywords.forEach(word => {
    const regex = new RegExp(`\\b(${word})\\b`, "gi");
    text = text.replace(regex, "<b>$1</b>");
  });

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

      // ⬇️ POST an Server
      fetch(SERVER_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ input: selectedText })
      })
      .then(response => response.json())
      .then(data => {
        // Klassen zurücksetzen
        ["outputText", "outputVerbal", "outputQuelle", "outputReference"].forEach(id => {
          const el = document.getElementById(id);
          el.classList.remove("Transparent", "Initially-Transparent", "Intransparent");
        });

        // Sichtbarkeit
        outputText.style.display = "block";
        outputReference.style.display = "block";
        outputVerbal.style.display = "block";
        outputQuelle.style.display = "block";

        // Quelle
        if (
          data.message_source?.trim().includes("Both sources are provided. Please validate.") || 
          data.message_source?.trim().includes("A source is provided. Please validate.")
        ) {
          outputQuelle.classList.add("Transparent");
        } else {
          outputQuelle.classList.add("Initially-Transparent");
        }

        // Reference
        if (
          data.message_reference?.trim() ===
          "The tool did not identify any reference class description in the selected text."
        ) {
          outputReference.classList.add("Initially-Transparent");
        } else {
          outputReference.classList.add("Transparent");
        }

        // Verbal
        if (data.message_verbal?.trim()) {
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

        const caseClass = caseToClass[data.eval_case_overall];
        if (caseClass) {
          outputText.classList.add(caseClass);
        }

        // Ergebnis formatieren
        outputText.innerHTML = formatTextBold(data.message_quant || "", true);
        outputReference.innerHTML = formatTextBold(data.message_reference || "");
        outputVerbal.innerHTML = formatTextBold(data.message_verbal || "");
        outputQuelle.innerHTML = formatTextBold(data.message_source || "");

        if (data.eval_case_overall === "NR" || data.eval_case_overall === "UR") {
          outputText.innerHTML = formatTextBold(data.message_quant || "");
          outputReference.style.display = "none";
          outputVerbal.style.display = "none";
          outputQuelle.style.display = "none";
        }

        // Zurücksetzen
        analyzeBtn.disabled = false;
        analyzeText.innerText = "Analyze";
        spinner.style.display = "none";
      })
      .catch(err => {
        outputText.innerText = `❌ Server error: ${err.message}`;
        outputText.style.display = "block";
        analyzeBtn.disabled = false;
        analyzeText.innerText = "Analyze";
        spinner.style.display = "none";
      });
    });
  });
});