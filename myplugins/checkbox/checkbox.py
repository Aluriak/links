"""
checkbox
===================================

This Pelican-Markdown plugin replace github like markdown notation of checkbox by html code.
"""

import re
import markdown as md
from markdown.inlinepatterns import Pattern
from markdown.extensions import Extension
from markdown.util import etree


BOX_PATTERN = r'\[([ a-z-]+)\]'
ICONS_SHORTCUT = {
    ' ': 'fa-square-o',
    'v': 'fa-check-square-o',
    'x': 'fa-times',
    'n': 'fa-times',
    'l': 'fa-link',
    's': 'fa-space-shuttle',
    'g': 'fa-gitlab',
    't': 'fa-terminal',
    '+': 'fa-plus',
    '-': 'fa-minus',
    'o': 'fa-ok-sign',
    'b': 'fa-bomb',
    '»': 'fa-caret-right',
    '«': 'fa-caret-left',
    '>': 'fa-chevron-right',
    '<': 'fa-chevron-left',
}


class BoxPattern(Pattern):
    def handleMatch(self, m):
        boxcontent = m.group(2)
        box_name = ICONS_SHORTCUT.get(boxcontent, 'fa-' + boxcontent)
        el = etree.Element('i', {'class': 'fa {} fa-fw'.format(box_name)})
        el.text = ''
        return el


class BoxExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('boxpattern', BoxPattern(BOX_PATTERN), '_end')
