import random
import math

def get_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# 貪欲法
def greedy_solve(cities):
    N = len(cities)

    distance = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            distance[i][j] = distance[j][i] = get_distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: distance[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour


def annealing_solve(cities):
    city_length = len(cities)       # citiesの数
    current_route = greedy_solve(cities)        # 初期ルートの値

    def calculate_total_distance(cities, route):
        distance = 0
        # ０〜route分の距離をカウントしていく
        for i in range(1, len(route)):
            distance += get_distance(cities[route[i - 1]], cities[route[i]])
        distance += get_distance(cities[route[-1]], cities[route[0]])  # ここで一番最後の地点と最初の地点をつなぐ
        return distance
    
    current_distance = calculate_total_distance(cities, current_route)

    for t in range(10000):
        # 反転させるルートの始点、終点をランダムに決める
        left = random.randint(1, city_length - 1)
        right = random.randint(1, city_length - 1)
        # もし始点が終点を上回ってしまったら入れ替える
        if left > right:
            left, right = right, left
        # ここでルートを反転させる
        current_route[left:right+1] = reversed(current_route[left:right+1])
        new_distance = calculate_total_distance(cities, current_route)
        # new_distanceの方が短ければ値を更新する
        if current_distance >= new_distance:
            current_distance = new_distance
        else:
            current_route[left:right+1] = reversed(current_route[left:right+1])
    
    return current_route
