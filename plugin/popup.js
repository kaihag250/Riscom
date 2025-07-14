const SERVER_URL = "http://193.196.39.15:8000/extract";

function formatTextBold(text, includeNumbers = false) {
  if (!text) return "";

  // Sonderzeichen escapen
  text = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Schlagwörter fett
  const keywords = ["Caution", "Attention", "Warning"];
  keywords.forEach(word => {
    const regex = new RegExp(`\\b(${word})\\b`, "gi");
    text = text.replace(regex, "<b>$1</b>");
  });

  // Zahlen fett (optional)
  if (includeNumbers) {
    text = text.replace(/(\d+(\.\d+)?%?)/g, "<b>$1</b>");
  }

  return text;
}

// 🔧 Neue Funktion zur Textbereinigung
function cleanText(text) {
  return text
    .replace(/[\u200B-\u200D\uFEFF]/g, '')  // Zero-width chars
    .replace(/\u00A0/g, ' ')                // Geschützte Leerzeichen
    .replace(/\r?\n|\r/g, ' ')              // Zeilenumbrüche
    .replace(/\s+/g, ' ')                   // Mehrfache Leerzeichen
    .trim();
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("analyze");
  const analyzeText = document.getElementById("analyzeText");
  const spinner = document.getElementById("spinner");
  const outputText = document.getElementById("outputText");
  const outputReference = document.getElementById("outputReference");
  const outputVerbal = document.getElementById("outputVerbal");
  const outputQuelle = document.getElementById("outputQuelle");

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    analyzeText.innerText = "Analyzing …";
    spinner.style.display = "inline-block";

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript(
      {
        target: { tabId: tab.id },
        func: () => window.getSelection().toString()
      },
      async (results) => {
        let selectedText = results[0].result || "";
        selectedText = cleanText(selectedText); // 🧼 Bereinigung

       if (!selectedText || selectedText.length < 5) {
         outputText.innerText = "⚠️ No valid text selected. Please mark some meaningful text.";
         outputText.style.display = "block";
         resetButton();
         return; }

        ["outputText", "outputVerbal", "outputQuelle", "outputReference"].forEach(id => {
          const el = document.getElementById(id);
          el.classList.remove("Transparent", "Initially-Transparent", "Intransparent");
        });

        if (!selectedText) {
          outputText.innerText = "⚠️ No text selected.";
          outputText.style.display = "block";
          resetButton();
          return;
        }

        if (selectedText.length > 650) {
          outputText.innerText = "⚠️ The selected text exceeds the maximum text length.";
          outputText.style.display = "block";
          resetButton();
          return;
        }

        try {
          const res = await fetch(SERVER_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: selectedText })
          });

          const data = await res.json();
          console.log("Full response:", data);

          if (data.advice) {
            const {
              message_quant,
              message_reference,
              message_verbal,
              message_source,
              eval_case_overall
            } = data.advice;

            outputText.innerHTML = formatTextBold(message_quant, true);
            outputReference.innerHTML = formatTextBold(message_reference);
            outputVerbal.innerHTML = formatTextBold(message_verbal);
            outputQuelle.innerHTML = formatTextBold(message_source);

            outputText.style.display = "block";
            outputReference.style.display = "block";
            outputVerbal.style.display = "block";
            outputQuelle.style.display = "block";

            if (
              message_source?.trim().includes("Both sources are provided. Please validate.") ||
              message_source?.trim().includes("A source is provided. Please validate.")
            ) {
              outputQuelle.classList.add("Transparent");
            } else {
              outputQuelle.classList.add("Initially-Transparent");
            }

            if (
              message_reference?.trim() ===
              "The tool did not identify any reference class description in the selected text."
            ) {
              outputReference.classList.add("Initially-Transparent");
            } else {
              outputReference.classList.add("Transparent");
            }

            if (message_verbal?.trim()) {
              outputVerbal.classList.add("Initially-Transparent");
            } else {
              outputVerbal.style.display = "none";
            }

            const caseToClass = {
              L1: "Transparent",
              L2: "Initially-Transparent",
              L3: "Intransparent",
              L4: "Intransparent",
              "R1.1": "Transparent",
              "R2.1": "Initially-Transparent",
              "R3.1": "Intransparent",
              NN: "Intransparent",
              UR: "Initially-Transparent"
            };

            const caseClass = caseToClass[eval_case_overall];
            if (caseClass) {
              outputText.classList.add(caseClass);
            }

            if (eval_case_overall === "NR" || eval_case_overall === "UR") {
              outputText.innerHTML = formatTextBold(message_quant, true);
              outputReference.style.display = "none";
              outputVerbal.style.display = "none";
              outputQuelle.style.display = "none";
            }

          } else {
            outputText.style.display = "block";
            outputText.innerText = "❌ No server response";
          }

        } catch (err) {
          outputText.style.display = "block";
          outputText.innerText = "⚠️ Error: " + err.message;
        } finally {
          resetButton();
        }
      }
    );
  });

  function resetButton() {
    analyzeText.innerText = "Analyze";
    spinner.style.display = "none";
    btn.disabled = false;
  }
});