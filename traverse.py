from requests.models import default_hooks
from scraping import scrape


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
                    print(dist[edge_dict[u][i][0]])
                    print("Found")
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

    for i in range(len(path)):
        print(path[i])


player_dict, edge_dict = scrape()
print(len(player_dict))
shortestPath(edge_dict, "Hakim Ziyech", "Bukayo Saka")
# print(edge_dict["Willian"])
