#!/usr/bin/env python3
# python excel_to_jsonl.py \/Users/philippeiser/Desktop/Teamprojekt/TrainingData.xlsx \--sheet 0 \--prompt-col "Unnamed: 0" \--output /Users/philippeiser/Desktop/Teamprojekt/Git_Connection/Riscom/TrainingData_formatted.jsonl

import pandas as pd
import json
from datetime import datetime

def excel_to_jsonl(
    excel_path: str,
    sheet_name: int = 0,
    prompt_col: str = 'Unnamed: 0',
    output_jsonl: str = 'output.jsonl'
):
    """
    Liest eine Excel-Datei ein, nimmt die Spalte `prompt_col` als Prompt,
    packt alle anderen Spalten als JSON in das Feld 'response'
    und schreibt jede Zeile als JSON-Objekt in eine .jsonl-Datei.
    """
    # Excel einlesen
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    # Spalte umbenennen für Klarheit
    if prompt_col not in df.columns:
        raise ValueError(f"Spalte '{prompt_col}' nicht gefunden. Verfügbare Spalten: {df.columns.tolist()}")
    df = df.rename(columns={prompt_col: 'prompt'})

    # Hilfsfunktion für Zeile → JSON
    def row_to_dict(row):
        data = row.drop('prompt').to_dict()
        clean = {}
        for k, v in data.items():
            if pd.isna(v):
                continue
            # Datumswerte in ISO-Format
            if isinstance(v, (datetime, pd.Timestamp)):
                clean[k] = v.isoformat()
            else:
                clean[k] = v
        return {'prompt': row['prompt'], 'response': clean}

    # JSONL schreiben
    with open(output_jsonl, 'w', encoding='utf-8') as fout:
        for _, row in df.iterrows():
            record = row_to_dict(row)
            fout.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"\n✓ Fertig! JSONL gespeichert unter: {output_jsonl}")
    print(f"Anzahl Datensätze: {len(df)}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="Konvertiert eine Excel-Tabelle in JSONL (prompt + response-JSON)."
    )
    parser.add_argument('excel_path', help='Pfad zur Excel-Datei (z.B. TrainingData.xlsx)')
    parser.add_argument('--sheet', help='Sheet-Name (falls nicht das erste Sheet)', default=None)
    parser.add_argument('--prompt-col', help='Name der Prompt-Spalte', default='Unnamed: 0')
    parser.add_argument('--output', help='Pfad zur Ausgabedatei (.jsonl)', default='output.jsonl')
    args = parser.parse_args()

    excel_to_jsonl(
        excel_path=args.excel_path,
        sheet_name=args.sheet,
        prompt_col=args.prompt_col,
        output_jsonl=args.output
    )
