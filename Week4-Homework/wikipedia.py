import sys
import collections
import random
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # A mapping from the page title to a page ID (integer).
        # For example, self.title_to_id[abcd] returns an ID of the page whose
        # title is abcd.
        self.title_to_id = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.title_to_id[title] = id
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

        # あるページが他のページからリンクされている数
        self.linked_count = {}
        for id in self.titles.keys():
            self.linked_count[id] = 0
        for id in self.titles.keys():
            for dst in self.links[id]:
                self.linked_count[dst] += 1

        # あるページから他のページへリンクするノードの数
        self.link_count = {}
        for id in self.titles.keys():
            self.link_count[id] = len(self.links[id])

    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        linked_count = self.linked_count

        print("The most linked pages are:")
        linked_count_max = max(linked_count.values())
        for dst in linked_count.keys():
            if linked_count[dst] == linked_count_max:
                print(self.titles[dst], linked_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = self.title_to_id.get(start)  
        goal_id = self.title_to_id.get(goal)

        if start_id == None or goal_id == None:
            print("The page with that title does not exist.")
            return

        find_path_by_bfs = deque([start_id])    # 探索用のキュー
        visited = {}
        node = None
        visited[start_id] = node

        print("The shortest path is:")
        while find_path_by_bfs:
            node = find_path_by_bfs.popleft()
            # goalに到達したら visitedを辿って shortest_pathに追加していく
            if node == goal_id:
                shortest_path = []
                while node is not None:
                    shortest_path.append(self.titles[node])
                    node = visited[node]
                shortest_path.reverse()     # start → goal になるよう reverseする
                print(" → ".join(shortest_path))
                print()
                return
            for child in self.links[node]:
                if not child in visited:
                    visited[child] = node
                    find_path_by_bfs.append(child)
        print("Not found")
        print()

   # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        link_count = self.link_count
        all_node = len(self.titles)
        
        prev_answer = {}        # 前回の計算結果 これを元に計算する　初期値は１にしておく
        for id in self.titles.keys():
            prev_answer[id] = 1.0

        answer = {}             # 計算した答えを入れていく
        for id in self.titles.keys():
            answer[id] = 0.0

        while True:
            print("計算中")
            distribution_to_all_nodes = 0       # 全てのノードに分配するページランク

            # 最初に全てのノードに分配する ページランクの15%を計算しておく
            for all_node_id in self.titles.keys():
                distribution_to_all_nodes += prev_answer[all_node_id] * 0.15

            for id in prev_answer.keys():
                if link_count[id] != 0:     # 隣接ノードがある場合
                    distribution_to_link_nodes = (prev_answer[id] * 0.85) / link_count[id]

                    # 隣接ノードに分配する
                    for link_node_id in self.links[id]:
                        answer[link_node_id] += distribution_to_link_nodes

                else:       # 隣接ノードがない場合
                    distribution_to_all_nodes += prev_answer[id] * 0.85

            # 最初の 15%, 隣接ノードがなかった場合のページランクを全てのノードに分配
            for all_node_id in self.titles.keys():
                answer[all_node_id] += distribution_to_all_nodes / all_node

            # answer と prev_answer の全ての差が 0.01以下になれば
            # 収束したとみなし whileループを抜ける
            if all(abs(answer[id] - prev_answer[id]) <= 0.01 for id in answer.keys()):
                break

            # answer, prev_answerの初期化
            prev_answer.update(answer)      
            for id in self.titles.keys():
                answer[id] = 0.0

        print("The most popular pages are:")
        # 答えを点数順にソートし、高い方から10件をコンソールに出力する
        sorted_answers = sorted(answer.items(), key=lambda item: item[1], reverse=True)
        for id, score in sorted_answers[:10]:
            print(self.titles[id] + ":" + str(score))
        print()


    # リンクがない・リンクされていないページ
    def find_no_link_and_linked_pages(self):
        linked_count = self.linked_count
        link_count = self.link_count
        unconnected_pages = {}

        for id in self.titles.keys():
            title = self.titles[id]
            # 索引　_〇〇というページは省きます
            if not title.startswith("索引_") and linked_count[id] == 0 and link_count[id] == 0:
                unconnected_pages[id] = title


        if len(unconnected_pages) > 10:
            for i in range(10):
                print(random.choice(list(unconnected_pages.values())))
        else:
            print(list(unconnected_pages.values()))
        print("Total pages:" + str(len(unconnected_pages)))
        print()

    # target がリンクされているページの中で最も他のページにリンクされているページを返す
    def find_most_linked_pages_include_target_link(self, target):
        target_id = self.title_to_id.get(target)
        # 入力されたtitleが存在しなければエラーを返す
        if target_id is None:
            print("Target page not found")
            return

        linking_pages = {}

        for id, link in self.links.items():
            if target_id in link and self.titles[id] != "日本":
                linking_pages[id] = link

        # titleは存在するが、targetにリンクしない場合
        if not linking_pages:
            print("Target page is not linked")
            return
        
        most_linked_page = max(linking_pages, key=lambda id: self.linked_count[id])
        
        print("Most linked pages including [" + target + "]:")
        print(self.titles[most_linked_page])
        print()



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_shortest_path("渋谷", "小野妹子")
    wikipedia.find_no_link_and_linked_pages()
    wikipedia.find_most_linked_pages_include_target_link("Google")
    wikipedia.find_most_linked_pages_include_target_link("グラタン")
    wikipedia.find_most_linked_pages_include_target_link("びゃぼぼ")
    wikipedia.find_most_linked_pages_include_target_link("アジア月間")
    wikipedia.find_most_popular_pages()
