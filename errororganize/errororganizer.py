import os


def process_input_file(input_file_path: str) -> None:
    """
    입력 파일을 읽고, 각 Operating Sequence / Pattern 을 분석하여
    패턴명으로 에러 데이터가 포함된 파일을 생성
    Args:
        input_file_path (_type_): 처리하려는 입력 파일의 경로
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
    주어진 패턴명에 따라 에러 데이터를 파일에 작성
    
    Args:
        pattern (str): 파일명으로 사용될 패턴명
        data_lines (list): 파일에 작성할 데이터 라인들의 리스트
        file_mode (str): 파일을 열 때 사용할 모드 ('w', 'a')
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
                formatted_line = f"{parts[2]:<15}\t{parts[1]:<10}\t{parts[3]:<15}\n"
                output_file.write(formatted_line)


def sort_and_remove_duplicates(filename: str) -> None:
    """
    지정된 파일에서 중복을 제거하고 cycle로 데이터를 정렬
    파일 내의 데이터를 정렬된 상태로 유지
    
    Args:
        filename (str): 중복 제거 및 정렬을 수행할 파일명
    """
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        unique_lines = set(lines[1:])

        def custom_sort_key(x):
            parts = x.split()

            return int((parts[0]))

        sorted_lines = sorted(unique_lines, key=custom_sort_key)

        with open(filename, "w", encoding="utf-8") as file:
            file.write(lines[0])
            file.writelines(sorted_lines)


def main():
    # input_file_name 조정을 통해 처리 대상 파일 지정 가능
    input_file_name = "inputdata"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(current_dir, input_file_name)

    process_input_file(input_file_path)


if __name__ == "__main__":
    main()
