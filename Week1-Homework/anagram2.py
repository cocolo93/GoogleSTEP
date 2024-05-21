   
@profile
def count_words(word):
    counter = {}
    for i in word:
        if i in counter:
            counter[i] += 1
        else:
            counter[i] = 1
    return counter

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
@profile
def calculate_score(word):
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score
@profile
def is_subset(dict_counter, word_counter):
    for key in dict_counter:
        if key not in word_counter or dict_counter[key] > word_counter[key]:
            return False
    return True
@profile
def search_anagram(word, dict):
    word_counter = count_words(word)
    best_score = 0
    anagram = None
    for key in dict:
        dict_counter = count_words(key)
        if is_subset(dict_counter, word_counter) and word != key:
            score = calculate_score(key)
            if score > best_score:
                best_score = score
                anagram = key
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
