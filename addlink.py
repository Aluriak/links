#!/usr/bin/python3
import os
import sys
import csv
import time
import codecs

DSV_FIELD_SEP = chr(31)
DSV_RECORD_SEP = chr(30)
CSV_PARAMS = {
    'delimiter': DSV_FIELD_SEP,
    # 'lineterminator': DSV_RECORD_SEP,  # NOT HANDLED BY PYTHON. NOT A JOKE. WTF PYTHON.
    'lineterminator': '\n',
}

LINKS_TO_PUBLISH = 'data/topublish.csv'


def add_link():
    try:
        DATA_TO_ADD = sys.argv[1]
    except IndexError:
        print('Expect first arg to be path to the file containing the information to add to database.')
        exit(1)

    print('ENCODING:', sys.stdout.encoding)
    # extract data
    with codecs.open(DATA_TO_ADD, 'r', encoding='utf_8_sig') as fd:
        title = next(fd).strip()
        url = next(fd).strip()
        tags = next(fd).strip()
        body = fd.read().strip()
        pubdate = int(time.time())


    # write data into database
    WORKING_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    os.chdir(WORKING_DIR)

    # NB: do not append the utf-8-sig at start (the codec is dumb: it would add it at the end)
    with codecs.open(LINKS_TO_PUBLISH, 'a', encoding='utf_8') as fd:
        writer = csv.writer(fd, **CSV_PARAMS)
        writer.writerow((title, tags, body, url, pubdate))

    print('DONE:', title)


def remaining_links():
    # WORKING_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    # os.chdir(WORKING_DIR)
    # print(WORKING_DIR)

    # NB: do not append the utf-8-sig at start (the codec is dumb: it would add it at the end)
    with codecs.open(LINKS_TO_PUBLISH, encoding='utf_8') as fd:
        reader = csv.reader(fd, **CSV_PARAMS)
        yield from reader


if __name__ == '__main__':
    add_link()
