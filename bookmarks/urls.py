from django.conf.urls.defaults import *

# for voting
from voting.views import vote_on_object
from bookmarks.models import Bookmark
from bookmarks.forms import BookmarkInstanceForm, BookmarkInstanceEditForm

urlpatterns = patterns('',
    url(r'^$', 'bookmarks.views.bookmarks', name="all_bookmarks"),
    url(r'^your_bookmarks/$', 'bookmarks.views.your_bookmarks', name="your_bookmarks"),
    url(r'^your_public_bookmarks/$', 'bookmarks.views.your_public_bookmarks', name="your_public_bookmarks"),
    url(r'^add/$', 'bookmarks.views.add', name="add_bookmark"),
    url(r'^(\d+)/delete/$', 'bookmarks.views.delete', name="delete_bookmark_instance"),
    url(r'^(\d+)/edit/$', 'bookmarks.views.edit', name="edit_bookmark_instance"),    
    
    # for voting
    (r'^(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$',
        vote_on_object, dict(
            model=Bookmark,
            template_object_name='bookmark',
            template_name='kb/link_confirm_vote.html',
            allow_xmlhttprequest=True)),

    # ajax validation
    (r'^validate_add/$', 'ajax_validation.views.validate', 
        {'form_class': BookmarkInstanceForm, 
        'callback': lambda request, 
        *args, 
        **kwargs: {'user': request.user}}, 
        'bookmark_instance_form_validate'),
        
    # ajax validation
    (r'^validate_edit/$', 'ajax_validation.views.validate', 
        {'form_class': BookmarkInstanceEditForm, 
        'callback': lambda request, 
        *args, 
        **kwargs: {'user': request.user}}, 
        'bookmark_instance_edit_form_validate'),        
            
            
)


## for restapi
#from django_restapi.model_resource import Collection
#from django_restapi.responder import XMLResponder, JSONResponder
#from django_restapi.receiver import XMLReceiver, JSONReceiver

#xml_bookmarks_resource = Collection(
#    queryset = Bookmark.objects.all(),
#    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
#    receiver = XMLReceiver(),
#    responder = XMLResponder(paginate_by = 10)
#)

#json_bookmarks_resource = Collection(
#    queryset = Bookmark.objects.all(),
#    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
#    responder = JSONResponder(paginate_by=10)
#)
#from bookmarks.models import BookmarkInstance

#xml_bookmarkinstances_resource = Collection(
#    queryset = BookmarkInstance.objects.all(),
#    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
#    receiver = XMLReceiver(),
#    responder = XMLResponder(paginate_by = 10)
#)

#json_bookmarkinstances_resource = Collection(
#    queryset = BookmarkInstance.objects.all(),
#    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
#    responder = JSONResponder(paginate_by=10)
#)

#from bookmarks.feeds import BookmarkFeed, RSS1BookmarkFeed, AtomBookmarkFeed, RDFBookmarkFeed
#feeds_dict = {
#    'rss':  BookmarkFeed,
#    'rss1': RSS1BookmarkFeed,
#    'atom': AtomBookmarkFeed,
#    'rdf': RDFBookmarkFeed,
#}
#bookmarks_feed_dict = {"feed_dict": feeds_dict}


urlpatterns += patterns('',

# duy
#    (r'^feeds/bookmarks/(.*)/?$', 'django.contrib.syndication.views.feed', bookmarks_feed_dict),
#    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', bookmarks_feed_dict),
    url(r'^feeds/(?P<feedtype>\w+)/bookmark/$', 'bookmarks.views.bookmark_feed', name='bookmark_feed'),
    url(r'^feeds/(?P<feedtype>\w+)/bookmark/(?P<id_slug>\d+)/$', 'bookmarks.views.bookmark_feed', name='bookmark_feed'),

#    # for json
#    (r'^api/json/(?P<model_name>[\d\w]+)/$', 'bookmarks.serializers.bookmarks_json'),
#    (r'^api/json/(?P<model_name>[\d\w]+)/(?P<object_id>\d+)/$', 'bookmarks.serializers.bookmarks_json'),
##    (r'^json/', include('json.urls')),
#    # for xml
#    (r'^api/xml/(?P<model_name>[\d\w]+)/$', 'bookmarks.serializers.bookmarks_xml'),
#    (r'^api/xml/(?P<model_name>[\d\w]+)/(?P<object_id>\d+)/$', 'bookmarks.serializers.bookmarks_xml'),
    url(r'^api/(?P<format>\w+)/(?P<model_name>[\d\w]+)/$', 'bookmarks.serializers.bookmarks', name="bookmark_serializer"),
    url(r'^api/(?P<format>\w+)/(?P<model_name>[\d\w]+)/(?P<object_id>\d+)/$', 'bookmarks.serializers.bookmarks', name="bookmark_serializer"),

#    # for restapi
#    (r'^api/rest/xml/bookmark/(.*?)/?$', xml_bookmarks_resource),
#    (r'^api/rest/json/bookmark/(.*?)/?$', json_bookmarks_resource),
#    (r'^api/rest/xml/bookmarkinstance/(.*?)/?$', xml_bookmarkinstances_resource),
#    (r'^api/rest/json/bookmarkinstance/(.*?)/?$', json_bookmarkinstances_resource),


#permitted_methods = ('GET', 'POST', 'PUT', 'DELETE')
#from django.db.models.loading import get_model
#    url(r'^api/rest/(?P<format>\w+)/(?P<model_name>[\d\w]+)/(.*?)/?$', Collection(
#        queryset = get_model("bookmarks", model_name).objects.all(), 
#        permitted_methods = permitted_methods, 
#        receiver = None if (format == "json") else XMLReceiver(), 
#        responder = JSONResponder(paginate_by=10) if (format == "json") else XMLResponder(paginate_by = 10)
#    ), name="bookmark_rest"),
    url(r'^api/rest/(?P<format>\w+)/(?P<model_name>[\d\w]+)/$', 'bookmarks.rest.bookmarks', name="bookmark_rest"),
    url(r'^api/rest/(?P<format>\w+)/(?P<model_name>[\d\w]+)/(?P<object_id>[\d]+)/$', 'bookmarks.rest.bookmarks', name="bookmark_rest"),

)
