import requests
from bs4 import BeautifulSoup
import re

# 位置情報からその日の天気を返す
def get_weather_from_location(original_location):
  # 住所の中から郵便番号を抽出する
  location = re.findall('\d{3}-\d{4}', original_location)
  # 1回目のスクレイピングでは住所を検索し、候補から取ってくる
  url = "https://weather.yahoo.co.jp/weather/search/?p=" + location[0]
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  content = soup.find(class_="serch-table")
  # 2回目のスクレイピングで用いるURLを得る
  location_url = "http:" + content.find('a').get('href')
  r = requests.get(location_url)
  soup = BeautifulSoup(r.text, 'html.parser')
  content = soup.find(id='yjw_pinpoint_today').find_all('td')
  info = []

  for each in content[1:]:
    info.append(each.get_text().strip('\n'))
  
  # 時間
  time = info[:8]
  # 天気
  weather = info[9:17]
  # 気温
  temperature = info[18:26]
  # 上の3つの情報を合わせる
  weather_info = [(time[i], weather[i], temperature[i]) for i in range(8)]

  result = [('{0[0]}: {0[1]}, {0[2]}°C'.format(weather_info[i])) for i in range(8)]
  result = ('{}\nの今日の天気は\n'.format(original_location) + '\n'.join(result) + '\nです。')

  return result
