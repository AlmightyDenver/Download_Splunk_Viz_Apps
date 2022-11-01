# Requirements

1. python3, package(selenium 4)
2. ChromeDriver(or other browser driver)

</br></br>

# Updates

## 1.1.0 ver

~~- 기존 앱 이름 _viz_ 만 다운로드 -> 앱 이름 viz|Viz|visualization|Visualization 인 앱 다운로드~~

- SplunkBase 페이지 바뀜
- splunk/developer 지원 앱 아닌 경우 warning 페이지 confirm download 추가
- Splunk selenium 4 업데이트로 코드 수정

</br>

## 1.2.0 ver

- 기존 splunkbase 페이지 html 다운로드 -> 다운로드 필요 x
- Splunkbase id, pw, 검색 키워드, 크롬드라이버 디렉토리만 필요
- 앱 이름이 검색한 키워드와 일치하는지 검사 기능 추가(대소문자 무시)

</br></br>

# How To Use

1. `python Download_Splunk__apps_120.py -i <SPLUNK_ID> -k <SEARCH_KEYWORD> -d <BROWSER_DRIVER_LOCATION>`
2. Enter SPLUNK_PW

</br>

## Command examples

`python Download_Splunk__apps_120.py -i myid -k viz -d /Users/denver/Documents/Tennis/chromedriver`
→ Download only apps that matches keyword
