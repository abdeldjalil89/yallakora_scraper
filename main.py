import csv
from bs4 import BeautifulSoup
import requests

date = input("please enter a Date in the following format:MM/DD/YYYY ")
page = requests.get(f"https://www.yallakora.com/matches-center?date={date}")

matches_details = []


def get_match_info(championship):
  championship_title = (
      championship.contents[1].find("h2").text.strip()
      if len(championship.contents) > 1
      and championship.contents[1].find("h2")
      else "دوري"
  )
  all_matchs = championship.find_all("div", {"class": "item"})
  number_of_matches = len(all_matchs)

  for i in range(number_of_matches):
    # استخراج الفريق الأول بحماية
    team_A_elm = all_matchs[i].find("div", {"class": "teamA"})
    if team_A_elm and team_A_elm.find("p"):
      team_A = team_A_elm.find("p").text.strip()
    else:
      team_A = ""

    # استخراج الفريق الثاني بحماية
    team_B_elm = all_matchs[i].find("div", {"class": "teamB"})
    if team_B_elm and team_B_elm.find("p"):
      team_B = team_B_elm.find("p").text.strip()
    else:
      team_B = ""

    # استخراج النتيجة ووقت المباراة بحماية كاملة ضد الأخطاء
    mres_div = all_matchs[i].find("div", {"class": "MResult"})
    if mres_div:
      metch_result = mres_div.find_all("span", {"class": "score"})
      if len(metch_result) >= 2:
        score = f"{metch_result[0].text.strip()} - {metch_result[1].text.strip()}"
      else:
        score = "لم تبدأ"

      time_elem = mres_div.find("span", {"class": "time"})
      match_time = time_elem.text.strip() if time_elem else ""
    else:
      score = "غير متوفر"
      match_time = ""

    matches_details.append({
        "نوع البطولة": championship_title,
        "فريق الاول": team_A,
        "فريق الثاني": team_B,
        "وقت المبارات": match_time,
        "نتيجه": score,
    })


def main(page):
  src = page.content
  soup = BeautifulSoup(src, "lxml")

  championships = soup.find_all("div", {"class": "matchesList"})

  for i in range(len(championships)):
    get_match_info(championships[i])

  if len(matches_details) > 0:
    keys = matches_details[0].keys()
    with open(
        r"c:\Users\Abdeldjalil\Documents\yallakora\matches-details.csv",
        "w",
        encoding="utf-8-sig",
    ) as output_file:
      dict_writer = csv.DictWriter(output_file, keys)
      dict_writer.writeheader()
      dict_writer.writerows(matches_details)
    print("file created!")
  else:
    print("لم يتم العثور على مباريات في هذا التاريخ!")


main(page)
