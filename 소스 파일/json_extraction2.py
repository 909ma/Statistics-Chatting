import json
import datetime
import os


def run(input_file):
    # 필터링된 데이터를 저장할 디렉토리
    output_directory = "./src/"

    # 치환할 내용 설정
    replacement_text = "(인터넷공유)"

    # JSON 파일 읽기
    with open(input_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # JSON 데이터 추출
    if isinstance(json_data, dict):
        # 필요한 정보 추출
        name = json_data.get("name")
        messages = json_data.get("messages", [])

        # 날짜별로 데이터 그룹화
        grouped_data = {}
        for message in messages:
            if isinstance(message, dict):
                # 필요한 정보 추출
                message_date = message.get("date")
                message_from = message.get("from")
                message_text = message.get("text") if "text" in message else "(NULL)"
                # 텍스트 치환
                if message_text and isinstance(message_text, list):
                    for i in range(len(message_text)):
                        if isinstance(message_text[i], dict):
                            if "type" in message_text[i] and message_text[i]["type"] == "link":
                                url = message_text[i].get("text")
                                if url and url.startswith("http"):
                                    message_text[i]["text"] = replacement_text

                # 날짜 형식 변환
                date = datetime.datetime.strptime(message_date, "%Y-%m-%dT%H:%M:%S")
                output_filename = date.strftime("data%Y%m.json")

                # 그룹화된 데이터에 추가
                if output_filename in grouped_data:
                    grouped_data[output_filename].append({
                        "date": message_date,
                        "name": message_from,
                        "text": message_text
                    })
                else:
                    grouped_data[output_filename] = [{
                        "date": message_date,
                        "name": message_from,
                        "text": message_text
                    }]

        # 디렉토리가 없는 경우에 생성
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # 그룹화된 데이터를 각각의 파일로 저장
        for filename, data in grouped_data.items():
            output_file = os.path.join(output_directory, filename)

            # 새로운 JSON 파일 저장
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.write("\n")

    print("추출이 완료되었습니다.")
