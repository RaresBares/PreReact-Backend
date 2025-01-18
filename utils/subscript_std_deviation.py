import pandas as pd
import argparse


def main(args):
        df = pd.read_csv(args.file)

      # Standardabweichung berechnen
        std = df["raw"].std()

        # Standardabweichung in DataFrame umwandeln
        data = pd.DataFrame({"stddev": [std]})

        # In die Datei schreiben oder anhängen
        data.to_csv(args.file, mode='r+', index=False, header=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="arguments")
    parser.add_argument("--file", type=str, required=True, help="The location of the file")

    args = parser.parse_args()
    main(args)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="arguments")
    parser.add_argument("--file", type=str, required=True, help="The location of the file")

    args = parser.parse_args()
    main(args)