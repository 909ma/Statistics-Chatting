import json
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

    # 전체 사용자의 메시지 길이와 발신량을 저장할 딕셔너리
    user_message_lengths = {}
    user_message_counts = {}

    # JSON 파일 읽기
    for input_file in input_files:
        with open(input_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # 사용자별 메시지 길이와 발신량 추출 및 처리
        for item in json_data:
            name = item.get("name")
            message_text = item.get("text")

            if name and message_text:
                message_length = len(message_text)
                if name in user_message_lengths:
                    user_message_lengths[name] += message_length
                    user_message_counts[name] += 1
                else:
                    user_message_lengths[name] = message_length
                    user_message_counts[name] = 1

    # 도넛 차트 데이터 생성
    labels = list(user_message_lengths.keys())
    sizes = list(user_message_lengths.values())
    counts = list(user_message_counts.values())
    labels_sizes = [f"{label} ({size})" for label, size in zip(labels, sizes)]
    labels_counts = [f"{label} ({count})" for label, count in zip(labels, counts)]
    plt.suptitle(group_name + " 메세지 전송량", fontsize=16, fontproperties=fontprop)

    # 도넛 차트 그리기
    plt.subplot(1, 2, 1)
    plt.pie(sizes, labels=labels_sizes, autopct="%1.1f%%", startangle=90, textprops={'fontproperties': fontprop}, radius=2)
    plt.title(ChartTitle + " 글자 수", fontproperties=fontprop)
    plt.axis("equal")

    plt.subplot(1, 2, 2)
    plt.pie(counts, labels=labels_counts, autopct="%1.1f%%", startangle=90, textprops={'fontproperties': fontprop}, radius=2)
    plt.title(ChartTitle + " 발송 건 수", fontproperties=fontprop)
    plt.axis("equal")

    plt.subplots_adjust(left=0.05, right=0.95, wspace=0.5)

    plt.tight_layout()

    # 결과 폴더가 없다면 생성
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # 이미지로 저장
    plt.savefig(result_folder + ChartTitle + " " + group_name + ' 메세지 전송량.png', bbox_inches='tight')

    plt.show()
