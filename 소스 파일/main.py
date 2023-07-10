import json
import json_extraction
import json_extraction2
import json_extraction_kakao1
import json_extraction_kakao2
import count_message2
import sending_time_message
import sending_time_message2
import traffic_sending
import trending_words_no_filtered
import trending_words_no_filtered2
import trending_words
import trending_words2



def main():
    # JSON 파일에서 데이터 읽기
    with open('config.json', "r", encoding="utf-8") as file:
        config_data = json.load(file)

    # 읽어온 데이터 사용하기
    print(config_data['input_file'])
    print(config_data['output_file'])

    while True:
        print("11. 텔레그램 data.json 추출")
        print("12. 텔레그램 dataYYYYMM.json 추출")
        print("21. 카카오톡 data.json 추출")
        print("22. 카카오톡 dataYYYYMM.json 추출")
        print("3. 메세지 전송량 변화 추이(개인)")
        print("4. 메세지 전송 시각(메세지 건 당)")
        print("5. 메세지 전송 시각(글자수 당)")
        print("6. 메세지 전송량")
        print("7. 자주 쓰는 단어(필터 OFF)(개인)")
        print("8. 자주 쓰는 단어(필터 OFF)(단체)")
        print("9. 자주 쓰는 단어(필터 ON)(개인)")
        print("10. 자주 쓰는 단어(필터 ON)(단체)")
        print("0. 종료")
        choice = input("원하는 기능을 선택하세요: ")

        if choice == "11":
            json_extraction.run(config_data['input_file'], config_data['output_file'])
        elif choice == "12":
            json_extraction2.run(config_data['input_file'])
        elif choice == "21":
            json_extraction_kakao1.run(config_data['input_file_kakao'])
        elif choice == "22":
            json_extraction_kakao2.run(config_data['input_file_kakao'])
        elif choice == "3":
            count_message2.run(config_data['output_file'], config_data['group_name'], config_data['font_path'], config_data['result_folder'])
        elif choice == "4":
            sending_time_message.run(config_data['font_path'], config_data['group_name'], config_data['result_folder'])
        elif choice == "5":
            sending_time_message2.run(config_data['font_path'], config_data['group_name'], config_data['result_folder'])
        elif choice == "6":
            traffic_sending.run(config_data['font_path'], config_data['group_name'], config_data['result_folder'])
        elif choice == "7":
            trending_words_no_filtered.run(config_data['font_path'], config_data['group_name'], config_data['result_folder'])
        elif choice == "8":
            trending_words_no_filtered2.run(config_data['font_path'], config_data['group_name'], config_data['result_folder'])
        elif choice == "9":
            trending_words.run(config_data['font_path'], config_data['group_name'], config_data['result_folder'])
        elif choice == "10":
            trending_words2.run(config_data['font_path'], config_data['group_name'], config_data['result_folder'])
        elif choice == "0":
            break
        else:
            print("올바른 선택지를 입력하세요.")


if __name__ == "__main__":
    main()
