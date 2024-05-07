import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def graph_boxplot(
    aggregated_data: dict, output_dir: str = None, colorful: bool = False
) -> None:
    """
    Generates a box plot for each data in the dictionary and saves them to pngs.

    Args:
        aggregated_data (dict): A dictionary where keys are dataset names and values are lists of tuples.
                          Each tuple contains a pair of values (X, Y) for plotting.
        output_dir (str): The directory where the box plot images will be saved. If None, defaults to "./output".
        colorful (bool): Determines whether each box in the box plot should have a unique color.
                         If False, all boxes will use the default color.
    """
    if output_dir is None:
        output_dir = "./output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for key, data in aggregated_data.items():
        df = pd.DataFrame(data, columns=["X", "Y"])
        df = df[df["X"] <= 8]

        if colorful:
            palette = sns.color_palette("hsv", n_colors=len(df["X"].unique()))
        else:
            palette = "deep"

        plt.figure(figsize=(12, 8))
        sns.boxplot(x="X", y="Y", hue="X", data=df, palette=palette)
        plt.title(f"{key}")
        plt.xlabel("Wafer ID")
        plt.ylabel("")
        plt.grid(True)
        plt.legend(title="", loc="upper left", bbox_to_anchor=(1.02, 1))

        output_path = os.path.join(
            output_dir, f"{key.replace(' ', '_').replace('/', '_')}_boxplot.png"
        )
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()


def aggregate_data(data: dict) -> dict:
    """
    Aggregates numerical data from different sheets or DataFrame columns into a dictionary.

    Args:
        data (dict): A dictionary where each key is a name and each value is a DataFrame.

    Returns:
        dict: A dictionary where each key is an 'ITEM_ID' and each value is a list of tuples.
              Each tuple contains a pair of integers (column index, value).
    """
    aggregated_data = {}

    for site, df in data.items():
        for index, row in df.iterrows():
            item_id = row["ITEM_ID"]
            if item_id not in aggregated_data:
                aggregated_data[item_id] = []

            for col in df.columns:
                if str(col).isdigit():
                    aggregated_data[item_id].append((int(col), row[col]))

    return aggregated_data


def read_excel_sheets(filename: str) -> dict:
    """
    Reads specified patterns of sheets from an Excel file into DataFrames.

    Args:
        filename (str): Path to the Excel file.

    Returns:
        dict: A dictionary with sheet names as keys and DataFrames as values.
    """

    xls = pd.ExcelFile(filename)

    sheet_names = [
        name for name in xls.sheet_names if "NZWB2" in name and "_SITE" in name
    ]

    data_frames = {}
    for sheet_name in sheet_names:
        data_frames[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

    return data_frames


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "Dolphin5_NZWB2_BEOL_WAT_Raw data.xlsx"
    targetfile = os.path.join(current_dir, filename)
    sheet_data = read_excel_sheets(targetfile)
    aggregated_data = aggregate_data(sheet_data)
    graph_boxplot(aggregated_data, colorful=True)


if __name__ == "__main__":
    main()
