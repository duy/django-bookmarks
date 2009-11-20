#from atomformat import Feed
# to add categories to feeds, don't know to do it with atomformat library
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed, RssUserland091Feed
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from bookmarks.models import Bookmark
from django.template.defaultfilters import linebreaks, escape, capfirst
from datetime import datetime

ITEMS_PER_FEED = getattr(settings, 'PINAX_ITEMS_PER_FEED', 20)


class BookmarkFeed(Feed):

#    feed_url
#    slug 
#    title
    # in RSS2, Atom, RSS1, <title>Bookmarks Feeds for Rhizomatik Labs</title>
    def title(self, bookmark):
        if not bookmark:
            return 'Bookmarks Feeds'
        else:
            return 'Bookmarks Feeds for %s' % bookmark.description
#    link
    def link(self, bookmark):
        if not bookmark:
            return 'http://%s/feeds/bookmarks/%s' % (Site.objects.get_current().domain, self.slug) # <id>http://example.com/feeds/bookmarks/rss</id>
        else:
            bookmarks_url = bookmark.get_absolute_url().split('/')[1]
            bookmark_id = bookmark.get_absolute_url().split('/')[2]
            return 'http://%s/feeds/%s/%s/%s' % (Site.objects.get_current().domain, bookmarks_url, self.slug, bookmark_id) # <id>http://example.com/feeds/bookmarks/rss/1</id>

#    feed_guid 
    # in Atom 
    def feed_guid(self, bookmark):
        if not bookmark:
            return 'http://%s/feeds/bookmarks/%s' % (Site.objects.get_current().domain, self.slug) # <id>http://example.com/feeds/bookmarks/atom</id>
        else:
            bookmarks_url = bookmark.get_absolute_url().split('/')[1]
            bookmark_id = bookmark.get_absolute_url().split('/')[2]
            return 'http://%s/feeds/%s/%s/%s' % (Site.objects.get_current().domain, bookmarks_url, self.slug, bookmark_id) # <id>http://example.com/feeds/bookmarks/atom/1</id>
#    description
    # in RSS2, RSS1, <description>Updates on changes and additions to Bookmarks Feeds</description>
    def description(self, bookmark):
        if not bookmark:
            return 'Updates on changes and additions to Bookmarks Feeds'
        else:
            return 'Updates on changes and additions to Bookmarks Feeds for %s' % bookmark.description

#    author_name
    def author_name(self, bookmark):
        if bookmark:
            return bookmark.adder.username
#    author_email
    def author_email(self, bookmark):
        if bookmark:
            return bookmark.adder.email
#    author_link
    def author_link(self, bookmark):
        if bookmark:
            return bookmark.adder.get_profile().website
#    categories
    def categories(self, bookmark):
        if bookmark:
            from tagging.models import Tag
    #        return Tag.objects.get_for_object(bookmark)
            return bookmark.all_tags()
#    copyright
#    ttl
#    items
    def items(self, bookmark):
        if not bookmark:
            return Bookmark.objects.order_by("-added")[:ITEMS_PER_FEED]
        else:
            return [bookmark]
#    item_link
    # in RSS2, <link>http://rhizomatik.net/</link>
    # in Atom, <link href="http://rhizomatik.net/" rel="alternate"></link>
    # in RSS1, <link>http://rhizomatik.net/</link>
    def item_link(self, bookmark):
        return bookmark.url
#    item_guid
    # in RSS1, <guid>1</guid>
    def item_guid(self, bookmark):
        return str(bookmark.id)
#    item_autor_name
    def item_author_name(self, bookmark):
        return bookmark.adder.username
#    item_author_email
    def item_author_email(self, bookmark):
        return bookmark.adder.email
#    item_author_link
    def item_author_link(self, bookmark):
        return bookmark.adder.get_profile().website
#    item_enclosure_url
#    item_enclosure_mime_type
#    item_copyright
#    item_pubdate
    # in RSS2, <pubDate>Sun, 15 Nov 2009 07:40:24 -0500</pubDate>
    def item_pubdate(self, bookmark):
        return bookmark.added
#    item_categories
    # in RSS2, <category>rhizomatik</category><category>rhizome</category><category>social networks</category>
    # in Atom, <category>rhizomatik</category><category>rhizome</category><category>social networks</category>
    def item_categories(self, bookmark):
        from tagging.models import Tag
#        return Tag.objects.get_for_object(bookmark)
        return bookmark.all_tags()
#    comments

    # for item_title, must be a template
    title_template = 'feeds/rss_title.html'
    description_template = 'feeds/rss_description.html'


    def get_object(self, bits):
        if len(bits) > 0:
            return Bookmark.objects.get(id__exact=bits[0])


    
class AtomBookmarkFeed(BookmarkFeed):
    feed_type = Atom1Feed
    subtitle = BookmarkFeed.description # <subtitle>Updates on changes and additions to Bookmarks Feeds</subtitle>

class RSS1BookmarkFeed(BookmarkFeed):
    feed_type = RssUserland091Feed

from rss10 import RdfFeed
class RDFBookmarkFeed(BookmarkFeed):
    feed_type = RdfFeed
    
    
#    def __init__(self, request,
#                 group_slug=None, bridge=None,
#                 bookmark_qs=ALL_BOOKMARK
#                 extra_context=None,
#                 title_template = u'feeds/rss_title.html',
#                 description_template = u'feeds/rss_description.html',
#                 *args, **kw):


#        self.title_template = title_template
#        self.description_template = description_template
#        super(BookmarkFeed, self).__init__('', request)
#    def items(self):
#        return Bookmark.objects.order_by("-added")[:ITEMS_PER_FEED]

#    def item_pubdate(self, item):
#        """
#        Return the item's pubdate. It's this modified date
#        """
#        return item.modified

