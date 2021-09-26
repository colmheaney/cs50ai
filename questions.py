import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    word_map = {}
    for file_name in os.listdir(directory):
        with open(os.path.join(directory, file_name)) as f:
            word_map[file_name] = f.read()

    return word_map


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stop_words = nltk.corpus.stopwords.words("english")

    words = nltk.word_tokenize(document.lower())
    words = [w for w in words if w not in string.punctuation]
    words = [w for w in words if w not in stop_words]

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf_map = {}
    document_names = set(documents)
    for document_name in document_names:
        document_words = documents[document_name]
        for document_word in document_words:
            if document_word in idf_map:
                idf_map[document_word] += 1
            else:
                idf_map[document_word] = 1

    for word in set(idf_map):
        frequency = idf_map[word]
        idf = math.log(len(documents)/frequency)
        idf_map[word] = idf
        
    return idf_map


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = {}
    for file in files:
        tf_idf = 0
        for query_word in query:
            if query_word in files[file]:
                idf = idfs[query_word]
                count = files[file].count(query_word)
                tf_idf += idf * count

        tf_idfs[file] = tf_idf

    sorted_docs = list(dict(sorted(tf_idfs.items(), key=lambda item: item[1])).keys())
    return sorted_docs[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    idf_sentence_scores = {}
    for sentence in sentences:
        idf_sum = 0
        num_of_sentence_words_in_query = 0
        for query_word in query:
            if query_word in sentences[sentence]:
                idf_sum += idfs[query_word]
                num_of_sentence_words_in_query += 1
        
        query_word_density = num_of_sentence_words_in_query / len(sentences[sentence])
        idf_sentence_scores[sentence] = (idf_sum, query_word_density)
    
    idf_sentence_scores = sorted(idf_sentence_scores.items(), 
                                 key=lambda item: (item[1][0], item[1][1]),
                                 reverse=True)
                                 
    return [s[0] for s in idf_sentence_scores[:n]]


if __name__ == "__main__":
    main()
