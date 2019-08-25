import pandas as pd

from eventfindaClient import recommends


def test():
    filename = 'test-recommendation.csv'

    session_id = 'ABwppHHo-pdB0jaxXCJVBTh5SlcIDrDDzMKKKsOVqS8YWAUwzI-sGrSRSHPMliIs0b4Vv5Rp_GlxyDmtXWPEFprWM852BER5Pg'

    df = pd.read_csv(filename)

    df_session = df[df['session_id'] == session_id]

    # print(df_session)

    searchQuery = df_session.groupby('session_id')['rawContent'].apply(lambda s: "%s" % ','.join(s)).values[0]

    # searchQuery = 'kids,childplay'
    result = recommends(filename, searchQuery)
    print('searchQuery: ', searchQuery, ' single result:', result, '\r\n')

    searchQuery = 'dance'

    result = recommends(filename, searchQuery)
    print('searchQuery: ', searchQuery, ' single result:', result, '\r\n')


def main():
    test()


if __name__ == '__main__':
    main()
