import json
from datetime import datetime

class Achievement:
   file_path='achievements.json'

   def __init__(self):
      self.achievements={
         "ACH_single_win": {
            "icon":None,
            "name":"싱글 플레이어 대전에서 승리",
            "description":"싱글 플레이어 대전에서 승리하여 업적 달성!",
            "achievement":False,
            "date":None
         },
         "ACH_story_win" : {
            "icon":None,
            "name":"컴퓨터는 내 상대가 안돼!",
            "description":"모든 스토리 모드 대전에서 승리하여 업적 달성!",
            "achievement":{
               "regionA":False,
               "regionB":False,
               "regionC":False,
               "regionD":False
            },
            "date":None
         },
         "ACH_10turn_win":{
            "icon":None,
            "name":"너무 쉬운데?",
            "description":"싱글 플레이어 대전에서 10턴 안에 승리하여 업적 달성!",
            "achievement":False,
            "date":None
         },
         "ACH_noskill_win":{
            "icon":None,
            "name":"핸디캡 줘도 이기네ㅋ",
            "description":"기술 카드를 단 한 번도 사용하지 않고 승리하여 업적 달성!",
            "achievement":False,
            "date":None
         },
         "ACH_swap_win":{
            "icon":None,
            "name":"이걸 역전하네?!",
            "description":"다른 플레이어가 UNO를 선언한 뒤에 승리하여 업적 달성!",
            "achievement":False,
            "date":None
         },
         "ACH_swap_lose":{
            "icon":None,
            "name":"이걸 역전당하네..",
            "description":"내가 UNO를 선언한 뒤에 패배하여 업적 달성!",
            "achievement":False,
            "date":None
         },
         "ACH_single10_win":{
            "icon":None,
            "name":"UNO게임 마스터",
            "description":"싱글 플레이어 대전에서 10번 승리하여 업적 달성!",
            "achievement":False,
            "date":None,
            "cnt":0 #승리 횟수
         },
         "ACH_uno_cnt":{
            "icon":None,
            "name":"순발력 좋은데?",
            "description":"상대보다 UNO 먼저 선언한 횟수",
            "achievement":False,
            "date":None,
            "cnt":0 #UNO 선언 횟수
         }
      }

      self.selected_achievements = {}

      for key,value in self.achievements.items():
            for k in value.keys():
               if k=="achievement":
                  self.selected_achievements[key]={k:value[k]}
               elif k=="date":
                  self.selected_achievements[key][k]=value[k]
               elif k=="cnt":
                  self.selected_achievements[key][k]=value[k]
               else:
                  pass
      

   def save(self):
      with open(self.file_path, 'w') as f:
         json.dump(self.selected_achievements, f)

   def load(self):
      with open(self.file_path, 'r') as f:
         self.selected_achievements = json.load(f)

      for key, value in self.selected_achievements.items(): #불러온 json파일이 반영된 결과인 seleceted_achievements를 achievements에 반영
         for k in value.keys():
            self.achievements[key][k]=value[k]

   def init(self):
      self.selectec_achievements={
         "ACH_single_win": {
            "achievement":False,
            "date":None
         },
         "ACH_story_win" : {
            "achievement":{
               "regionA":False,
               "regionB":False,
               "regionC":False,
               "regionD":False
            },
            "date":None
         },
         "ACH_10turn_win":{
            "achievement":False,
            "date":None
         },
         "ACH_noskill_win":{
            "achievement":False,
            "date":None
         },
         "ACH_swap_win":{
            "achievement":False,
            "date":None
         },
         "ACH_swap_lose":{
            "achievement":False,
            "date":None
         },
         "ACH_single10_win":{
            "achievement":False,
            "date":None,
            "cnt":0 #승리 횟수
         },
         "ACH_uno_cnt":{
            "achievement":False,
            "date":None,
            "cnt":0 #UNO 선언 횟수
         }
      }
   def clear(self):
      self.init() #selecetd_achievements dict 값들이 바뀜
      self.save() #그 바뀐 값들을 json에 저장
      self.load() #그 바뀐 json을 achievements에 반영

   
ach=Achievement()
ach.load()
print(ach.achievements)