import random
import math

def get_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def calculate_total_distance(cities, route):
    distance = 0
    for i in range(1, len(route)):
        distance += get_distance(cities[route[i - 1]], cities[route[i]])
    distance += get_distance(cities[route[-1]], cities[route[0]])
    return distance
# 貪欲法(start_city[0]をランダムに設定)
def greedy_solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = get_distance(cities[i], cities[j])

    best_tour = None
    best_tour_length = float('inf')
    LOOP = 100
    for i in range(LOOP):
        start_city = random.randint(0, N - 1)
        current_city = start_city
        unvisited_cities = set(range(N)) - {start_city}
        tour = [current_city]

        while unvisited_cities:
            next_city = min(unvisited_cities, key=lambda city: dist[current_city][city])
            unvisited_cities.remove(next_city)
            tour.append(next_city)
            current_city = next_city

        tour_length = calculate_total_distance(cities, tour)
        if tour_length < best_tour_length:
            best_tour_length = tour_length
            best_tour = tour

    return best_tour

# 焼きなまし
def annealing_solve(cities):
    city_length = len(cities)
    current_route = greedy_solve(cities)
    current_distance = calculate_total_distance(cities, current_route)

    LOOP = 50000
    for t in range(LOOP):
        left = random.randint(0, city_length - 1)
        right = random.randint(0, city_length - 1)
        current_route[left:right+1] = reversed(current_route[left:right+1])
        
        new_distance = calculate_total_distance(cities, current_route)
        if current_distance > new_distance:
            current_distance = new_distance
        else:
            current_route[right:left+1] = reversed(current_route[right:left+1])
    
    return current_route

# 2-opt
def two_opt(cities, tour):
    N = len(tour)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = get_distance(cities[i], cities[j])

    while True:
        count = 0
        for i in range(N-2):
            for j in range(i+2, N):
                l1 = dist[tour[i]][tour[i + 1]]
                l2 = dist[tour[j]][tour[(j + 1) % N]]
                l3 = dist[tour[i]][tour[j]]
                l4 = dist[tour[i + 1]][tour[(j + 1) % N]]
                if l1 + l2 > l3 + l4:
                    tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                    count += 1
        if count == 0:
            break
    return tour

def solve(cities):
    tour = annealing_solve(cities)
    tour = two_opt(cities, tour)
    return tour
