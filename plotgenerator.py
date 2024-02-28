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
        description="Command line interface for generating boxplots from excel files"
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

    parser.add_argument(
        "--figsize_horizontal",
        default=18,
        type=int,
        help="Horizontal size of the whole figure ex:  18",
    )

    parser.add_argument(
        "--Voltage_name",
        default="Voltage",
        type=str,
        help="Name of the column containing voltage values ex:  Voltage",
    )

    args = parser.parse_args()

    df = pd.read_excel(args.filename)
    unique_voltages = sorted(df[args.Voltage_name].unique())

    fig, axes = plt.subplots(
        1,
        len(unique_voltages),
        figsize=(args.figsize_horizontal * len(unique_voltages), 6),
    )

    max_value = df["Value"].max()
    min_value = df["Value"].min()

    for i, voltage in enumerate(unique_voltages):
        subset = df[df[args.Voltage_name] == voltage]
        groups = subset.groupby("Corner")
        boxes = []

        for name, group in groups:
            boxes.append(group["Value"].values)

        axes[i].boxplot(boxes, labels=groups.groups.keys(), vert=True)
        axes[i].set_title(f"Voltage: {voltage}")
        axes[i].set_xlabel("Corner")

    if args.unifyscale:
        for ax in axes:
            ax.set_ylim(min_value, max_value)

    plt.subplots_adjust(wspace=0.5)
    fig.tight_layout(rect=[0.01, 0, 0.99, 1])
    plt.show()


if __name__ == "__main__":
    main()
