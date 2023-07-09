import json


def run(input_file, output_file):

    # 치환할 내용 설정
    replacement_text = "(인터넷공유)"

    # 필요한 정보를 저장할 리스트
    filtered_data = []

    # JSON 파일 읽기
    with open(input_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # JSON 데이터 추출
    if isinstance(json_data, dict):
        # 필요한 정보 추출
        name = json_data.get("name")
        messages = json_data.get("messages", [])

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

                # 필터링된 데이터를 새로운 JSON 형식으로 저장
                filtered_data.append({
                    "date": message_date,
                    "name": message_from,
                    "text": message_text
                })

    # 새로운 JSON 파일 저장
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)

    print("추출이 완료되었습니다.")
