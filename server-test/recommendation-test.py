import random

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def test():
    filename = 'test-recommendation.csv'
    searchQuery = 'dance'

    result = recommends(filename, searchQuery)
    print('searchQuery: ', searchQuery, ' result:', result)

    searchQuery = 'kids,childplay'
    result = recommends(filename, searchQuery)
    print('searchQuery: ', searchQuery, ' result:', result)


def recommends(filename, searchQuery):
    querysDF = pd.read_csv(filename)
    # print('Raw Data: ', querysDF, '\n')

    # loading queryText dataType historical data.
    querysDF = querysDF[querysDF['dataType'] == 'queryText']
    querysDF['rawContent'] = querysDF['rawContent'].str.lower()
    # print('filtered result: ', querysDF[querysDF['dataType'] == 'queryText'], '\n')
    session_queries = querysDF.groupby('session_id')['rawContent'].apply(lambda s: "%s" % ','.join(s))
    # print("Past Queries, ", session_queries.values, '\n')

    # build tfidf recommendation sparse matrix.
    tfidf = TfidfVectorizer()
    queries_tfidf = tfidf.fit_transform(session_queries.values)

    # search by similarity.
    matchInd = np.argmax(cosine_similarity(queries_tfidf, tfidf.transform([searchQuery.lower()])))
    matchedString = session_queries.values[matchInd]
    print('searched', searchQuery, ' result: ', matchedString)

    # excluded search keywords.
    possible_recommendations_set = set(matchedString.split(',')).difference(set(searchQuery.split(',')))
    # print('possible recommendations: ', possible_recommendations_set)
    recommendations = list(possible_recommendations_set)
    # print(recommendations)

    # returns 1 recommendations randomly.
    result = random.choice(recommendations)
    return result


def main():
    test()


if __name__ == '__main__':
    main()
