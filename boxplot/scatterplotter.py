import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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

    indexrow = df.iloc[1]
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

        tuple_array = [
            (last_char, indexrow[index], value)
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
            (index, vals[0], vals[1]) for index, vals in sorted(combined.items())
        ]

    return refined_data_groups


def graph_scatterplot(
    grouped_data: dict, output_dir: str = "./output", padding: float = 0.1
) -> None:
    """
    Saves a scatter plot for each data group in the provided dictionary.

    Args:
        grouped_data (dict): A dictionary where keys are codenums and values are lists of tuples,
                          each tuple containing a pair of floats (N value, P value).
        output_dir (str): The directory where the scatter plot images will be saved.
    """
    target_codenums = ["LVT", "RVT", "SLVT"]

    plot_data = {
        codenum: grouped_data[codenum]
        for codenum in target_codenums
        if codenum in grouped_data
    }

    index_int = []
    for codenum in plot_data:
        for data_list in plot_data[codenum]:
            modified_data_list = (int(data_list[0]), data_list[1], data_list[2])
            index_int.append((codenum,) + modified_data_list)

    # Filtering out indexes greater than 8
    all_values = [value for value in index_int if value[1] <= 8]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if all_values:
        index_color_map = {
            index: i
            for i, index in enumerate(sorted(set(val[1] for val in all_values)))
        }
        color_array = [index_color_map[val[1]] for val in all_values]
        colors = plt.get_cmap("viridis")(
            [
                index_color_map[val[1]] / max(index_color_map.values())
                for val in all_values
            ]
        )

        plt.figure(figsize=(10, 5))
        codenum_groups = {codenum: [] for codenum in target_codenums}
        for value in all_values:
            label = f"NZWB2_{value[1]}"
            plt.scatter(
                value[2],
                value[3],
                color=colors[color_array.index(index_color_map[value[1]])],
                label=label,
                alpha=0.5,
            )
            codenum_groups[value[0]].append((value[2], value[3]))

        for codenum, points in codenum_groups.items():
            if points:
                x_coords, y_coords = zip(*points)
                min_x, max_x = min(x_coords), max(x_coords)
                min_y, max_y = min(y_coords), max(y_coords)
                width, height = max_x - min_x, max_y - min_y
                padded_rect = patches.Rectangle(
                    (min_x - padding * width, min_y - padding * height),
                    width + 2 * padding * width,
                    height + 2 * padding * height,
                    linewidth=1,
                    edgecolor="r",
                    facecolor="none",
                )
                plt.gca().add_patch(padded_rect)
                plt.text(
                    min_x + width / 2,
                    max_y + padding * height,
                    codenum,
                    horizontalalignment="center",
                    verticalalignment="top",
                    fontsize=10,
                )

        plt.title("RO_SDB_Vt_Targeting")
        plt.xlabel("RO_nMOS_SDB_Vtsat (N)")
        plt.ylabel("RO_pMOS_SDB_Vtsat (P)")
        plt.grid(True)

        handles, labels = plt.gca().get_legend_handles_labels()
        unique_labels = dict(zip(labels, handles))
        plt.legend(
            unique_labels.values(),
            [label.split("_")[1] for label in unique_labels.keys()],
            loc="upper left",
            bbox_to_anchor=(1, 1),
        )

        file_path = os.path.join(output_dir, "LVT_RVT_SLVT_scatterplot.png")
        plt.savefig(file_path, bbox_inches="tight")
        plt.close()


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "Dophin5_NZWB2_TR_WAT_Rawdata.xlsx"
    targetfile = os.path.join(current_dir, filename)
    grouped_data = process_excel_file(targetfile)
    graph_scatterplot(grouped_data)


if __name__ == "__main__":
    main()
