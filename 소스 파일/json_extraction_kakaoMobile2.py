import json
import os


def convert_to_json(txt_file):
    messages = []
    current_date = None

    with open(txt_file, "r", encoding="utf-8") as file:
        lines = file.readlines()[2:]  # 맨 윗 두 줄 스킵
        for line in lines:
            line = line.strip()
            # 대화 정보인지 확인
            if ":" not in line:
                continue
            # 시간(time), 이름(name), 텍스트(text)를 추출
            tempDate = line.split(". ")
            year = tempDate[0].zfill(4)
            month = tempDate[1].zfill(2)
            day = tempDate[2].split()[0].zfill(2)
            current_date = f"{year}-{month}-{day}"

            parts = line.split(", ")
            time = parts[0].split()[-1]

            hour = time.split(":")[0].zfill(2)
            minute = time.split(":")[1].zfill(2)

            tempTime = parts[0].split()[-2]
            name, text = parts[1].split(" : ", 1)

            # 시간 형식 변환 (12시간 -> 24시간)
            if "오후" in tempTime:
                if hour != "12":
                    hour = int(hour) + 12
            time = str(hour) + ":" + minute

            if current_date is not None:
                date = current_date + "T" + time + ":00"
            else:
                date = None

            message = {
                "date": date,
                "name": name.strip() if name else None,
                "text": text.strip()
            }
            messages.append(message)

    return messages


def run(input_file):
    # JSON 형식으로 변환하여 저장
    messages = convert_to_json(input_file)

    # 날짜별로 데이터 구분
    data_by_month = {}
    for message in messages:
        date = message["date"]
        if date:
            year_month = date[:7]  # YYYY-MM 형식
            if year_month not in data_by_month:
                data_by_month[year_month] = []
            data_by_month[year_month].append(message)

    # 데이터를 각각의 파일에 저장
    output_directory = "./src/"

    # 디렉토리가 없는 경우에 생성
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for year_month, data in data_by_month.items():
        output_file = output_directory + f"data{year_month.replace('-', '')}.json"
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write(json_data)

    print("JSON 데이터가 성공적으로 저장되었습니다.")
