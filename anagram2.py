def count_words(s):
    counter = {}
    for i in s:
        if i in counter:
            counter[i] += 1
        else:
            counter[i] = 1
    return counter

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

def calculate_score(word):
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score

def is_subset(dict_counter, word_counter):
    for key in dict_counter:
        if key not in word_counter or dict_counter[key] > word_counter[key]:
            return False
    return True

def search_anagram(s, dict):
    word_counter = count_words(s)
    best_score = 0
    anagram = None
    for i in dict:
        sorted_i = "".join(sorted(i))
        dict_counter = count_words(sorted_i)
        if is_subset(dict_counter, word_counter) and s != i:
            score = calculate_score(i)
            if score > best_score:
                best_score = score
                anagram = i    
    return anagram

input_src = input('input?' )
output_src = input('output?' )

with open(input_src, 'r') as f:
    words = f.read().splitlines()
with open('words.txt', 'r') as f:
    dict = f.read().splitlines()

for word in words:
    anagram = search_anagram(word, dict)
    with open(output_src, mode='a') as f1:
        f1.write(anagram + '\n')
