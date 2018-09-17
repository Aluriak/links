"""
pietags
===================================
This plugin generates a pie chart from available tags
"""


from collections import Counter
from operator import itemgetter

import logging
import math
import random

from pelican import signals

logger = logging.getLogger(__name__)


def set_default_settings(settings):
    settings.setdefault('PIETAG_MOST_COMMON', 16)
    settings.setdefault('PIETAG_OTHERS_LABEL', 'others')
    settings.setdefault('PIETAG_HTML_TARGET', 'data/pietags.html')



def init_default_config(pelican):
    from pelican.settings import DEFAULT_CONFIG
    set_default_settings(DEFAULT_CONFIG)
    if pelican:
        set_default_settings(pelican.settings)


def generate_pie_chart(generator):
    NB_TAG = generator.settings.get('PIETAG_MOST_COMMON')
    OTHERS_LABEL = generator.settings.get('PIETAG_OTHERS_LABEL')
    HTML_TARGET = generator.settings.get('PIETAG_HTML_TARGET')
    # logger.warning("hello")
    counts = Counter(tag for article in generator.articles
                     for tag in getattr(article, 'tags', []))
    most_common = {tag.name: count for tag, count in counts.most_common(NB_TAG)}
    most_common[OTHERS_LABEL] = sum(count for tag, count in counts.items() if tag.name not in most_common)
    assert len(most_common) == NB_TAG + 1, len(most_common)
    with open(HTML_TARGET, 'w') as fd:
        fd.write(build_pie_chart_code(most_common, {tag.name: tag for tag in counts}))


def build_pie_chart_code(counts:dict, tag_objects:dict) -> 'html':
    import plotly.offline as offline
    import plotly.graph_objs as go

    labels, values = zip(*counts.items())

    trace = go.Pie(
        labels=labels, values=values,
        hoverinfo='label+percent',
        textinfo='value', textfont={'size': 15},
        marker={'line': {'color': '#000000', 'width': 2}})
    layout = go.Layout(
        title='<b>Tags distribution among links</b>',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    figure = go.Figure(data=[trace], layout=layout)
    return offline.plot(figure, output_type='div')



def register():
    signals.initialized.connect(init_default_config)
    signals.article_generator_finalized.connect(generate_pie_chart)
