def binary_search(sorted_s, new_dict):
    l = 0
    r = len(new_dict) - 1
    anagram = []

    while l <= r:
        m = (l + r) // 2
        if sorted_s == new_dict[m][0]:
            anagram.append(new_dict[m][1])
            l = m - 1
            r = m + 1
            while l >= 0 and new_dict[l][0] == sorted_s:
                anagram.append(new_dict[l][1])
                l -= 1
            while r < len(new_dict) and new_dict[r][0] == sorted_s:
                anagram.append(new_dict[r][1])
                r += 1
            return anagram
        elif sorted_s > new_dict[m][0]:
            l = m + 1
            continue
        elif sorted_s < new_dict[m][0]:
            r = m - 1
            continue

    return 'No Anagram'

def search_anagram(s, dict):
    sorted_s = "".join(sorted(s))
    new_dict = []
    for i in dict:
        sorted_i = "".join(sorted(i))
        new_dict.append((sorted_i, i))
    new_dict.sort()
    anagram = binary_search(sorted_s, new_dict)
    return anagram

s = input()
with open('words.txt', 'r') as f:
    dict = f.read().splitlines()
print(search_anagram(s, dict))