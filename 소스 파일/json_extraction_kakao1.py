import json
import os


def convert_to_json(txt_file):
    messages = []
    current_date = None

    with open(txt_file, "r", encoding="utf-8") as file:
        lines = file.readlines()[2:]  # 맨 윗 두 줄 스킵

        for line in lines:
            line = line.strip()
            if line.startswith("---------------"):
                # 헤더에서 날짜(date)를 추출
                date_line = line.split()[1:]
                current_date = " ".join(date_line).split("-----")[0].strip()
                # 날짜 형식 변환
                year = current_date.split("년 ")[0]
                month = current_date.split("년 ")[1].split("월 ")[0].zfill(2)
                day = current_date.split("월 ")[1].split("일 ")[0].zfill(2)
                current_date = f"{year}-{month}-{day}"
            elif line:
                # 시간(time), 이름(name), 텍스트(text)를 추출
                parts = line.split("] ")
                name = parts[0].strip("[]")
                time = " ".join(parts[1:-1]).strip("[]")
                text = parts[-1]

                # 시간 형식 변환 (12시간 -> 24시간)
                if "오후" in time:
                    hour = int(time.split()[1].split(":")[0]) + 12
                    minute = time.split()[1].split(":")[1]
                    time = f"{hour:02d}:{minute}"

                if current_date is not None:
                    date = current_date + "T" + time + ":00"
                else:
                    date = None

                message = {
                    "date": date,
                    "name": name if name else None,
                    "text": text
                }
                messages.append(message)

    json_data = json.dumps(messages, indent=4, ensure_ascii=False)

    # 필터링된 데이터를 저장할 디렉토리
    output_directory = "./src/"

    # 디렉토리가 없는 경우에 생성
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_file = output_directory + "data.json"

    # JSON 데이터를 파일에 저장
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(json_data)

    print("JSON 데이터가 성공적으로 저장되었습니다.")


def run(input_file):
    # JSON 형식으로 변환하여 저장
    convert_to_json(input_file)
