import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def test():
    querysDF = pd.read_csv('test-recommendation.csv')
    print('Raw Data: ', querysDF, '\n')
    session_queries = querysDF.groupby('session_id')['rawContent'].apply(lambda s: "%s" % ','.join(s))
    print("Past Queries, ", session_queries.values, '\n')

    tfidf = TfidfVectorizer()
    queries_tfidf = tfidf.fit_transform(session_queries.values)

    searchQuery = 'dance'
    matchInd = np.argmax(cosine_similarity(queries_tfidf, tfidf.transform([searchQuery])))
    print('searched', searchQuery, ' result: ', session_queries.values[matchInd])

    searchQuery = 'kid, childplay'
    matchInd = np.argmax(cosine_similarity(queries_tfidf, tfidf.transform([searchQuery])))
    print('searched', searchQuery, ' result: ', session_queries.values[matchInd])


def main():
    test()


if __name__ == '__main__':
    main()
