def main():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import openpyxl
        import argparse
    except ImportError:
        print("Required modules not found. Installing...")
        import subprocess

        subprocess.check_call(
            ["pip", "install", "pandas", "numpy", "matplotlib", "openpyxl", "argparse"]
        )
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import openpyxl
        import argparse

    parser = argparse.ArgumentParser(
        description="Command line interface for Delta Tuning."
    )

    parser.add_argument(
        "--filename",
        default="data.xlsx",
        type=str,
        help="name of the file to be read ex:  data.xlsx",
    )
    parser.add_argument(
        "--unifyscale",
        default=True,
        type=bool,
        help="Unify scale of all plots or not ex:  True/False",
    )

    args = parser.parse_args()

    df = pd.read_excel(args.filename)
    unique_voltages = sorted(df["Voltage"].unique())

    fig, axes = plt.subplots(
        1, len(unique_voltages), figsize=(15 * len(unique_voltages), 6)
    )

    global_min = float("inf")
    global_max = float("-inf")

    for i, voltage in enumerate(unique_voltages):
        subset = df[df["Voltage"] == voltage]
        groups = subset.groupby("Corner")
        boxes = []

        for name, group in groups:
            boxes.append(group["Value"].values)

        bp = axes[i].boxplot(boxes, labels=groups.groups.keys(), vert=True)
        axes[i].set_title(f"Voltage: {voltage}")
        axes[i].set_xlabel("Corner")

        if args.unifyscale:
            for line in bp["medians"]:
                ydata = line.get_ydata()
                global_min = min(global_min, min(ydata))
                global_max = max(global_max, max(ydata))

    if args.unifyscale:
        for ax in axes:
            ax.set_ylim(global_min, global_max)

    plt.subplots_adjust(wspace=0.4)

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
