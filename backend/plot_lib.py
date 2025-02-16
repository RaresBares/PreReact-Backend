import matplotlib.pyplot as plt
import numpy as np

from backend.generics.Feature import Feature


def show_Feature(raw_data,data, name=""):
    fig, (raw, feat) = plt.subplots(1, 2, layout="constrained")
    raw.plot(range(0, len(raw_data)), raw_data)
    raw.set_xlabel("frequency")
    raw.set_ylabel("amplitude")
    raw.set_title("Raw data")

    feat.plot(range(0, len(data)), data)
    feat.set_xlabel("frequency")
    feat.set_ylabel("amplitude")
    feat.set_title(f"{name}")

    return fig, raw, feat



