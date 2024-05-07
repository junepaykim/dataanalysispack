import pandas as pd
import matplotlib.pyplot as plt
import os


def process_excel_file(filename: str) -> dict:
    """
    Processes an Excel file to extract data and aggregate it.
    It removes the first four columns, interprets the rest of the data,
    and returns a dictionary where keys are `codenum`s (item ID prefixes) and values
    are lists of tuples of aggregated data.

    Args:
        filename (str): The path to the Excel file to be processed.

    Returns:
        dict: A dictionary containing the `codenum`s as keys.
    """
    xls = pd.ExcelFile(filename)

    try:
        df = pd.read_excel(xls, sheet_name="site")
    except ValueError:
        df = pd.read_excel(xls, sheet_name=1)

    columns = df.columns
    data = df.values

    df = pd.DataFrame(data, columns=columns)

    data_groups = {}

    for _, row in df.iterrows():
        item_id = row.iloc[0]

        if not isinstance(item_id, str):
            continue
        key = item_id.split("_")[0]
        codenum = key[:-1]
        last_char = key[-1]

        if last_char not in ["N", "P"]:
            continue

        if codenum not in data_groups:
            data_groups[codenum] = {}

        # Remove first four columns : ITEM_ID val(SPEC_LOW) 	val(TARGET)	val(SPEC_HIGH)

        tuple_array = [
            (last_char, index, value)
            for index, value in enumerate(row[4:], start=4)
            if pd.notna(value)
        ]
        data_groups[codenum].setdefault(last_char, []).append(tuple_array)

    refined_data_groups = {}
    for code, groups in data_groups.items():
        n_data = [item for sublist in groups.get("N", []) for item in sublist]
        p_data = [item for sublist in groups.get("P", []) for item in sublist]

        combined = {}
        for last_char, index, value in n_data:
            combined.setdefault(index, [None, None])[0] = value
        for last_char, index, value in p_data:
            combined.setdefault(index, [None, None])[1] = value

        refined_data_groups[code] = [
            (vals[0], vals[1]) for _, vals in sorted(combined.items())
        ]

    return refined_data_groups


def graph_scatterplot(data_dict: dict, output_dir: str = None) -> None:
    """
    Saves a scatter plot for each data group in the provided dictionary.

    Args:
        data_dict (dict): A dictionary where keys are codenums and values are lists of tuples,
                          each tuple containing a pair of floats (N value, P value).
        output_dir (str): The directory where the scatter plot images will be saved.
                          If None, uses "./output".

    Returns:
        None: Saves the scatter plots.
    """
    if output_dir is None:
        output_dir = "./output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for codenum, data in data_dict.items():
        x_values = [x[0] for x in data if x[0] is not None]
        y_values = [y[1] for y in data if y[1] is not None]
        plt.figure(figsize=(10, 5))
        plt.scatter(x_values, y_values, alpha=0.5)
        plt.title(f"Scatter Plot for {codenum}")
        plt.xlabel("N values")
        plt.ylabel("P values")
        plt.grid(True)
        if output_dir:
            file_path = os.path.join(output_dir, f"{codenum}_scatterplot.png")
            plt.savefig(file_path)
        plt.close()


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "Dophin5_NZWB2_TR_WAT_Rawdata.xlsx"
    targetfile = os.path.join(current_dir, filename)
    grouped_data = process_excel_file(targetfile)
    graph_scatterplot(grouped_data)


if __name__ == "__main__":
    main()
