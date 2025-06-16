chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getSelection") {
    let selectedText = "";

    // Versuch 1: Normale Markierung
    if (window.getSelection) {
      selectedText = window.getSelection().toString().trim();
    }

    // Versuch 2: Innerhalb eines Shadow DOM oder komplexer Blöcke
    if (!selectedText) {
      const active = document.activeElement;
      if (active && typeof active.value === "string") {
        const start = active.selectionStart;
        const end = active.selectionEnd;
        selectedText = active.value.substring(start, end).trim();
      }
    }

    // Ergebnis zurückgeben
    sendResponse({ text: selectedText || "" });
    return true; // wichtig für asynchronen Response
  }
});