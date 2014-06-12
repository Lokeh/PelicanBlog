#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Will Acton'
SITENAME = u'Will Acton : Web Developer and Brazilian Jiu Jitsu Fanatic'
SITEDESC = u'Web developer and BJJ fanatic from Portland, OR. A blog about front end, back end, every-end web development. Fitness and jiu jitsu also make appearances.'
SITEURL = 'http://willacton.com/blog/'

TIMEZONE = 'USA/Pacific'
THEME = "theme/summerblue"
CSS_FILE = 'style.css'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

#TEMPLATE_PAGES = {'theme/summerblue/pages/about.html': 'about.html'}
DISPLAY_PAGES_ON_MENU = True

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
CATEGORIES_SAVE_AS = False
CATEGORY_SAVE_AS = False
AUTHOR_SAVE_AS = False
AUTHORS_SAVE_AS = False
TAGS_SAVE_AS = False
TAG_SAVE_AS = False
