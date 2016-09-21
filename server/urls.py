from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^boardgame/name/$', views.boardgames, name='boardgames'),
    url(r'^boardgame/id/(?P<boardgame_id>[0-9]+(,[0-9]+)*)/$', views.boardgames_id, name='boardgame_id'),
    url(r'^boardgame/name/(?P<boardgame_name>[a-zA-Z0-9 ]+(,[A-Za-z0-9 ]+)*)/$', views.boardgames_name, name='boardgame_name'),
    url(r'^boardgame/add/$' , views.add_boardgame ),
    url(r'^player/add/$', views.add_player ),
    url(r'^player/email/(?P<email>(.)+)/$', views.check_email ),
    url(r'^player/nickname/(?P<nickname>(.)+)/$', views.check_nickname ),
    url(r'^players$', views.players ),
    url(r'^login/(?P<user>(.)+)/(?P<password>(.)+)/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]