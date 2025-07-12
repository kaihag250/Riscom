import pandas as pd

# Excel-Datei laden
df = pd.read_excel("inference_testing_results_1107.xlsx")

# Als CSV speichern
df.to_csv("model_output.csv", index=False)

print("Datei erfolgreich als CSV gespeichert.")
