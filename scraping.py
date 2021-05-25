import requests
import re
import html2text
import time
from bs4 import BeautifulSoup
import pickle


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

# Find teams in a league to scrape


def find_teams(find):
    years = {}
    # t1 = time.time()
    for y in range(1, len(find)):
        l = []
        url = "https://www.worldfootball.net/players/eng-premier-league-" + \
            find[y-1] + "-" + find[y] + "/"
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, features='lxml')
        # soup = soup.get_text().split("\n")
        soup = soup.select("a[href*=teams]")
        for s in soup:
            # print(type(s))
            if "Squad" in s.text:
                l.append(s['href'])
                # print(s['href'])
        # print(soup)
        years[find[y]] = l
    return years


def scrape(years):
    player_dict = {}
    edge_dict = {}
    for year in years:
        teams = years[year]
        for team in teams:
            t1 = time.time()
            url = "https://www.worldfootball.net" + team
            r = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, features='lxml')
            soup = soup.get_text().split("\n")
            # print(len(soup))
            check = False
            groups = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
            group = ""
            player = []
            players = []
            names = []
            for line in soup:
                # Start adding players and/or change group
                if any(g in line for g in groups):
                    group = line
                    check = True
                # Stop at manager
                if "Manager" in line or "Coach" in line:
                    check = False
                # Finish player list after adding date of birth
                if (len(player) >= 2 and "/" in line):
                    player.append(line)
                    player.append(group)
                    players.append(player)
                    # print(player)
                    player = []
                elif check and line.strip() and not any(g in line for g in groups):
                    player.append(line)

                # print(line)

            for player in players:
                # Move name to first position
                if any(char.isdigit() for char in player[0]):
                    name = player[1]
                    player[1] = player[0]
                    player[0] = name
                else:
                    name = player[0]
                # Add players to hash table
                names.append(name)
                player_dict[name] = player
                # print(player_dict.get(hash(name[0])))
                # print(name)

            # Add edges for all players on this team
            for edge1 in names:
                # Empty list of edges to add for each player
                edges_to_add = []
                for edge2 in names:
                    # If not looking at itself
                    if not edge2 == edge1:
                        # Add edge to list
                        edges_to_add.append(edge2)
                        # print(key, player_dict[key])
                for edge2 in edges_to_add:
                    # Add edge1, edge2 to edge1
                    if edge1 in edge_dict:
                        edge_dict[edge1].append([edge2, team + " " + year])
                    else:
                        # Create edge bucket if it doesn't exist
                        edge_dict[edge1] = []
                        edge_dict[edge1].append([edge2, team + " " + year])
                    # Add edge2, edge1 to edge2
                    if edge2 in edge_dict:
                        edge_dict[edge2].append([edge1, team + " " + year])
                    else:
                        # Create edge bucket if it doesn't exist
                        edge_dict[edge2] = []
                        edge_dict[edge2].append([edge1, team + " " + year])

    p = "Willian"
    # print(p, player_dict[p], edge_dict[p])
    # print(time.time() - t1)
    # print(len(edge_dict))
    # print(len(player_dict))

    # Change player list to dictionary so that name can be found
    # Hash by name
    # Store edges as edge1: (edge2, details)
    # Build database of v and e
    save_obj(edge_dict, 'edge_dict')
    # print(edge_dict)
    save_obj(player_dict, 'player_dict')
    # return player_dict, edge_dict


# teams = ['arsenal-fc', 'chelsea-fc', 'manchester-united', 'leicester-city']
years = {'2018': ['arsenal-fc', 'chelsea-fc', 'manchester-united', 'leicester-city'],
         '2019': ['arsenal-fc', 'chelsea-fc', 'manchester-united', 'leicester-city'],
         '2020': ['arsenal-fc', 'chelsea-fc', 'manchester-united', 'leicester-city'],
         '2021': ['arsenal-fc', 'chelsea-fc', 'manchester-united', 'leicester-city']}

# scrape(years)
find = ['2011', '2012', '2013', '2014', '2015',
        '2016', '2017', '2018', '2019', '2020', '2021']
# for i in range()
years2 = find_teams(find)
# print(years2)

scrape(years2)
# print(edge_dict)
