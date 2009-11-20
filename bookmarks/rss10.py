
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.feedgenerator import SyndicationFeed

class RdfFeed(SyndicationFeed):
    # http://www.w3.org/TR/rdf-syntax-grammar/
    # http://web.resource.org/rss/1.0/spec
    mime_type = 'application/rdf+xml'
    ns_rdf = u'http://www.w3.org/1999/02/22-rdf-syntax-ns'
    ns_rss = u'http://purl.org/rss/1.0'
    ns_dc= u"http://purl.org/dc/elements/1.1/"

    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement(u"rdf:RDF", self.root_attributes())
        
        handler.startElement(u"rss:channel",  dict(tuple(self.rss_attributes().items())+((u"rdf:about", self.feed["link"]),)))
        self.add_root_elements(handler)
        self.endChannelElement(handler)
        self.write_items(handler)
        handler.endElement(u"rdf:RDF")

    # <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    def root_attributes(self):
        if self.feed['language'] is not None:
            return {u"xmlns:rdf": self.ns_rdf, u"xml:lang": self.feed['language']}
        else:
            return {u"xmlns:rdf": self.ns_rdf}

    # <rss:channel xmlns:rss="http://purl.org/rss/1.0/" rdf:about="http://localhost:8890/bookmark/4/">
    def rss_attributes(self):
            return {u"xmlns:rss": self.ns_rss}

    def add_root_elements(self, handler):
        handler.addQuickElement(u"rss:title", self.feed['title'])
        handler.addQuickElement(u"rss:link", self.feed['link'])
        handler.addQuickElement(u"rss:description", self.feed['description'])

        #   <dc:date xmlns:dc="http://purl.org/dc/elements/1.1/">2009-11-19T16:05:18Z</dc:date>
        handler.addQuickElement(u"dc:date", self.latest_post_date().strftime('%Y-%m-%dT%H:%M:%SZ'), {u"xmlns:dc": self.ns_dc})
        # <dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/" />
        handler.addQuickElement(u"dc:creator", self.feed["author_name"], {u"xmlns:dc": self.ns_dc})
        self.add_root_item_elements(handler)

    def add_root_item_elements(self, handler):
        #   <rss:items>
        handler.startElement(u'rss:items', {})
        #   <rdf:Seq>
        handler.startElement(u'rdf:Seq', {})
        for item in self.items:
            #      <rdf:li rdf:resource="http://rhizomatik.net" />
            handler.addQuickElement(u"rdf:li", attrs={u"rdf:resource":  item['link']})
        handler.endElement(u'rdf:Seq')
        handler.endElement(u'rss:items')

    def write_items(self, handler):
        for item in self.items:
            #  <rss:item xmlns:rss="http://purl.org/rss/1.0/" rdf:about="http://rhizomatik.net">
#            handler.startElement(u'rss:item', self.rss_attributes(), self.item_attributes(item))
            handler.startElement(u'rss:item', dict(tuple(self.rss_attributes().items())+tuple(self.item_attributes(item).items())))
            self.add_item_elements(handler, item)
            handler.endElement(u"rss:item")

    def item_attributes(self, item):
        return {u"rdf:about": item['link']}

    def add_item_elements(self, handler, item):
#      <rss:title>rhizomatik labs</rss:title>
        handler.addQuickElement(u"rss:title", item['title'])
#      <rss:link>http://rhizomatik.net</rss:link>
        handler.addQuickElement(u"rss:link", item['link'])
        if item['pubdate'] is not None:
#      <dc:date xmlns:dc="http://purl.org/dc/elements/1.1/">2009-11-19T16:04:27Z</dc:date> 2009-11-15T07:40:24-05:00
            handler.addQuickElement(u"dc:date", item['pubdate'].strftime('%Y-%m-%dT%H:%M:%SZ'), {u"xmlns:dc": self.ns_dc}) #2009-11-04T04:50:58Z
        if item['author_name'] is not None:
            handler.addQuickElement(u"dc:creator", item["author_name"], {u"xmlns:dc": self.ns_dc})
#      <dc:description xmlns:dc="http://purl.org/dc/elements/1.1/">0</dc:description>
        if item['description'] is not None:
            handler.addQuickElement(u"dc:description", item['description'], {u"xmlns:dc": self.ns_dc})
#      <content:encoded xmlns:content="http://purl.org/rss/1.0/modules/content/"><![CDATA[0]]></content:encoded>
#        if item['content'] is not None:
#            handler.addQuickElement(u"content:encoded", item['content'], {u"xmlns:content": u"http://purl.org/rss/1.0/modules/content"})

    def endChannelElement(self, handler):
        handler.endElement(u"rss:channel")

