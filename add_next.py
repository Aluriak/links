"""Get a link in input file,
and publish it.

"""

import os
import csv
import time
import random
import argparse
import markdown
from enum import Enum


class Method(Enum):
    """Link picking method"""
    First, Last, Random = 'first', 'last', 'random'

assert Method('first') == Method.First


DSV_FIELD_SEP = chr(31)
DSV_RECORD_SEP = chr(30)
CSV_PARAMS = {
    'delimiter': DSV_FIELD_SEP,
    # 'lineterminator': DSV_RECORD_SEP,  # NOT HANDLED BY PYTHON. NOT A JOKE. WTF PYTHON.
    'lineterminator': '\n',
}

LINKS_TO_PUBLISH = 'data/topublish.csv'
TEMPLATE = 'data/template.mkd'
DEFAULT_AUTHOR = 'lucas'
DEFAULT_LANG = 'fr'
DEFAULT_STATUS = 'published'
UID_SIZE = 10


def random_id(size:int=10) -> str:
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(alphabet) for _ in range(size))


def publish_link(url:str, title:str, description:str, tags:iter, date:str,
                 lang:str=DEFAULT_LANG, status:str=DEFAULT_STATUS):
    """Create the page, put it in articles"""
    with open(TEMPLATE) as fd:
        mkd = fd.read()
    slug = random_id(UID_SIZE)
    filename = f'content/articles/{date}_{slug}.mkd'
    while os.path.exists(filename):
        print('Article {} already exists'.format(filename))
        slug = random_id(UID_SIZE)
        filename = f'content/articles/{date}_{slug}.mkd'
    print('New article:', filename)
    assert not os.path.exists(filename)

    # interpret the title as mkd (allowing italic for instance)
    html_title = markdown.markdown(title)
    if html_title.startswith('<p>'):
        html_title = html_title[len('<p>'):]
    if html_title.endswith('</p>'):
        html_title = html_title[:-len('</p>')]

    print(html_title)
    with open(filename, 'w', encoding='utf8') as fd:
        fd.write(mkd.format(
        title=html_title,
        slug=slug,
        url=url,
        description=description,
        tags=', '.join(tags),
        date=date,
        lang=lang,
        status=status,
    ))


def extract_and_publish(method:Method=Method.First, use_date_field:bool=False):
    """Extract the next link, and publish it."""
    with open(LINKS_TO_PUBLISH, encoding='utf_8_sig') as fd:
        reader = csv.reader(fd, **CSV_PARAMS)
        links = tuple(reader)
    if len(links) == 0:
        raise ValueError(f"No more links to extract ({LINKS_TO_PUBLISH} is empty).")
    else:
        if method is Method.First:
            index = 0
        elif method is Method.Last:
            index = len(links) - 1
        elif method is Method.Random:
            index = random.choice(range(len(links)))
        else:
            raise ValueError("Given method, {}, is unexpected. Valid methods: {}"
                             "".format(method, ', '.join(m.value for m in Methods)))
    link = links[index]
    links = (links[:index] if index != 0 else ()) + links[index+1:]
    # build the article
    publication_timestamp = None  # use the current time by default
    if use_date_field and len(link) == 4:
        publication_timestamp = float(link[3])  # use timestamp in data
    publish_link(url=link[2], title=link[0], description=link[1], tags=[],
                 date=current_time(publication_timestamp))
    # rebuild the topublish database
    with open(LINKS_TO_PUBLISH, 'w', encoding='utf_8_sig') as fd:
        writer = csv.writer(fd, **CSV_PARAMS)
        for link in links:
            writer.writerow(link)


def current_time(timestamp:float=None):
    local = time.localtime(timestamp)
    # print(local)
    return '{y:02}-{t:02}-{d:02}-{h:02}:{m:02}:{s:02}'.format(
        y=local.tm_year, t=local.tm_mon, d=local.tm_mday,
        h=local.tm_hour, m=local.tm_min, s=local.tm_sec,
    )


def parse_cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--method', type=Method, default=Method.First,
                        help="method to use to extract the next link: {}".format(', '.join(m.value for m in Method)))
    parser.add_argument('--use-date-field', action='store_true',
                        default=False,
                        help="Use the fourth field in input file to determine publication date.")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_cli()
    # print(args)
    extract_and_publish(method=args.method, use_date_field=args.use_date_field)
