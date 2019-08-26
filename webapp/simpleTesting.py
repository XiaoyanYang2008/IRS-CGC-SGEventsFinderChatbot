import random
import csv
import os

import pandas as pd
from eventfindaClient import loadEvent


def testSessionAndDataInsertion():
    session_id_str = 'projects/local-event-finder-udknhf/agent/sessions/c0cc2f9b-e7a7-8aff-5d7b-c3931da50615'
    session_id = parseSessionID(session_id_str)
    value = random.randint(0, 100)
    insertData('user-data.csv', session_id, 'queryText', value)
    value = random.randint(0, 100)
    insertData('user-data.csv', session_id, 'queryText', value)

    print(value)


def testLoadEvent():
    loadEvent('The All-Babes Cineleisure Dance Battle Returns',
              'ABwppHEzuq0BXbiZEMwRDZu-DsVUtPoK8D3GcTUXhefu9VC-4I1f9RmJyYg0ZQE7ymGluFFb5XBcDPTLYZ7zMVj5Z1aBxbuDsg')


def main():
    # testSessionAndDataInsertion()

    testLoadEvent()
    # testStringJoin()


def parseSessionID(session_id_str):
    if session_id_str is None or session_id_str == '':
        return ''

    chunks = session_id_str.split('/')
    session_id = chunks[len(chunks) - 1]
    return session_id


def insertData(filename, session_id, dataType, rawContent):
    # Insert data into csv file
    try:
        header = ['session_id', 'dataType', 'rawContent']
        data = [session_id, dataType, rawContent]

        if not os.path.exists(filename):
            with open(filename, "w") as tmp:
                wh = csv.writer(tmp, quoting=csv.QUOTE_NONE)
                wh.writerow(header)
                tmp.close()

        with open(filename, "a+") as fp:
            wr = csv.writer(fp, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(data)

        return "Resume of " + session_id + " created successfully"
    except Exception as e:
        errmsg = "Error encountered: " + str(e)
        return errmsg


if __name__ == '__main__':
    main()
