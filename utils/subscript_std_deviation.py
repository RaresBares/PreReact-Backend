import pandas as pd
import argparse

def main(args):
    # CSV einlesen
    df = pd.read_csv(args.file)

    # Standardabweichung berechnen
    std = df["raw"].std()

    # Spalte 'features' prüfen und ggf. hinzufügen
    if "features" not in df.columns:
        df["features"] = ""  # Statt None leere Strings einfügen

    # Standardabweichung in die erste Zelle der Spalte schreiben
    df.loc[0, "features"] = std

    # Debugging-Ausgaben
    print("DataFrame vor dem Speichern:")
    print(df)

    # Änderungen in die Datei schreiben
    df.to_csv(args.file, index=True, header=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="arguments")
    parser.add_argument("--file", type=str, required=True, help="The location of the file")

    args = parser.parse_args()
    main(args)
