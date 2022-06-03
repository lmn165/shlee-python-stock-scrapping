if __name__ == '__main__':

    file = open('./data/엔비디아/001/article_202206022001.txt', 'r', encoding='utf-8')
    text = file.read()
    wordList = text.split()
    wordCount = {}
    for word in wordList:
        wordCount[word] = wordCount.get(word, 0) + 1
        keys = sorted(wordCount.keys())

    for word in keys:
        print(f'{word} : {wordCount[word]}')