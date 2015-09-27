from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ask_pupkin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'asking.views.index'),
    url(r'^signup/$', 'asking.views.signup'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^answer/$', 'asking.views.answer'),
    url(r'^index/best/$', 'asking.views.index', {'sort': 'best'}),
    url(r'^ask/$', 'asking.views.ask'),
    url(r'^like/$', 'asking.views.like'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
