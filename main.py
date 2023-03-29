import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import chromedriver_binary

LINKS = [
    "https://ervelia.pl/profile/character/MrJackpot",
    "https://ervelia.pl/profile/character/MrLuckyStrike",
    "https://ervelia.pl/profile/character/Indifferent",
    "https://ervelia.pl/profile/character/Wrozeczka",
    "https://ervelia.pl/profile/character/PrendkiMarek",
    "https://ervelia.pl/profile/character/REYNOLDS",
    "https://ervelia.pl/profile/character/Kahh",
    "https://ervelia.pl/profile/character/RAIZKING",
    "https://ervelia.pl/profile/character/BECEL",
    "https://ervelia.pl/profile/character/216",
    "https://ervelia.pl/profile/character/TurboKotek"
]


def get_info(link):
    driver = webdriver.Chrome()
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all("span", {"class": "value ml-3"})
    text = ""
    guild = ""
    name = ""
    for result in results:
        result = str(result)
        if "Dowódca" not in result and "Członek" not in result and "guild" not in result:
            regex = re.search(", (.*)<", result)
            text = regex.group(1)
        if "guild" in result:
            regex = re.search('/guild/(.*)">', result)
            guild = regex.group(1)
    results = soup.find_all("h3")
    for result in results:
        result = str(result)
        if "div" not in result:
            regex = re.search(">(.*)<", result)
            name = regex.group(1)
    return name, guild, text


def get_status(last_online):
    day = last_online[:2]
    hour = last_online[-5:]
    curr_day = datetime.datetime.now().strftime("%d")
    curr_date = datetime.datetime.now()
    delta = datetime.timedelta(hours=-1)
    if curr_day != day:
        return False
    curr_date += delta
    curr_hour = curr_date.strftime("%H:%M")
    if hour < curr_hour:
        return False
    return True


def show_data():
    guilds = []
    characters = []
    is_anyone_online = False
    for link in LINKS:
        name, guild, text = get_info(link)
        if guild not in guilds:
            guilds.append(guild)
        characters.append({'name': name, 'guild': guild, 'last_online': text})

    for guild_name in guilds:
        guild_name_printed = False
        for char_info in characters:
            was_online = get_status(char_info['last_online'])
            if char_info['guild'] == guild_name and was_online:
                is_anyone_online = True
                if not guild_name_printed:
                    print(f"{guild_name}:")
                    guild_name_printed = True
                print(f"    {char_info['name']}, ostatnio online: {char_info['last_online'][-5:]}")

    if not is_anyone_online:
        print("Brak zalogowanych graczy.")


show_data()
