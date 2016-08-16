from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^boardgame/name/$', views.boardgames, name='boardgames'),
    url(r'^boardgame/id/(?P<boardgame_id>[0-9]+(,[0-9]+)*)/$', views.boardgames_id, name='boardgame_id'),
    url(r'^boardgame/name/(?P<boardgame_name>[a-zA-Z0-9 ]+(,[A-Za-z0-9 ]+)*)/$', views.boardgames_name, name='boardgame_name'),
    url(r'^player/add/$', views.add_player ),
    #url(r'^login/(?P<login>(.)+)/(?P<password>(.)+)/$', views.login, name='login'),
]