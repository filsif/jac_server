from django.shortcuts import render

from django.http import HttpResponse , Http404

from django.core import serializers as szs

from server.models import BoardGame , Player

from server.forms import *




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

def boardgames(request ):     
    data = szs.serialize("json",BoardGame.objects.all())
    return HttpResponse( "filsif\r\n" + data )


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
    
    print (objs)
    data = szs.serialize("json",objs)
    if request.session.get('has_commented', False):
        return HttpResponse( "already got" )
    else:
        request.session['has_commented'] = True
        return HttpResponse(data)

'''
def login( request, login , password ):
    pass
'''

def add_player(request):
    if request.method == 'POST':
        print ("TOTO : " + str(request.POST)) 
        form = PlayerForm(request.POST)
        if form.is_valid():
            firstname       = form.cleaned_data['firstname']
            lastname        = form.cleaned_data['lastname']
            nickname        = form.cleaned_data['nickname']
            photo           = form.cleaned_data['photo']
            age             = form.cleaned_data['age']
            address         = form.cleaned_data['address']
            email           = form.cleaned_data['email']
            mobile_phone    = form.cleaned_data['mobile_phone']
            
            query = Player(firstname = firstname , lastname = lastname , nickname = nickname , photo = photo , age = age , address = address , email = email , mobile_phone = mobile_phone )
            query.save()
            
            
            
          
            data = szs.serialize("json" , Player.objects.filter( pk = query.pk ) )
            
            
            
            return HttpResponse(  data )
        else:
            raise Http404("Form is not valid : " + str(form.errors) )
    else:
        raise Http404("Not a POST request")
            