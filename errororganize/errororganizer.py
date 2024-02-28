import os


def process_input_file(input_file_path: str) -> None:
    """
    입력 파일을 읽고, 각 Operating Sequence / Pattern 을 분석하여
    패턴명으로 에러 데이터가 포함된 파일을 생성
    Args:
        input_file_path (_type_): 처리하려는 입력 파일의 경로
    """
    with open(input_file_path, "r", encoding="utf-8") as file:
        current_pattern = ""
        data_lines = []
        for line in file:
            if line.startswith("Operating Sequence / Pattern :"):
                if data_lines and len(data_lines) > 1:
                    file_mode = "a" if os.path.exists(f"{current_pattern}.txt") else "w"
                    write_output_file_formatted(current_pattern, data_lines, file_mode)
                data_lines = []
                current_pattern = line.split(":")[-1].strip()
            elif line.strip().startswith("Number"):
                data_lines.append(line.strip())
            elif line.strip() and data_lines:
                data_lines.append(line.strip())

        if data_lines and len(data_lines) > 1:
            file_mode = "a" if os.path.exists(f"{current_pattern}.txt") else "w"
            write_output_file_formatted(current_pattern, data_lines, file_mode)


def write_output_file_formatted(pattern: str, data_lines:list, file_mode:str) -> None:
    """
    지정된 pattern의 파일명을 생성하거나, 에러를 포맷에 맞게 파일에 기록

    Args:
        pattern (str): 출력 파일의 이름 (Operating Sequence / Pattern의 Pattern 값)
        data_lines (list): 기록할 데이터 라인들
        file_mode (str): 파일 열기 모드 (w: 쓰기, a: 추가)
    """
    if len(data_lines) > 1:
        filename = f"{pattern}.txt"
        with open(filename, file_mode, encoding="utf-8") as output_file:
            if file_mode == "w":
                header = f"{'Failing Cycles':<15}\t{'Signal':<10}\t{'Expected States':<15}\t{'Number':<6}"
                output_file.write(header + "\n")
            for line in data_lines[1:]:
                parts = line.split()
                formatted_line = (
                    f"{parts[2]:<15}\t{parts[1]:<10}\t{parts[3]:<15}\t{parts[0]:<6}"
                )
                output_file.write(formatted_line + "\n")


def main():
    # 파일 경로는 현재 작업 디렉토리의 inputdata 파일임을 가정하고 만듬
    input_file_name = "inputdata"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(current_dir, input_file_name)

    process_input_file(input_file_path)


if __name__ == "__main__":
    main()
