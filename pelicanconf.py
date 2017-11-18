#!/usr/bin/env python
import os
from glob import glob
import addlink

AUTHOR = 'lucas'
SITENAME = 'lucas/links'
SITEURL = ''
SERVERURL = 'https://lucas.bourneuf.net'

PATH = 'content'
TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = 'fr'
DEFAULT_DATE_FORMAT = '%d/%m/%Y'

# Feed generation is usually not desired when developing
DEFAULT_PAGINATION = 10
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_METADATA = {
    'tags': 'undefined',
    'status': 'draft',
}

PIWIK = False  # not used as url holder, but uniquely as enable/disable piwik

REMAINING_LINKS = sum(1 for link in addlink.remaining_links())
PUBLISHED_LINKS = len(glob('content/articles/*.mkd'))
SITESUBTITLE = '<em> One link per day for the next {r}</em>'.format(p=PUBLISHED_LINKS, r=REMAINING_LINKS)

# pages
DISPLAY_PAGES_ON_MENU = False
for page_template in glob('pages_template/*.mkd'):
    page_name = os.path.basename(page_template)
    page = 'content/pages/{}'.format(page_name)
    with open(page, 'w') as ofd, open(page_template) as ifd:
        ofd.write(ifd.read().format(
            remaining_links=REMAINING_LINKS,
            published_links=PUBLISHED_LINKS,
        ))
    print('Page {} generated.'.format(page_name))


################################################################################
#                               THEMES
################################################################################
# theme names
THEME_SIMPLE = 'simple'
THEME_NMNLIST = 'nmnlist'
THEME_BOOTSTRAP = 'bootstrap2-dark'
THEME_FUU = 'fuu'

# paths
THEMES_PATH = 'themes/'
MY_THEMES_PATH = 'mythemes/'

# this is the one
# THEME = THEMES_PATH + THEME_BOOTSTRAP
THEME = MY_THEMES_PATH + THEME_BOOTSTRAP
# THEME = MY_THEMES_PATH + THEME_FUU
# THEME = MY_THEMES_PATH + THEME_NMNLIST

# themes config
if THEME_NMNLIST in THEME:
    HIDE_DATE = False


################################################################################
#                           PELICAN PLUGINS
################################################################################
PLUGIN_LIQUID_TAG = [
    'liquid_tags.img',
    'liquid_tags.video',
    # 'liquid_tags.youtube',
    # 'liquid_tags.vimeo',
    # 'liquid_tags.include_code',
    # 'liquid_tags.notebook'
]

# Pelican plugins
PLUGIN_PATHS = ['./pelican-plugins', './myplugins']
PLUGINS = [
    # 'pelican-toc',
    # 'autopages',  # page for authors, tags and categories
    # 'post_stats',  # compute statistics on articles
    'random_article',  # provides a randomly choosen article link
    # 'global_license',  # provides a global constant, containing the license text
    'github_activity',  # dynamic access to github activity
    # 'backreftranslate',  # add is_translation_of attribute to translated articles
    'tag_cloud',  # tag cloud
    *PLUGIN_LIQUID_TAG,  # insert images, videos,… properly
    'section_number',
    # 'filetime_from_git',
    # 'render_math',
    'sitemap',  # cf SITEMAP var

    # My plugins
]


# ACTIVATED PLUGINS DATA
GITHUB_URL = 'https://github.com/aluriak.atom'
GITHUB_ACTIVITY_FEED = 'https://github.com/aluriak.atom'
GITHUB_ACTIVITY_MAX_ENTRIES = 5
RANDOM = 'random.html'  # random_article: name of the generated HTML page
SECTION_NUMBER_MAX = 5
TAG_CLOUD_STEPS = 2  # number of different size
TAG_CLOUD_MAX_ITEMS = 10
TAG_CLOUD_SORTING = 'random'
TAG_CLOUD_BADGE = True
TOC = {'TOC_HEADERS': '^h[1-4]', 'TOC_RUN': 'false'}

# DEACTIVATED PLUGINS DATA
LICENCE = 'WTFPL'  # LICENCE text, globally available



################################################################################
#                           LINKS & FEEDS
################################################################################
# Blogroll:   (font awesome icon, diplayed name, link)
BLOG_LINKS = 'Here', 'bars', (
    ('link',      'all links',   '/links/'),
    ('bar-chart', 'about',       '/links/pages/about.html'),
    ('th-list',   'archive',     '/links/archives.html'),
    ('question',  'random link', '/links/random.html'),
)
LINKS = 'Links', 'external-link', (
    ('home',    'home',    SERVERURL + '/home'),
    ('pencil',  'blog',    SERVERURL + '/blog'),
    ('envelope','mail',    'mailto:{{firstname}}.{{lastname}}@laposte.net'),
)
# OUTER_WEB = 'outer web', 'wpexplorer', (
    # ('user-circle',  'pro-domo',  'https://pro-domo.ddns.net/blog'),
    # ('user-circle',  'dridk',     'http://dridk.labsquare.org/'),
# )

ARTICLE_URL = '{slug}.html'
ARTICLE_SAVE_AS = '{slug}.html'
ARTICLE_LANG_URL = '{slug}.html'
ARTICLE_LANG_SAVE_AS = '{slug}.html'
DRAFT_URL = 'drafts/{slug}.html'
DRAFT_SAVE_AS = 'drafts/{slug}.html'
DRAFT_LANG_URL = 'drafts/{slug}.html'
DRAFT_LANG_SAVE_AS = '{slug}.html'


################################################################################
#                           OTHER & WEIRD
################################################################################
LOAD_CONTENT_CACHE = False
DELETE_OUTPUT_DIRECTORY = True
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
FEED_ATOM = 'feeds/atom.xml'
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'daily',
        'indexes': 'daily',
        'pages': 'daily'
    }
}
