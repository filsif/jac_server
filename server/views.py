from django.shortcuts import render

from django.http import HttpResponse

from django.core import serializers as szs

from server.models import BoardGame



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def boardgames_id(request, boardgame_id):
    
    datas = boardgame_id.split(',')
    
    objs = []
    
    for elem in datas:
        try:
            obj = BoardGame.objects.get(pk=int(elem))
        except BoardGame.DoesNotExist:
            pass
        else:
            objs.append( obj )
    data = szs.serialize("json",objs)
    return HttpResponse( data )


def boardgames_name(request, boardgame_name):
    
    datas = boardgame_name.split(',')
    
    objs = []
    
    for elem in datas:
        try:
            obj = BoardGame.objects.filter(name__startswith=elem)
        except BoardGame.DoesNotExist:
            pass
        else:
            objs += obj
    
    print objs
    data = szs.serialize("json",objs)
    return HttpResponse( data )