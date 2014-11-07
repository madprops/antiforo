from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	#url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'/home/yo/antiforo/media'}),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'/home/localghost/webapps/antiforo/antiforo/media'}),
	(r'^$', 'server.views.main'),
	(r'^entrar/$', 'server.views.enter'),
	(r'^thumbs/$', 'server.views.thumbs'),
	(r'^vote/$', 'server.views.vote'),
	(r'^update_poll_results/$', 'server.views.update_poll_results'),
	(r'^opciones/$', 'server.views.options'),
	(r'^load_more_threads/$', 'server.views.load_more_threads'),
	(r'^load_more_posts/$', 'server.views.load_more_posts'),
	(r'^nuevo/$', 'server.views.new_thread'),
	(r'^encuesta/$', 'server.views.new_poll'),
	(r'^(?P<id>[\w\ ]+)/$', 'server.views.thread'),
	(r'^(?P<id>[\w\ ]+)/responder/$', 'server.views.post'),
	(r'^(?P<forum>[\w]+)/$', 'server.views.forum'),
)
