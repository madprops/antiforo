
# encoding: utf-8

import datetime
from gettext import gettext as _
import locale
import re
import string
import unicodedata
from django import template
from django.conf import settings
from django.utils import formats
from django.utils.encoding import force_unicode, iri_to_uri
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe, SafeData
from django.template.defaultfilters import stringfilter
from django.utils.translation import ugettext, ungettext
from django.utils.dateformat import format
from django.utils.safestring import SafeData, mark_safe
from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy
from django.utils.http import urlquote

register = template.Library()
	
def ultralize(text, trim_url_limit=None, nofollow=False, autoescape=False):
	trim_url = lambda x, limit=trim_url_limit: limit is not None and (len(x) > limit and ('%s...' % x[:max(0, limit - 3)])) or x
	safe_input = isinstance(text, SafeData)
	words = word_split_re.split(force_unicode(text))
	nofollow_attr = nofollow and ' rel="nofollow"' or ''
	has_stuff = False
	for i, word in enumerate(words):
		match = None
		if '.' in word or '@' in word or ':' in word:
			match = punctuation_re.match(word)
		if match:
			lead, middle, trail = match.groups()
			# Make URL we want to point to.
			url = None
			if middle.startswith('http://') or middle.startswith('https://'):
				url = urlquote(middle, safe='/&=:;#?+*')
			elif middle.startswith('www.') or ('@' not in middle and \
					middle and middle[0] in string.ascii_letters + string.digits and \
					(middle.endswith('.org') or middle.endswith('.net') or middle.endswith('.com'))):
				url = urlquote('http://%s' % middle, safe='/&=:;#?+*')
			elif '@' in middle and not ':' in middle and simple_email_re.match(middle):
				url = 'mailto:%s' % middle
				nofollow_attr = ''
			# Make link.
			if url:
				trimmed = trim_url(middle)
				ytregex = re.compile(r"v=(?P<id>[A-Za-z0-9\-=_]{11})")
				vimeoregex = re.compile(r"^(http://)?(www\.)?(vimeo\.com/)(?P<id>\d+)")
				dmregex = re.compile(r"^(http://)?(www\.)?(dailymotion\.com/video/)(?P<id>[A-Za-z0-9]+)")
				ytmatch = ytregex.search(middle)
				vimeomatch = vimeoregex.match(middle)
				dmmatch = dmregex.match(middle)
				if ytmatch:
					video_id = ytmatch.group('id')
				if vimeomatch:
					video_id = vimeomatch.group('id')
				if dmmatch:
					video_id = dmmatch.group('id')
				if autoescape and not safe_input:
					lead, trail = escape(lead), escape(trail)
					url, trimmed = escape(url), escape(trimmed)
				if any(s in middle for s in ['.jpg', '.JPG', '.gif', '.GIF', '.bmp', '.BMP', '.png', '.PNG', '.jpeg', '.JPEG', 'gstatic.com/images']):
					if has_stuff:
						middle = ''
					else:
						middle = '<a target=_blank href="%s"><img class="contentimg" style="padding-top:8px;display:block; max-width:100%%" src="%s"></a>' % (url, url)
						has_stuff = True
				elif middle.startswith("http://www.youtube.com/") or middle.startswith("www.youtube.com/") or middle.startswith("youtube.com/") or middle.startswith("https://www.youtube.com/"):
					if ytmatch:
						if has_stuff:
							middle = ''
						else:
							middle = "<iframe style=\"z-index:-1000;padding-top:8px;display:block;margin-bottom:3px\" title=\"YouTube video player\" width=\"400\" height=\"243\" src=\"http://www.youtube.com/embed/%s\" frameborder=\"0\" allowfullscreen></iframe>" % (video_id + "?wmode=opaque&autohide=1&amp&disablekb=1&rel=0")
							has_stuff = True
				elif middle.startswith("http://www.vimeo.com") or middle.startswith("www.vimeo.com") or middle.startswith("vimeo.com") or middle.startswith("http://vimeo.com"):
					if vimeomatch:
						if has_stuff:
							middle = ''
						else:
							middle = "<iframe style='padding-top:8px;display:block;'src=\"http://player.vimeo.com/video/%s?title=0&amp;byline=0&amp;portrait=0\" width=\"600\" height=\"405\" frameborder=\"0\"></iframe>" % (video_id)
							has_stuff = True
				elif middle.startswith("http://www.dailymotion.com") or middle.startswith("www.dailymotion.com") or middle.startswith("dailymotion.com") or middle.startswith("http://dailymotion.com"):
					if dmmatch:
						if has_stuff:
							middle = ''
						else:
							middle = "<iframe style='padding-top:8px' frameborder='0' width='560' height='315' src='http://www.dailymotion.com/embed/video/%s?width=560'></iframe>" % (video_id)
							has_stuff = True
				elif middle.endswith(".ogg") or middle.endswith(".mp3"): 
					if has_stuff:
						middle = ''
					else:
						middle = "<audio style=\"display:block;margin-bottom:8px\" src=\"%s\" controls=\"controls\"></audio>" % (url)
						has_stuff = True
				else:
					if has_stuff:
						middle = ''
					else:
						middle = "<a style='display:block;' target='_blank' href='%s'%s>%s</a>" % (url, nofollow_attr, trimmed)
						has_stuff = True
				words[i] = mark_safe('%s%s%s' % (lead, middle, trail))
			else:
				if safe_input:
					words[i] = mark_safe(word)
				elif autoescape:
					words[i] = escape(word)
		elif safe_input:
			words[i] = mark_safe(word)
		elif autoescape:
			words[i] = escape(word)
	return mark_safe(u''.join(words))

def get_media_url(text, trim_url_limit=None, nofollow=False, autoescape=False):
	middle = 'nope'
	trim_url = lambda x, limit=trim_url_limit: limit is not None and (len(x) > limit and ('%s...' % x[:max(0, limit - 3)])) or x
	safe_input = isinstance(text, SafeData)
	words = word_split_re.split(force_unicode(text))
	nofollow_attr = nofollow and ' rel="nofollow"' or ''
	for i, word in enumerate(words):
		match = None
		if '.' in word or '@' in word or ':' in word:
			match = punctuation_re.match(word)
		if match:
			lead, middle, trail = match.groups()
			# Make URL we want to point to.
			url = None
			if middle.startswith('http://') or middle.startswith('https://'):
				url = urlquote(middle, safe='/&=:;#?+*')
			elif middle.startswith('www.') or ('@' not in middle and \
					middle and middle[0] in string.ascii_letters + string.digits and \
					(middle.endswith('.org') or middle.endswith('.net') or middle.endswith('.com'))):
				url = urlquote('http://%s' % middle, safe='/&=:;#?+*')
			elif '@' in middle and not ':' in middle and simple_email_re.match(middle):
				url = 'mailto:%s' % middle
				nofollow_attr = ''
			# Make link.
			if url:
				trimmed = trim_url(middle)
				ytregex = re.compile(r"v=(?P<id>[A-Za-z0-9\-=_]{11})")
				vimeoregex = re.compile(r"^(http://)?(www\.)?(vimeo\.com/)(?P<id>\d+)")
				dmregex = re.compile(r"^(http://)?(www\.)?(dailymotion\.com/video/)(?P<id>[A-Za-z0-9]+)")
				ytmatch = ytregex.search(middle)
				vimeomatch = vimeoregex.match(middle)
				dmmatch = dmregex.match(middle)
				if ytmatch:
					video_id = ytmatch.group('id')
				if vimeomatch:
					video_id = vimeomatch.group('id')
				if dmmatch:
					video_id = dmmatch.group('id')
				if autoescape and not safe_input:
					lead, trail = escape(lead), escape(trail)
					url, trimmed = escape(url), escape(trimmed)
				if any(s in middle for s in ['.jpg', '.JPG', '.gif', '.GIF', '.bmp', '.BMP', '.png', '.PNG', '.jpeg', '.JPEG', 'gstatic.com/images']):
					middle = '<a target=_blank href="%s"><img class="contentimg" style="display:block; width:100%%;padding-top:5px; margin-bottom:3px" src="%s"></a>' % (url, url)
				elif middle.startswith("http://www.youtube.com/") or middle.startswith("www.youtube.com/") or middle.startswith("youtube.com/") or middle.startswith("https://www.youtube.com/"):
					if ytmatch:
						middle = "<iframe style=\"display:block;padding-top:5px; margin-bottom:3px\" title=\"YouTube video player\" width=\"600\" height=\"365\" src=\"http://www.youtube.com/embed/%s\" frameborder=\"0\" allowfullscreen></iframe>" % (video_id + "?wmode=opaque&autohide=1&amp&disablekb=1&rel=0")
				elif middle.startswith("http://www.vimeo.com") or middle.startswith("www.vimeo.com") or middle.startswith("vimeo.com") or middle.startswith("http://vimeo.com"):
					if vimeomatch:
						middle = ''
						middle = "<iframe style='display:block;'src=\"http://player.vimeo.com/video/%s?title=0&amp;byline=0&amp;portrait=0\" width=\"600\" height=\"405\" frameborder=\"0\"></iframe>" % (video_id)
				elif middle.startswith("http://www.dailymotion.com") or middle.startswith("www.dailymotion.com") or middle.startswith("dailymotion.com") or middle.startswith("http://dailymotion.com"):
					if dmmatch:
						middle = "<iframe frameborder='0' width='560' height='315' src='http://www.dailymotion.com/embed/video/%s?width=560'></iframe>" % (video_id)
				elif middle.endswith(".ogg") or middle.endswith(".mp3"):
					middle = "<audio style=\"display:block;padding-top:5px; margin-bottom:6px\" src=\"%s\" controls=\"controls\"></audio>" % (url)
				else:
					middle = "<a style='display:block;' target='_blank' href='%s'%s>%s</a>" % (url, nofollow_attr, trimmed)
				return middle
	return False

def has_url(text, trim_url_limit=None, nofollow=False, autoescape=False):
	middle = 'nope'
	trim_url = lambda x, limit=trim_url_limit: limit is not None and (len(x) > limit and ('%s...' % x[:max(0, limit - 3)])) or x
	safe_input = isinstance(text, SafeData)
	words = word_split_re.split(force_unicode(text))
	nofollow_attr = nofollow and ' rel="nofollow"' or ''
	for i, word in enumerate(words):
		match = None
		if '.' in word or '@' in word or ':' in word:
			match = punctuation_re.match(word)
		if match:
			lead, middle, trail = match.groups()
			url = None
			if middle.startswith('http://') or middle.startswith('https://'):
				url = urlquote(middle, safe='/&=:;#?+*')
			elif middle.startswith('www.') or ('@' not in middle and \
					middle and middle[0] in string.ascii_letters + string.digits and \
					(middle.endswith('.org') or middle.endswith('.net') or middle.endswith('.com'))):
				url = urlquote('http://%s' % middle, safe='/&=:;#?+*')
			elif '@' in middle and not ':' in middle and simple_email_re.match(middle):
				url = 'mailto:%s' % middle
				nofollow_attr = ''
			if url:
				return True
	return False

@register.filter
def datemate(value):
	hoy = datetime.date.today()
	if value.year == hoy.year:
		fecha = format(value, "d F").replace(' 0', ' ')
	else:
		fecha = format(value, "d F Y").replace(' 0', ' ')
	ayer = hoy - datetime.timedelta(1)
	hora = format(value, "g:i A").lower()
	if value.year == hoy.year and value.month == hoy.month and value.day == hoy.day:
		fecha = "today"
	if value.year == ayer.year and value.month == ayer.month and value.day == ayer.day:
		fecha = "yesterday"
	return fecha + " " + "at" + " " + hora
	
@register.filter
def radtime(time):
	now = datetime.datetime.now()
	if type(time) is int:
		diff = now - datetime.datetime.fromtimestamp(time)
	elif isinstance(time,datetime.datetime):
		diff = now - time 
	elif not time:
		diff = now - now
	second_diff = diff.seconds
	day_diff = diff.days
	if day_diff < 0:
		return ''
	if day_diff == 0:
		if second_diff < 60:
			return "less than a minute ago"
		if second_diff < 120:
			return  "1 minute ago"
		if second_diff < 3600:
			return str( second_diff / 60 ) + " minutes ago"
		if second_diff < 7200:
			return "1 hour ago"
		if second_diff < 86400:
			return str( second_diff / 3600 ) + " hours ago"
	if day_diff == 1:
		return "1 day ago"
	if day_diff < 7:
		return str(day_diff) + " days ago"
	if day_diff < 31:
		if day_diff/7 == 1:
			ago = " week ago"
		else:
			ago = " weeks ago"
		return str(day_diff/7) + ago
	if day_diff < 365:
		if day_diff/30 == 1:
			ago = " month ago"
		else:
			ago = " months ago"
		return str(day_diff/30) + ago
	if day_diff/365 == 1:
		ago = " year ago"
	else:
		ago = " years ago"
	return str(day_diff/365) + ago

@register.filter
def happy_time(value):
	time = datetime.datetime.now()
	return format(time, "g:i A").lower()

@register.filter
@stringfilter
def stripper(value):
	p = re.compile(r'<.*?>')
	return p.sub('', value)

























################################################
################################################

"""HTML utilities suitable for global use."""

################################################
################################################

# Configuration for urlize() function.
LEADING_PUNCTUATION  = ['(', '<', '&lt;']
TRAILING_PUNCTUATION = ['.', ',', ')', '>', '\n', '&gt;']

# List of possible strings used for bullets in bulleted lists.
DOTS = ['&middot;', '*', '\xe2\x80\xa2', '&#149;', '&bull;', '&#8226;']

unencoded_ampersands_re = re.compile(r'&(?!(\w+|#\d+);)')
word_split_re = re.compile(r'(\s+)')
punctuation_re = re.compile('^(?P<lead>(?:%s)*)(?P<middle>.*?)(?P<trail>(?:%s)*)$' % \
	('|'.join([re.escape(x) for x in LEADING_PUNCTUATION]),
	'|'.join([re.escape(x) for x in TRAILING_PUNCTUATION])))
simple_email_re = re.compile(r'^\S+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+$')
link_target_attribute_re = re.compile(r'(<a [^>]*?)target=[^\s>]+')
html_gunk_re = re.compile(r'(?:<br clear="all">|<i><\/i>|<b><\/b>|<em><\/em>|<strong><\/strong>|<\/?smallcaps>|<\/?uppercase>)', re.IGNORECASE)
hard_coded_bullets_re = re.compile(r'((?:<p>(?:%s).*?[a-zA-Z].*?</p>\s*)+)' % '|'.join([re.escape(x) for x in DOTS]), re.DOTALL)
trailing_empty_content_re = re.compile(r'(?:<p>(?:&nbsp;|\s|<br \/>)*?</p>\s*)+\Z')
del x # Temporary variable

def escape(html):
	"""
	Returns the given HTML with ampersands, quotes and angle brackets encoded.
	"""
	return mark_safe(force_unicode(html).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'))
escape = allow_lazy(escape, unicode)

_base_js_escapes = (
	('\\', r'\u005C'),
	('\'', r'\u0027'),
	('"', r'\u0022'),
	('>', r'\u003E'),
	('<', r'\u003C'),
	('&', r'\u0026'),
	('=', r'\u003D'),
	('-', r'\u002D'),
	(';', r'\u003B'),
	(u'\u2028', r'\u2028'),
	(u'\u2029', r'\u2029')
)

# Escape every ASCII character with a value less than 32.
_js_escapes = (_base_js_escapes +
			   tuple([('%c' % z, '\\u%04X' % z) for z in range(32)]))

def escapejs(value):
	"""Hex encodes characters for use in JavaScript strings."""
	for bad, good in _js_escapes:
		value = mark_safe(force_unicode(value).replace(bad, good))
	return value
escapejs = allow_lazy(escapejs, unicode)

def conditional_escape(html):
	"""
	Similar to escape(), except that it doesn't operate on pre-escaped strings.
	"""
	if isinstance(html, SafeData):
		return html
	else:
		return escape(html)

def linebreaks(value, autoescape=False):
	"""Converts newlines into <p> and <br />s."""
	value = re.sub(r'\r\n|\r|\n', '\n', force_unicode(value)) # normalize newlines
	paras = re.split('\n{2,}', value)
	if autoescape:
		paras = [u'%s' % escape(p).replace('\n', '<br />') for p in paras]
	else:
		paras = [u'%s' % p.replace('\n', '<br />') for p in paras]
	return u'\n\n'.join(paras)
linebreaks = allow_lazy(linebreaks, unicode)

def strip_tags(value):
	"""Returns the given HTML with all tags stripped."""
	return re.sub(r'<[^>]*?>', '', force_unicode(value))
strip_tags = allow_lazy(strip_tags)

def strip_spaces_between_tags(value):
	"""Returns the given HTML with spaces between tags removed."""
	return re.sub(r'>\s+<', '><', force_unicode(value))
strip_spaces_between_tags = allow_lazy(strip_spaces_between_tags, unicode)

def strip_entities(value):
	"""Returns the given HTML with all entities (&something;) stripped."""
	return re.sub(r'&(?:\w+|#\d+);', '', force_unicode(value))
strip_entities = allow_lazy(strip_entities, unicode)

def fix_ampersands(value):
	"""Returns the given HTML with all unencoded ampersands encoded correctly."""
	return unencoded_ampersands_re.sub('&amp;', force_unicode(value))
fix_ampersands = allow_lazy(fix_ampersands, unicode)



def clean_html(text):
	"""
	Clean the given HTML.  Specifically, do the following:
		* Convert <b> and <i> to <strong> and <em>.
		* Encode all ampersands correctly.
		* Remove all "target" attributes from <a> tags.
		* Remove extraneous HTML, such as presentational tags that open and
		  immediately close and <br clear="all">.
		* Convert hard-coded bullets into HTML unordered lists.
		* Remove stuff like "<p>&nbsp;&nbsp;</p>", but only if it's at the
		  bottom of the text.
	"""
	from django.utils.text import normalize_newlines
	text = normalize_newlines(force_unicode(text))
	text = re.sub(r'<(/?)\s*b\s*>', '<\\1strong>', text)
	text = re.sub(r'<(/?)\s*i\s*>', '<\\1em>', text)
	text = fix_ampersands(text)
	# Remove all target="" attributes from <a> tags.
	text = link_target_attribute_re.sub('\\1', text)
	# Trim stupid HTML such as <br clear="all">.
	text = html_gunk_re.sub('', text)
	# Convert hard-coded bullets into HTML unordered lists.
	def replace_p_tags(match):
		s = match.group().replace('</p>', '</li>')
		for d in DOTS:
			s = s.replace('<p>%s' % d, '<li>')
		return u'<ul>\n%s\n</ul>' % s
	text = hard_coded_bullets_re.sub(replace_p_tags, text)
	# Remove stuff like "<p>&nbsp;&nbsp;</p>", but only if it's at the bottom
	# of the text.
	text = trailing_empty_content_re.sub('', text)
	return text
clean_html = allow_lazy(clean_html, unicode)
