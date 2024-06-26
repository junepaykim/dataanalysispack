import os


def process_input_file(input_file_path: str) -> None:
    """
    Read the input file and analyze each Operating Sequence / Pattern
    Create a file containing error data with a pattern name.
    Args:
        input_file_path (_type_): Path to the input file you want to process
    """
    written_files = set()

    with open(input_file_path, "r", encoding="utf-8") as file:
        current_pattern = ""
        data_lines = []
        for line in file:
            if line.startswith("Operating Sequence / Pattern :"):
                if data_lines and len(data_lines) > 1:
                    file_mode = "a" if os.path.exists(f"{current_pattern}.txt") else "w"
                    write_rawdata(current_pattern, data_lines, file_mode)
                    written_files.add(f"{current_pattern}.txt")
                data_lines = []
                current_pattern = line.split(":")[-1].strip().split(".")[-1]
            elif line.strip().startswith("Number"):
                data_lines.append(line.strip())
            elif line.strip() and data_lines:
                data_lines.append(line.strip())

        if data_lines and len(data_lines) > 1:
            file_mode = "a" if os.path.exists(f"{current_pattern}.txt") else "w"
            write_rawdata(current_pattern, data_lines, file_mode)
            written_files.add(f"{current_pattern}.txt")

    for filename in written_files:
        sort_and_remove_duplicates(filename)


def write_rawdata(pattern: str, data_lines: list, file_mode: str) -> None:
    """
    Write error data to a file according to the given pattern name.

    Args:
        pattern (str): Pattern name to be used as file name
        data_lines (list): List of data lines to write to file
        file_mode (str): Mode to use when opening the file ('w', 'a')
    """
    if len(data_lines) > 1:
        filename = f"{pattern}.txt"
        unique_lines = set(data_lines[1:])
        with open(filename, file_mode, encoding="utf-8") as output_file:
            if file_mode == "w":
                header = (
                    f"{'Failing Cycles':<15}\t{'Signal':<10}\t{'Expected States':<15}\n"
                )
                output_file.write(header)
            for line in unique_lines:
                parts = line.split()
                parts3_replace = 1 if parts[3] == "H" else 0
                formatted_line = (
                    f"C {parts[2]:<15}\t{parts[1]:<10}\t{parts3_replace:<15}\n"
                )
                output_file.write(formatted_line)


def sort_and_remove_duplicates(filename: str) -> None:
    """
    Remove duplicates from specified files and sort data by cycle
    Keep data within files sorted

    Args:
        filename (str): File name to remove duplicates and sort
    """
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        unique_lines = set(lines[1:])

        def custom_sort_key(x):
            parts = x.split()

            if parts[0].isdigit():
                return int(parts[0])
            elif len(parts[0]) == 1 and parts[1].isdigit():
                return int(parts[1])
            else:
                return float("inf")

        sorted_lines = sorted(unique_lines, key=custom_sort_key)

        with open(filename, "w", encoding="utf-8") as file:
            file.write(lines[0])
            file.writelines(sorted_lines)


def main():
    # input_file_name to select specific input file
    input_file_name = "inputdata"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(current_dir, input_file_name)

    process_input_file(input_file_path)


if __name__ == "__main__":
    main()
