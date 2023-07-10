import json
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os


def run(font_path, group_name, result_folder):
    start_date = input("YYYYMM: ")
    if start_date == "all":
        start_date = ""
        ChartTitle = "모든 기간"
    else:
        start_year = start_date[:4]
        start_month = start_date[4:]
        ChartTitle = start_year + "년 " + start_month + "월"

    # 입력 파일 경로
    input_file = fr".\src\data{start_date}.json"

    # 폰트 설정
    fontprop = fm.FontProperties(fname=font_path)

    # JSON 파일 읽기
    with open(input_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # 사용자별 메시지 추출
    user_messages = {}
    for item in json_data:
        name = item.get("name")
        message_text = item.get("text")
        if name and message_text:
            if name in user_messages:
                user_messages[name].append(message_text)
            else:
                user_messages[name] = [message_text]

    # 특수 문자 및 제외할 단어 목록
    special_chars = r"[^\w\s]"
    exclude_words = ["type", "text", "link"]

    # 유저별 가장 많이 사용하는 단어 추출
    user_top_words = {}
    for user, messages in user_messages.items():
        words = []
        for message in messages:
            cleaned_message = re.sub(special_chars, "", str(message).lower())
            words.extend(cleaned_message.split())
        word_counts = Counter(words)
        for word in exclude_words:
            if word in word_counts:
                del word_counts[word]
        top_words = word_counts.most_common(100)
        user_top_words[user] = top_words

    # 워드 클라우드 생성 및 표시
    num_users = len(user_top_words)
    num_cols = 3  # 한 행에 그려질 그래프의 개수
    num_rows = (num_users - 1) // num_cols + 1
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 8))
    fig.suptitle(ChartTitle + " " + group_name + ' 자주 하는 말(필터 OFF)(개인)', fontsize=16, fontproperties=fontprop)
    for i, (user, top_words) in enumerate(user_top_words.items()):
        wordcloud = WordCloud(
            background_color="white",
            font_path=font_path,
            width=800,
            height=600
        ).generate_from_frequencies(dict(top_words))
        ax = axs[i // num_cols, i % num_cols]
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.set_title(f"Word Cloud for {user}", fontproperties=fontprop)
        ax.axis("off")
    # 빈 자리에 그래프가 그려지지 않도록 설정
    for i in range(len(user_top_words), num_rows * num_cols):
        ax = axs[i // num_cols, i % num_cols]
        ax.axis("off")
    plt.tight_layout()

    # 결과 폴더가 없다면 생성
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # 이미지로 저장
    plt.savefig(result_folder + ChartTitle + " " + group_name + ' 자주 하는 말(필터 OFF)(개인).png', bbox_inches='tight')

    plt.show()
