from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.SiteHome.as_view()),

    url(r'^e/(?P<slug>.+)/(?P<pk>\d+)/$',
        views.EventDetail.as_view(),
        name='events.event_detail'),
]
