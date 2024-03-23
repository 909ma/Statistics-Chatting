import re
import os
import json
from collections import Counter
from konlpy.tag import Hannanum
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


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

    # 모든 사용자의 메시지 추출
    all_messages = []
    for item in json_data:
        message_text = item.get("text")
        if message_text:
            all_messages.append(message_text)

    # 특수 문자 및 제외할 단어 목록
    special_chars = r"[^\w\s]"
    exclude_words = ["type", "text", "link"]

    # 형태소 분석기 초기화
    hannanum = Hannanum()

    # 모든 사용자의 가장 많이 사용하는 단어 추출
    words = []
    for message in all_messages:
        if isinstance(message, str):
            try:
                # 문자열 디코딩
                decoded_message = message.decode('utf-8')
            except AttributeError:
                decoded_message = message
            # 정규식을 사용하여 반복되는 문자 제거 후 형태소 분석을 통해 명사만 추출
            cleaned_message = re.sub(r'(.)\1{2,}', r'\1', decoded_message)  # 2번 이상 반복되는 문자를 1번으로 줄임
            nouns = hannanum.nouns(cleaned_message)
            words.extend(nouns)
    word_counts = Counter(words)
    for word in exclude_words:
        if word in word_counts:
            del word_counts[word]
    top_words = word_counts.most_common(100)

    # 워드 클라우드 생성 및 표시
    wordcloud = WordCloud(
        background_color="white",
        font_path=font_path,
        width=800,
        height=600
    ).generate_from_frequencies(dict(top_words))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.suptitle(ChartTitle + " " + group_name + ' 자주 하는 말(필터 ON)(단체)', fontsize=16, fontproperties=fontprop)
    plt.axis("off")
    plt.tight_layout()

    # 결과 폴더가 없다면 생성
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # 이미지로 저장
    plt.savefig(result_folder + ChartTitle + " " + group_name + ' 자주 하는 말(필터 ON)(단체).png', bbox_inches='tight')

    plt.show()