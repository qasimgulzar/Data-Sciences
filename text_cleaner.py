import json


def tokenize_remove_stopwords(text):
    '''
    :param text: text string
    :return: remove stopwords from provided text string and return list of all other words.
    '''
    from nltk import RegexpTokenizer
    from nltk.corpus import stopwords
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = stopwords.words('english')
    word_tokens = tokenizer.tokenize(text)
    words = [word_tokens[i] for i in range(len(word_tokens)) if
             len(word_tokens[i]) > 0 and word_tokens[i] not in stop_words]
    return words;


def find_bigrams(input_list):
    '''
    :param input_list: list of words.
    :return: list of bigrams of provided list.
    '''
    bigram_list = []
    for i in range(len(input_list) - 1):
        bigram_list.append((input_list[i], input_list[i + 1]))
    return bigram_list


def get_word_count(words):
    '''
    :param words: list of words
    :return: dict of word count.
    '''
    distinct_words = list(set(words))
    words_count = [words.count(distinct_words[i]) for i in range(len(distinct_words))]
    return list(zip(distinct_words, words_count))


def get_top_topic_keywords(word_counts, threshold=10, global_topic_words=[]):
    '''
    :param word_counts: list of words with their count of occurrence in key pair {word: count}.
    :param threshold: Integer value to extract top x% word counts.
    :param global_topic_words: list of words from whole article (text)
    :return: list threshold% word count.
    '''
    import math as m
    total_words = len(word_counts)
    top = m.ceil((total_words * threshold) / 100)
    word_counts.sort(
        key=lambda word: word[1],
        reverse=True
    )
    topic_words = []
    paragraph_topic_words = [paragraph_topic_word[0] for paragraph_topic_word in word_counts]
    for g_topic_keyword in global_topic_words:
        if (g_topic_keyword in paragraph_topic_words):
            for topic_keyword in word_counts:
                if topic_keyword[0] == g_topic_keyword:
                    topic_words.append(topic_keyword)
            top = top - 1
    # for paragraph_topic_word in word_counts:
    #     if paragraph_topic_word[0] in global_topic_words:
    #         topic_words.append(paragraph_topic_word)
    #         top = top - 1
    if (top > 0):
        for paragraph_topic_word in word_counts:
            if paragraph_topic_word[0] not in global_topic_words:
                topic_words.append(paragraph_topic_word)
                top = top - 1
                if top < 1: break

    return topic_words


def word_count_with_most_used(words, threshold=10, global_topic_keywords=[]):
    '''
    :param words: list of keywords
    :param threshold:  default set to 10
    :param global_topic_keywords: list of keywords from whole text.
    :return: {word_count:[('word': count)],global_words(topic_keywords):[('word):count]}
    '''
    word_count = get_word_count(words)
    global_most_used_words = get_top_topic_keywords(word_counts=word_count, threshold=threshold,
                                                    global_topic_words=global_topic_keywords)
    return {'word_count': list(word_count), 'global_words': global_most_used_words}


# json.dump(word_count_and_most_used_global, open('global-word-counts.json', 'w'), indent=4)

def process_text(allstr, word_count_and_most_used_global):
    '''

    :param allstr: list of all paragraphs
    :param word_count_and_most_used_global: word count and global keywords fro whole text
    :return: None
    '''
    for str in allstr:
        if (len(str.strip()) > 0):
            paragraph_words = tokenize_remove_stopwords(str.lower())
            bigrams = find_bigrams([word for word in paragraph_words])
            bigram_strs = [' '.join(bigram) for bigram in bigrams]
            global_topic_keywords = [global_topic_keyword[0] for global_topic_keyword in
                                     word_count_and_most_used_global['global_words']]

            word_count_and_most_used = word_count_with_most_used(paragraph_words, threshold=10,
                                                                 global_topic_keywords=global_topic_keywords)
            global_topic_keywords_str = ",".join(
                ["%s : %s " % (g_count[0], g_count[1]) for g_count in
                 word_count_and_most_used_global['global_words']])

            words_str = ",".join(paragraph_words)

            bigrams_str = ",".join(bigram_strs)

            word_count_str = ",".join(
                ["%s : %s " % (w_count[0], w_count[1]) for w_count in word_count_and_most_used['word_count']])

            paragraph_topic_word_counts = ",".join(
                ["%s : %s " % (g_count[0], g_count[1]) for g_count in word_count_and_most_used['global_words']])
            paragraph_query_str = " ".join(
                ["%s " % (g_count[0],) for g_count in word_count_and_most_used['global_words']])

            print(
                "\n--------- Paragraph Start -------------",
                "\nTEXT : %s" % str.strip(),
                "\nWORDS : { %s }" % words_str,
                "\nBI-GRAMS : { %s }" % bigrams_str,
                "\nWORD-COUNT : { %s }" % word_count_str,
                "\nPARAGRAPH-TOPIC-WORD-COUNT : { %s }" % paragraph_topic_word_counts,
                "\nGLOBAL-TOPIC-WORD-COUNT : { %s }" % global_topic_keywords_str,
                "\nPARAGRAPH-QUERY : { %s }" % paragraph_query_str,
                "\n--------- Paragraph End ---------------"
            )


if __name__ == '__main__':
    with open('test4.txt') as f:
        allstr = f.readlines()

        words = tokenize_remove_stopwords(" ".join(allstr).lower())

        word_count_and_most_used_global = word_count_with_most_used(words)

        process_text(allstr=allstr, word_count_and_most_used_global=word_count_and_most_used_global)
