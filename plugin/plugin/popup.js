document.getElementById("analyze").addEventListener("click", () => {
  const output = document.getElementById("output");

  // Statt API-Call: Simulierter Server-Output zum Testen der Visuals
  // ❗ Nur EINE Variante aktiv lassen, die anderen auskommentieren

  // Variante 1: TRANSPARENT
  const data = {
    label: "Transparent",
    response: "✅ Die Risikokommunikation ist transparent."
  };

  // Variante 2: INITIALLY TRANSPARENT
  /*
  const data = {
    label: "Initially Transparent",
    response: "⚠️ Die Risikokommunikation ist anfangs transparent."
  };
  */

  // Variante 3: INTRANSPARENT
  /*
  const data = {
    label: "Intransparent",
    response: "❌ Die Risikokommunikation ist intransparent."
  };
  */

  // Ausgabe anzeigen
  output.innerText = data.response;

  // Vorherige Klassen entfernen
  output.classList.remove("Transparent", "Initially-Transparent", "Intransparent");

  // Neue Klasse hinzufügen (für CSS-Styling)
  if (["Transparent", "Initially Transparent", "Intransparent"].includes(data.label)) {
    const cssClass = data.label.replace(/\s/g, "-"); // z. B. "Initially Transparent" → "Initially-Transparent"
    output.classList.add(cssClass);
  }
});