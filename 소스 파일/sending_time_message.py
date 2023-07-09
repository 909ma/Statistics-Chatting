import json
import datetime
import glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os


def run(font_path, group_name, result_folder):
    start_date = input("YYYYMM: ")
    start_year = start_date[:4]
    start_month = start_date[4:]
    ChartTitle = start_year + "년 " + start_month + "월"

    # 폰트 설정
    fontprop = fm.FontProperties(fname=font_path)

    # 입력 파일 경로
    input_files = glob.glob(fr".\src\data{start_date}*.json")

    # 전체 사용자의 발신 시간대 정보를 저장할 딕셔너리
    user_hour_counts = {}

    # JSON 파일 읽기
    for input_file in input_files:
        with open(input_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # 사용자별 발신 시간 추출 및 처리
        for item in json_data:
            name = item.get("name")
            date_str = item.get("date")
            if name and date_str:
                sent_time = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                if name in user_hour_counts:
                    user_hour_counts[name].append(sent_time.hour)
                else:
                    user_hour_counts[name] = [sent_time.hour]

    # 개별 사용자의 발신 시간대 그래프 그리기
    for name, hour_counts in user_hour_counts.items():
        hour_counts_dict = {}
        for hour in hour_counts:
            if hour in hour_counts_dict:
                hour_counts_dict[hour] += 1
            else:
                hour_counts_dict[hour] = 1

        hours = sorted(hour_counts_dict.keys())
        counts = [hour_counts_dict[hour] for hour in hours]
        plt.plot(hours, counts, label=name)

    plt.xlabel("Hour", fontproperties=fontprop)
    plt.ylabel("Count", fontproperties=fontprop)
    plt.suptitle(group_name + " 메세지 전송 시각", fontsize=16, fontproperties=fontprop)
    plt.legend(prop=fontprop)
    plt.title(ChartTitle + " 발신 시간: 메세지 건 수 기준", fontproperties=fontprop)

    # 결과 폴더가 없다면 생성
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # 이미지로 저장
    plt.savefig(result_folder + ChartTitle + " " + group_name + " 메세지 전송 시각(메세지 건 수 기준).png")

    plt.show()
