import json
import datetime
import glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os


def run(font_path, group_name, result_folder):
    # 폰트 설정
    fontprop = fm.FontProperties(fname=font_path)

    # 시작 날짜와 끝 날짜 입력
    start_date = input("YYYYMM: ")
    start_year = start_date[:4]
    start_month = start_date[4:]
    ChartTitle = start_year + "년 " + start_month + "월"

    # 입력 파일 경로
    input_files = glob.glob(fr".\src\data{start_date}*.json")

    # 전체 사용자의 발신 시간대 정보를 저장할 딕셔너리
    user_hour_counts = {}

    # JSON 파일 읽기
    for input_file in input_files:
        with open(input_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # 사용자별 발신 시간과 메시지 길이 추출 및 처리
        for item in json_data:
            name = item.get("name")
            date_str = item.get("date")
            message_text = item.get("text")
            if name and date_str and message_text:
                sent_time = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                message_length = len(message_text)
                if name in user_hour_counts:
                    if sent_time.hour in user_hour_counts[name]:
                        user_hour_counts[name][sent_time.hour] += message_length
                    else:
                        user_hour_counts[name][sent_time.hour] = message_length
                else:
                    user_hour_counts[name] = {sent_time.hour: message_length}

    # 개별 사용자의 발신 시간대 그래프 그리기
    for name, hour_counts in user_hour_counts.items():
        hours = sorted(hour_counts.keys())
        counts = [hour_counts[hour] for hour in hours]
        plt.plot(hours, counts, label=name)

    plt.xlabel("Hour", fontproperties=fontprop)
    plt.ylabel("Message Length", fontproperties=fontprop)
    plt.suptitle(group_name + " 메세지 전송 시각", fontsize=16, fontproperties=fontprop)
    plt.legend(prop=fontprop)
    plt.title(ChartTitle + " 발신 시간: 글자수 기준", fontproperties=fontprop)

    # 결과 폴더가 없다면 생성
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # 이미지로 저장
    plt.savefig(result_folder + ChartTitle + " " + group_name + " 메세지 전송 시각(글자수 기준).png")

    plt.show()
