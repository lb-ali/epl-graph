# from requests.models import default_hooks
# from scraping import scrape
import time
import json
import random


def load_obj(name):
    with open('obj/' + name + '.json', 'r') as f:
        return json.load(f)


def BFS(pred, dist, edge_dict, start, end):
    # Queue of players to scan adjacency list
    queue = []
    # Store if each player has been visited
    visited = {}

    # Initially all players are unvisited
    for player in edge_dict:
        visited[player] = False
        dist[player] = 1000000
        pred[player] = None

    # Now visit start
    visited[start] = True
    dist[start] = 0
    queue.append(start)

    # BFS algorithm
    while(len(queue) != 0):
        # for _ in range(5):
        # Start from front of queue, pop this off queue
        # print(queue)
        u = queue[0]
        queue.pop(0)
        # Iterate through adjacent edges
        for i in range(len(edge_dict[u])):
            # print(edge_dict[start][i])
            if(visited[edge_dict[u][i][0]] == False):
                # print(edge_dict[start][i][0])
                # Mark as visited, mark distance and predecessor
                visited[edge_dict[u][i][0]] = True
                dist[edge_dict[u][i][0]] = dist[u] + 1
                pred[edge_dict[u][i][0]] = u
                queue.append(edge_dict[u][i][0])
                # Stop once we hit destination
                if(edge_dict[u][i][0] == end):
                    # print(dist[edge_dict[u][i][0]])
                    # print("Found")
                    return True
    return False


def shortestPath(edge_dict, start, end):
    # Store path distance
    dist = {}
    # Store predecessor
    pred = {}
    if(BFS(pred, dist, edge_dict, start, end) == False):
        print("No connection")

    path = []
    crawl = end
    path.append(crawl)

    while(pred[crawl] != None):
        path.append(pred[crawl])
        crawl = pred[crawl]

    # Print path
    for i in range(1, len(path)):
        # Find details for each connection
        connection = ""
        for j in range(len(edge_dict[path[i-1]])):
            if(edge_dict[path[i-1]][j][0] == path[i]):
                connection = edge_dict[path[i-1]][j][1]
            # else:
                # print(edge_dict[path[i-1]][j])
        print(path[i-1] + ", " + path[i] + ", " + connection)

    return(len(path))


# player_dict, edge_dict = scrape()
player_dict = load_obj('player_dict')
edge_dict = load_obj('edge_dict')
print(len(edge_dict))
for i in range(500):
    start = random.choice(list(player_dict.values()))[0]
    end = random.choice(list(player_dict.values()))[0]
    print(start, end)
    length = shortestPath(edge_dict, start, end)
    if(length > 4):
        break
# shortestPath(edge_dict, "Dennis Bergkamp", "James Justin")
t3 = time.time()
# print(edge_dict["Willian"])
