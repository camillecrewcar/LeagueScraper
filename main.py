import requests
from bs4 import BeautifulSoup
import json

base_url = "https://probuilds.net/champions"
site_url = "https://probuilds.net"

def get_html(url):
    response = requests.get(url)
    return response.text

def get_champion_links(base_url, site_url):
    html = get_html(base_url)
    soup = BeautifulSoup(html, 'html.parser')
    champions = {}

    # Adjust the selector based on the actual HTML structure
    champion_elements = soup.find_all('a', class_='item-link')

    for element in champion_elements:
        link = site_url + element['href']
        name = element.find('span', class_='title type-subtitle--bold').text.strip()
        champions[name] = link

    return champions

champion_links = get_champion_links(base_url, site_url)

# Print the dictionary of champion names and links
for champion, link in champion_links.items():
    print(f"{champion}: {link}")

# Save to JSON file
with open('champion_links.json', 'w') as json_file:
    json.dump(champion_links, json_file, indent=4)



def get_html(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for bad status codes
    return response.text


def get_champion_role(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    meta_details = soup.find('p', {'data-testid': 'meta-details'})
    if meta_details:
        roles = meta_details.text.strip()
        return roles.split(' / ')
    return []


def parse_champion_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = {}

    champ_title = soup.find('h1', {'class': 'champTitle'})
    if champ_title:
        data['name'] = champ_title.text.strip().split()[0]
    else:
        data['name'] = "Unknown"

    stats = {}
    stat_labels = {
        'lbl_stat_hp': 'Health',
        'lbl_stat_hpPerLevel': 'Health_per_level',
        'lbl_stat_hpRegen': 'Health_Regen',
        'lbl_stat_hpRegenPerLevel': 'Health_Regen_per_level',
        'lbl_stat_mp': 'Mana',
        'lbl_stat_mpPerLevel': 'Mana_per_level',
        'lbl_stat_mpRegen': 'Mana_Regen',
        'lbl_stat_mpRegenPerLevel': 'Mana_Regen_per_level',
        'lbl_stat_dmg': 'Attack_Damage',
        'lbl_stat_dmgPerLevel': 'Attack_Damage_per_level',
        'lbl_stat_aspeed': 'Attack_Speed',
        'lbl_stat_aspeedPerLevel': 'Attack_Speed_per_level',
        'lbl_stat_armor': 'Armor',
        'lbl_stat_armorPerLevel': 'Armor_per_level',
        'lbl_stat_mr': 'Magic_Resist',
        'lbl_stat_mrPerLevel': 'Magic_Resist_per_level',
        'lbl_stat_moveSpeed': 'Movement_Speed'
    }

    for stat_id, label in stat_labels.items():
        stat_element = soup.find(id=stat_id)
        if stat_element:
            stat_value = stat_element.text.strip()
            try:
                stat_value = int(stat_value)
            except ValueError:
                try:
                    stat_value = float(stat_value)
                except ValueError:
                    pass
            stats[label] = stat_value

    data['stats'] = stats
    return data


def parse_champion_statistics(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_elems = soup.findAll('span', {'class': '_dxv0e1'})

    win_rate = pick_rate = ban_rate = num_games = kda = "N/A"

    for elem in all_elems:
        strong_elem = elem.find('strong')
        if strong_elem:
            if strong_elem.text.strip() == 'Win':
                win_rate = elem.find_next('span').text.strip()
            elif strong_elem.text.strip() == 'Pick':
                pick_rate = elem.find_next('span').text.strip()
            elif strong_elem.text.strip() == 'Ban':
                ban_rate = elem.find_next('span').text.strip()
            elif strong_elem.text.strip() == 'Games:':
                num_games = elem.find_next('span').text.strip()
            elif strong_elem.text.strip() == 'KDA:':
                kda = elem.find_next('span').text.strip()

    return {
        "Win_Rate": win_rate,
        "Pick_Rate": pick_rate,
        "Ban_Rate": ban_rate,
        "Number_of_Games": num_games,
        "KDA": kda,
    }


champions = [
    "Aatrox", "Ahri", "Akali", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe",
    "Aurelionsol", "Azir", "Bard", "Blitzcrank", "Brand", "Braum", "Caitlyn", "Camille",
    "Cassiopeia", "ChoGath", "Corki", "Darius", "Diana", "DrMundo", "Draven", "Ekko",
    "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank",
    "Garen", "Gnar", "Gragas", "Graves", "Hecarim", "Heimerdinger", "Illaoi", "Irelia",
    "Ivern", "Janna", "JarvanIV", "Jax", "Jayce", "Jhin", "Jinx", "KaiSa", "Kalista",
    "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "KhaZix",
    "Kindred", "Kled", "KogMaw", "LeBlanc", "LeeSin", "Leona", "Lillia", "Lissandra",
    "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "MasterYi", "MissFortune",
    "Mordekaiser", "Morgana", "Nami", "Nasus", "Nautilus", "Neeko", "Nidalee", "Nocturne",
    "Nunu", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana",
    "Quinn", "Rakan", "Rammus", "RekSai", "Rell", "Renekton", "Rengar", "Riven", "Rumble",
    "Ryze", "Samira", "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana",
    "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka", "Swain", "Sylas", "Syndra",
    "TahmKench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle",
    "Tryndamere", "TwistedFate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar",
    "VelKoz", "Vi", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah",
    "Xerath", "XinZhao", "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Ziggs",
    "Zilean", "Zoe", "Zyra"
]
championsForLolSite = [
    "Aatrox", "Ahri", "Akali", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe",
    "Aurelion-sol", "Azir", "Bard", "Blitzcrank", "Brand", "Braum", "Caitlyn", "Camille",
    "Cassiopeia", "Cho-Gath", "Corki", "Darius", "Diana", "Dr-Mundo", "Draven", "Ekko",
    "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank",
    "Garen", "Gnar", "Gragas", "Graves", "Hecarim", "Heimerdinger", "Illaoi", "Irelia",
    "Ivern", "Janna", "Jarvan-IV", "Jax", "Jayce", "Jhin", "Jinx", "Kai-Sa", "Kalista",
    "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "Kha-Zix",
    "Kindred", "Kled", "Kog-Maw", "LeBlanc", "Lee-Sin", "Leona", "Lillia", "Lissandra",
    "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "Master-Yi", "Miss-Fortune",
    "Mordekaiser", "Morgana", "Nami", "Nasus", "Nautilus", "Neeko", "Nidalee", "Nocturne",
    "Nunu", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana",
    "Quinn", "Rakan", "Rammus", "Rek-Sai", "Rell", "Renekton", "Rengar", "Riven", "Rumble",
    "Ryze", "Samira", "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana",
    "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka", "Swain", "Sylas", "Syndra",
    "Tahm-Kench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle",
    "Tryndamere", "Twisted-Fate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar",
    "Vel-Koz", "Vi", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah",
    "Xerath", "Xin-Zhao", "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Ziggs",
    "Zilean", "Zoe", "Zyra"
]

champion_data_list = []
role_dict = {}

for i, champ in enumerate(champions):
    try:
        # Get champion abilities and stats
        url = 'https://www.lolrift.com/champions/' + champ + '/abilities'
        html = get_html(url)
        champion_data = parse_champion_data(html)

        # Get champion roles using championsForLolSite
        base_url = "https://www.leagueoflegends.com/en-gb/champions/"
        champ_url = f"{base_url}{championsForLolSite[i].lower()}/"
        roles = get_champion_role(champ_url)
        champion_data['roles'] = roles

        # Organize roles into the role_dict
        for role in roles:
            if role not in role_dict:
                role_dict[role] = []
            role_dict[role].append(champion_data['name'])

        # Get champion statistics
        stats_url = "https://www.metasrc.com/lol/build/" + champ
        stats_html = get_html(stats_url)
        champion_data['data'] = parse_champion_statistics(stats_html)

        champion_data_list.append(champion_data)
    except Exception as e:
        print(f"Failed to process champion {champ}: {e}")

# Write champion data to JSON file
with open('champion_data.json', 'w') as json_file:
    json.dump(champion_data_list, json_file, indent=4)

# Write role data to JSON file
with open('role_data.json', 'w') as json_file:
    json.dump(role_dict, json_file, indent=4)

print("Champion data has been saved to champion_data.json")
print("Role data has been saved to role_data.json")
