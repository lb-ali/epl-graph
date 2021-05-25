import requests
import re
import html2text
import time
from bs4 import BeautifulSoup

teams = ['arsenal-fc', 'chelsea-fc', 'manchester-united', 'leicester-city']
years = ['2019', '2020', '2021']
player_dict = {}
for year in years:
    for team in teams:
        t1 = time.time()
        url = "https://www.worldfootball.net/teams/" + team + "/" + year + "/2/"
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

        for edge1 in names:
            # Empty list of edges to add for each player
            edges_to_add = []
            for edge2 in names:
                # If not looking at itself
                if not edge2 == edge1:
                    # Add edge to list
                    edges_to_add.append(edge2)
                    # print(key, player_dict[key])
            processed_edges = []
            # Process each edge to add
            for edge2 in edges_to_add:
                processed_edges.append([edge1, edge2, team + " " + year])
            # Add processed edges to player's hash
            player_dict[edge1].append(processed_edges)

        # for k in player_dict:
            # print("\n")
print("Pedro", player_dict["Pedro"])
# print(time.time() - t1)

# Change player list to dictionary so that name can be found
# Hash by name
# Store edges as (hash1, hash2, details)
# Build database of v and e
