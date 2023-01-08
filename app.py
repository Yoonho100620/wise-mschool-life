from flask import Flask, json, request, jsonify
import sys
import requests
import datetime
from bs4 import BeautifulSoup


app = Flask(__name__)

dicSchool = {
  "이현중": "772",
  "서원중": "749",
  "소현중": "779",
  "정평중": "773",
  "홍천중": "1191",
  "상현중": "1183",
  "성복중": "746",
# "수지중" : "없음",
  "문정중": "778",
  "성서중": "774",
  "손곡중": "1185",
  "신봉중": "752",
  "구갈중": "765",
  "죽전중": "781"
  # 아직 추가못한 중학교는 토요일마다 5개씩 업데이트 하기
}

# -------------------------------------------------------------------------------------------------
# 급식 메뉴를 찾는 함수
# -------------------------------------------------------------------------------------------------
def find(date,schoolName):
  if schoolName in dicSchool:
    meal = requests.get(
      "https://www.wahschool.com/school/meal/view.htm?seq={}&searchDate={}&pageNo=1&scale=12"
      .format(dicSchool[schoolName], date))
    meal.text

    meal1 = BeautifulSoup(meal.content, "html.parser")
    menus = meal1.select_one('td.l_align')
    for br in menus.find_all("br") :
        br.replace_with("\n")
        
    print(menus)
    return menus.get_text()
  else:
    return "지원하지 않거나 오타가 있습니다."

# -------------------------------------------------------------------------------------------------
# 시작 이벤트 함수
# -------------------------------------------------------------------------------------------------
@app.route('/findLunch', methods=['POST'])
def findLunch():
    content = request.get_json()
    content = content['userRequest']['utterance']
    content=content.replace("\n","")
    print(content)
    splitContent = content.split(" ")    
    key = splitContent[0]
    value = splitContent[1]
    
    #주말이라면 "급식이 없습니다" 출력 , 아니라면 급식정보 출력
    
    if datetime.datetime.today().weekday() > 4:
        weekend = (datetime.datetime.today().weekday()) - 4
        now = datetime.datetime.now().date() - datetime.timedelta(days=weekend)
        
        if value == u"급식" :
            dataSend = {
                "version" : "2.0",
                "template" : {
                    "outputs" : [
                        {
                            "simpleText" : {
                                "text" : "급식이 없습니다."
                            }
                        }
                    ]
                }
            } 
    else:
        
        now = str(datetime.datetime.now().date())
        now = now.replace("-", "")
        print(now)
        # 급식 정보 
        if value == u"급식" :
            dataSend = {
                "version" : "2.0",
                "template" : {
                    "outputs" : [
                        {
                            "simpleText" : {
                                "text" : str(find(now, key))
                            }
                        }
                    ]
                }
            } 
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
