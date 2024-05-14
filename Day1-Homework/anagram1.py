def binary_search(sorted_word, new_dict):
    l = 0
    r = len(new_dict) - 1
    anagram = []

    while l <= r:
        m = (l + r) // 2
        if sorted_word == new_dict[m][0]:
            anagram.append(new_dict[m][1])
            l = m - 1
            r = m + 1
            while l >= 0 and new_dict[l][0] == sorted_word:
                anagram.append(new_dict[l][1])
                l -= 1
            while r < len(new_dict) and new_dict[r][0] == sorted_word:
                anagram.append(new_dict[r][1])
                r += 1
            return anagram
        elif sorted_word > new_dict[m][0]:
            l = m + 1
            continue
        elif sorted_word < new_dict[m][0]:
            r = m - 1
            continue

    return 'No Anagram'

def search_anagram(word, dict):
    sorted_word = "".join(sorted(word))
    new_dict = []
    for key in dict:
        sorted_key = "".join(sorted(key))
        new_dict.append((sorted_key, key))
    new_dict.sort()
    anagram = binary_search(sorted_word, new_dict)
    return anagram

word = input()
with open('words.txt', 'r') as f:
    dict = f.read().splitlines()
print(search_anagram(word, dict))