import json
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os


def run(input_file, group_name, font_path, result_folder):
    ChartTitle = group_name + " 월별 전송량 변화 추이"

    # 폰트 설정
    fontprop = fm.FontProperties(fname=font_path)

    # JSON 파일 읽기
    with open(input_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # 사용자 목록 추출
    user_list = list(set(item.get("name") for item in json_data if item.get("name")))

    # 그래프 영역 설정
    num_users = len(user_list)
    num_cols = 3  # 한 줄에 표시할 그래프의 수
    num_rows = (num_users + num_cols - 1) // num_cols  # 필요한 행의 수
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(24, 4 * num_rows), sharex=True)
    fig.suptitle(ChartTitle, fontsize=16, fontproperties=fontprop)

    # 각 사용자별 월별 메시지 전송량 추이 그래프 그리기
    for i, target_user in enumerate(user_list):
        target_name = target_user
        row = i // num_cols  # 현재 그래프의 행 인덱스
        col = i % num_cols  # 현재 그래프의 열 인덱스

        # 사용자별 발신 시간 추출 및 처리
        user_sent_counts = {}
        for item in json_data:
            name = item.get("name")
            date_str = item.get("date")
            if name and date_str:
                sent_time = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                if name == target_user:
                    year_month = sent_time.strftime("%Y-%m")
                    if year_month in user_sent_counts:
                        user_sent_counts[year_month] += 1
                    else:
                        user_sent_counts[year_month] = 1

        # 월별 메시지 전송량 추이 그래프 그리기
        x = sorted(user_sent_counts.keys())
        y = [user_sent_counts[key] for key in x]

        # 각 사용자별 그래프 그리기
        ax = axes[row, col]
        ax.plot(x, y, marker="o")
        ax.set_xlabel("Month", fontproperties=fontprop)
        ax.set_ylabel("Message Count", fontproperties=fontprop)
        ax.set_title(f"Message Count Trend for {target_name}", fontproperties=fontprop)
        ax.set_xticks(range(len(x)))
        ax.set_xticklabels(x, rotation=45, ha="right")

    # 빈 그래프 영역 제거
    if num_users % num_cols != 0:
        for i in range(num_users, num_rows * num_cols):
            row = i // num_cols
            col = i % num_cols
            fig.delaxes(axes[row, col])

    # 그래프 간 간격 조정
    plt.subplots_adjust(left=0.05, right=0.95, hspace=0.5, wspace=0.3)

    # 결과 폴더가 없다면 생성
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # 이미지로 저장
    plt.savefig(result_folder + ChartTitle + '.png')

    # 모든 그래프 표시
    plt.show()
