import json
import json_extraction
import json_extraction2
import json_extraction_kakaoPC1
import json_extraction_kakaoPC2
import json_extraction_kakaoMobile1
import json_extraction_kakaoMobile2



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
        print("21. 카카오톡 PC data.json 추출")
        print("22. 카카오톡 PC dataYYYYMM.json 추출")
        print("31. 카카오톡 Mobile data.json 추출")
        print("32. 카카오톡 Mobile dataYYYYMM.json 추출")
        print("0. 종료")
        choice = input("원하는 기능을 선택하세요: ")

        if choice == "11":
            json_extraction.run(config_data['input_file'], config_data['output_file'])
        elif choice == "12":
            json_extraction2.run(config_data['input_file'])
        elif choice == "21":
            json_extraction_kakaoPC1.run(config_data['input_file_kakao'])
        elif choice == "22":
            json_extraction_kakaoPC2.run(config_data['input_file_kakao'])
        elif choice == "31":
            json_extraction_kakaoMobile1.run(config_data['input_file_kakao'])
        elif choice == "32":
            json_extraction_kakaoMobile2.run(config_data['input_file_kakao'])
        elif choice == "0":
            break
        else:
            print("올바른 선택지를 입력하세요.")
