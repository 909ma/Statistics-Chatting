import json
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os


def run(font_path, group_name, result_folder):
    # 시작 날짜와 끝 날짜 입력
    start_date = input("YYYYMM: ")
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

    # 메시지 추출
    messages = []
    for item in json_data:
        message_text = item.get("text")
        if message_text:
            messages.append(message_text)

    # 특수 문자 및 제외할 단어 목록
    special_chars = r"[^\w\s]"
    exclude_words = ["type", "text", "link"]

    # 단어 빈도수 계산
    words = []
    for message in messages:
        cleaned_message = re.sub(special_chars, "", str(message).lower())
        words.extend(cleaned_message.split())
    word_counts = Counter(words)
    for word in exclude_words:
        if word in word_counts:
            del word_counts[word]
    top_words = word_counts.most_common(100)

    # 워드 클라우드 생성
    wordcloud = WordCloud(
        background_color="white",
        font_path=font_path,
        width=800,
        height=600
    ).generate_from_frequencies(dict(top_words))

    # 워드 클라우드 표시
    plt.figure(figsize=(8, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.suptitle(ChartTitle + " " + group_name + ' 자주 하는 말(필터 OFF)(단체)', fontsize=16, fontproperties=fontprop)
    plt.axis("off")
    plt.tight_layout()

    # 결과 폴더가 없다면 생성
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # 이미지로 저장
    plt.savefig(result_folder + ChartTitle + " " + group_name + ' 자주 하는 말(필터 OFF)(단체).png', bbox_inches='tight')

    plt.show()
